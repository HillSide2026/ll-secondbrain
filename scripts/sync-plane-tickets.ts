const fs = require("node:fs/promises");
const path = require("node:path");

const REQUIRED_ENV = [
  "PLANE_API_KEY",
  "PLANE_WORKSPACE_SLUG",
  "PLANE_API_BASE_URL",
];

const DEFAULT_MAPPING_FILE = path.join(
  process.cwd(),
  "00_SYSTEM",
  "integrations",
  "plane",
  "project-map.json"
);
const PROJECT_SEARCH_ROOTS = ["04_INITIATIVES", "05_MATTERS"];
const DEFAULT_LINKS_SECTION = `## Links

- Related notes:
- Related projects:
- Related decisions:`;

function requireEnv() {
  const missing = REQUIRED_ENV.filter((key) => !process.env[key]);
  if (missing.length > 0) {
    throw new Error(
      `Missing required environment variable(s): ${missing.join(", ")}`
    );
  }

  return {
    apiKey: process.env.PLANE_API_KEY,
    workspaceSlug: process.env.PLANE_WORKSPACE_SLUG,
    apiBaseUrl: process.env.PLANE_API_BASE_URL.replace(/\/+$/, ""),
    mappingFile: process.env.PLANE_PROJECT_MAP_FILE || DEFAULT_MAPPING_FILE,
  };
}

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJsonFile(filePath) {
  try {
    return JSON.parse(await fs.readFile(filePath, "utf8"));
  } catch (error) {
    if (error && error.code === "ENOENT") {
      throw new Error(`Plane project mapping file not found: ${filePath}`);
    }
    throw new Error(`Invalid Plane project mapping file ${filePath}: ${error}`);
  }
}

async function scanProjectFolders() {
  const projectFolders = new Set();

  async function walk(dir, depth) {
    if (depth < 0 || !(await pathExists(dir))) return;
    const entries = await fs.readdir(dir, { withFileTypes: true });
    const names = new Set(entries.map((entry) => entry.name));

    if (
      names.has("PROJECT_CHARTER.md") ||
      names.has("PROJECT_PLAN.md") ||
      names.has("MATTER.yaml") ||
      names.has("MATTER_BRIEF.md")
    ) {
      projectFolders.add(path.relative(process.cwd(), dir));
    }

    for (const entry of entries) {
      if (!entry.isDirectory() || entry.name.startsWith(".")) continue;
      await walk(path.join(dir, entry.name), depth - 1);
    }
  }

  for (const root of PROJECT_SEARCH_ROOTS) {
    await walk(path.join(process.cwd(), root), 5);
  }

  return projectFolders;
}

function normalizeMapping(rawMapping) {
  const entries = Array.isArray(rawMapping.projects)
    ? rawMapping.projects
    : Object.entries(rawMapping.projects || {}).map(([planeProject, config]) => ({
        plane_project: planeProject,
        ...config,
      }));

  const byKey = new Map();
  for (const entry of entries) {
    if (!entry || typeof entry !== "object") continue;
    const keys = [
      entry.plane_project_id,
      entry.plane_project_slug,
      entry.plane_project_name,
      entry.plane_project,
    ].filter(Boolean);
    for (const key of keys) byKey.set(String(key), entry);
  }

  return byKey;
}

function projectKeys(project) {
  return [
    project.id,
    project.pk,
    project.identifier,
    project.slug,
    project.name,
  ]
    .filter(Boolean)
    .map(String);
}

function resolveProjectMapping(project, mappingByKey) {
  for (const key of projectKeys(project)) {
    const mapping = mappingByKey.get(key);
    if (mapping) return mapping;
  }
  return null;
}

async function validateMapping(project, mapping) {
  const projectPath = compact(mapping.project_path);
  const ticketDir = compact(mapping.ticket_dir);
  if (!projectPath || !ticketDir) {
    console.warn(
      `Skipping Plane project "${pickName(project)}": mapping requires project_path and ticket_dir.`
    );
    return null;
  }

  if (path.isAbsolute(projectPath) || path.isAbsolute(ticketDir)) {
    console.warn(
      `Skipping Plane project "${pickName(project)}": mapping paths must be repo-relative.`
    );
    return null;
  }

  const normalizedProjectPath = path.normalize(projectPath);
  if (normalizedProjectPath.startsWith("..")) {
    console.warn(
      `Skipping Plane project "${pickName(project)}": project_path escapes repo.`
    );
    return null;
  }

  const absoluteProjectPath = path.join(process.cwd(), normalizedProjectPath);
  if (!(await pathExists(absoluteProjectPath))) {
    console.warn(
      `Skipping Plane project "${pickName(project)}": mapped project_path does not exist: ${projectPath}`
    );
    return null;
  }

  const normalizedTicketDir = path.normalize(ticketDir);
  if (normalizedTicketDir.startsWith("..")) {
    console.warn(
      `Skipping Plane project "${pickName(project)}": ticket_dir escapes project folder.`
    );
    return null;
  }

  return {
    projectPath: normalizedProjectPath,
    outputDir: path.join(absoluteProjectPath, normalizedTicketDir),
    ticketDir: normalizedTicketDir,
  };
}

function normalizeArrayResponse(payload) {
  if (Array.isArray(payload)) return { items: payload, hasMore: false };
  if (!payload || typeof payload !== "object") {
    throw new Error("Plane response was not an object or array");
  }

  const candidates = [
    payload.results,
    payload.items,
    payload.projects,
    payload.work_items,
    payload.issues,
    payload.data,
  ];
  const items = candidates.find(Array.isArray);
  if (!items) {
    throw new Error(
      `Plane response did not contain a recognized list field: ${Object.keys(
        payload
      ).join(", ")}`
    );
  }

  return {
    items,
    hasMore: Boolean(payload.next) || Boolean(payload.next_cursor),
  };
}

async function fetchJson(url, apiKey) {
  const response = await fetch(url, {
    headers: {
      "x-api-key": apiKey,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(
      `Plane API request failed ${response.status} ${response.statusText}: ${url}\n${body}`
    );
  }

  try {
    return await response.json();
  } catch (error) {
    throw new Error(`Plane API returned invalid JSON for ${url}: ${error}`);
  }
}

async function fetchPaginated(baseUrl, apiKey) {
  const limit = 100;
  let offset = 0;
  const allItems = [];

  while (true) {
    const url = new URL(baseUrl);
    url.searchParams.set("limit", String(limit));
    url.searchParams.set("offset", String(offset));

    const payload = await fetchJson(url.toString(), apiKey);
    const { items, hasMore } = normalizeArrayResponse(payload);
    allItems.push(...items);

    if (items.length < limit && !hasMore) break;
    if (items.length === 0) break;
    offset += limit;
  }

  return allItems;
}

function compact(value) {
  if (value === null || value === undefined) return "";
  if (typeof value === "string") return value.trim();
  if (typeof value === "number" || typeof value === "boolean") {
    return String(value);
  }
  return "";
}

function pickName(value) {
  if (!value) return "";
  if (typeof value === "string") return value;
  return compact(
    value.name ||
      value.display_name ||
      value.first_name ||
      value.username ||
      value.email ||
      value.identifier ||
      value.slug ||
      value.id
  );
}

function normalizeLabels(issue) {
  const rawLabels = issue.labels || issue.label_details || issue.label || [];
  const labels = Array.isArray(rawLabels) ? rawLabels : [rawLabels];
  return labels.map(pickName).filter(Boolean);
}

function normalizeAssignee(issue) {
  const rawAssignees =
    issue.assignees ||
    issue.assignee_details ||
    issue.assignee ||
    issue.assignees_list ||
    [];
  const assignees = Array.isArray(rawAssignees) ? rawAssignees : [rawAssignees];
  return assignees.map(pickName).filter(Boolean).join(", ");
}

function normalizeIssue(issue, project, workspaceSlug, apiBaseUrl) {
  const id = compact(issue.id || issue.issue_id || issue.pk);
  if (!id) throw new Error(`Plane work item is missing an id: ${JSON.stringify(issue)}`);

  const projectName = pickName(issue.project_detail || issue.project || project);
  const state = pickName(issue.state_detail || issue.state || issue.state_name);
  const labels = normalizeLabels(issue);
  const assignee = normalizeAssignee(issue);
  const cycle = pickName(issue.cycle_detail || issue.cycle || issue.cycle_name);
  const title = compact(issue.name || issue.title || issue.issue_name);
  const description = compact(
    issue.description_stripped ||
      issue.description_markdown ||
      issue.description ||
      issue.description_html
  );

  return {
    id,
    url:
      compact(issue.url || issue.html_url || issue.issue_url) ||
      buildPlaneUrl(apiBaseUrl, workspaceSlug, project.id || project.pk, id),
    project: projectName,
    title: title || `Plane ${id}`,
    state,
    priority: compact(issue.priority),
    assignee,
    labels,
    cycle,
    createdAt: compact(issue.created_at || issue.created || issue.created_on),
    updatedAt: compact(issue.updated_at || issue.updated || issue.updated_on),
    description,
  };
}

function buildPlaneUrl(apiBaseUrl, workspaceSlug, projectId, issueId) {
  let appBaseUrl = apiBaseUrl.replace(/\/+$/, "");
  if (appBaseUrl === "https://api.plane.so") {
    appBaseUrl = "https://app.plane.so";
  }
  return `${appBaseUrl}/${workspaceSlug}/projects/${projectId}/issues/${issueId}`;
}

function yamlString(value) {
  return JSON.stringify(compact(value));
}

function yamlArray(values) {
  return `[${values.map((value) => JSON.stringify(value)).join(", ")}]`;
}

function markdownListValue(values) {
  return values.length > 0 ? values.join(", ") : "";
}

function extractManualSections(existingContent) {
  if (!existingContent) return DEFAULT_LINKS_SECTION;
  const match = existingContent.match(/^## Links\s*[\s\S]*$/m);
  return match ? match[0].trimEnd() : DEFAULT_LINKS_SECTION;
}

function extractLastSynced(existingContent) {
  if (!existingContent) return "";
  const match = existingContent.match(/^last_synced:\s*("?)(.*?)\1\s*$/m);
  return match ? match[2] : "";
}

function renderTicket(ticket, mappingInfo, lastSynced, manualSections) {
  return `---
source: plane
generated_by: sync-plane-tickets
plane_id: ${yamlString(ticket.id)}
plane_url: ${yamlString(ticket.url)}
project: ${yamlString(ticket.project)}
repo_project_path: ${yamlString(mappingInfo.projectPath)}
title: ${yamlString(ticket.title)}
status: ${yamlString(ticket.state)}
priority: ${yamlString(ticket.priority)}
assignee: ${yamlString(ticket.assignee)}
labels: ${yamlArray(ticket.labels)}
cycle: ${yamlString(ticket.cycle)}
created: ${yamlString(ticket.createdAt)}
updated: ${yamlString(ticket.updatedAt)}
last_synced: ${yamlString(lastSynced)}
---

# ${ticket.title}

## Summary

${ticket.description || "_No description provided._"}

## Plane Metadata (generated)

- Status: ${ticket.state}
- Priority: ${ticket.priority}
- Project: ${ticket.project}
- Assignee: ${ticket.assignee}
- Labels: ${markdownListValue(ticket.labels)}
- Cycle: ${ticket.cycle}
- Plane URL: ${ticket.url}
- Repo project: ${mappingInfo.projectPath}

${manualSections}
`;
}

async function readExisting(filePath) {
  try {
    return await fs.readFile(filePath, "utf8");
  } catch (error) {
    if (error && error.code === "ENOENT") return "";
    throw error;
  }
}

async function writeIfChanged(filePath, content) {
  const existing = await readExisting(filePath);
  if (existing === content) return false;
  await fs.writeFile(filePath, content, "utf8");
  return true;
}

async function syncPlaneTickets() {
  const env = requireEnv();
  const rawMapping = await readJsonFile(env.mappingFile);
  const mappingByKey = normalizeMapping(rawMapping);

  const workspacePath = `/api/v1/workspaces/${encodeURIComponent(
    env.workspaceSlug
  )}`;
  const projectsUrl = `${env.apiBaseUrl}${workspacePath}/projects/`;
  const projects = await fetchPaginated(projectsUrl, env.apiKey);

  const lastSynced = new Date().toISOString();
  let written = 0;
  let seen = 0;
  let skippedProjects = 0;

  for (const project of projects) {
    const projectId = compact(project.id || project.pk);
    if (!projectId) {
      console.warn(`Skipping Plane project with missing id: ${JSON.stringify(project)}`);
      skippedProjects += 1;
      continue;
    }

    const mapping = resolveProjectMapping(project, mappingByKey);
    if (!mapping) {
      console.warn(
        `Skipping unmapped Plane project "${pickName(project)}" (${projectId}).`
      );
      skippedProjects += 1;
      continue;
    }

    const mappingInfo = await validateMapping(project, mapping);
    if (!mappingInfo) {
      skippedProjects += 1;
      continue;
    }

    await fs.mkdir(mappingInfo.outputDir, { recursive: true });

    const workItemsUrl =
      `${env.apiBaseUrl}${workspacePath}/projects/${encodeURIComponent(
        projectId
      )}/work-items/?expand=labels,assignees,state,project`;
    const issues = await fetchPaginated(workItemsUrl, env.apiKey);

    for (const issue of issues) {
      const ticket = normalizeIssue(
        issue,
        project,
        env.workspaceSlug,
        env.apiBaseUrl
      );
      const safeId = ticket.id.replace(/[^A-Za-z0-9_.-]/g, "-");
      const filePath = path.join(mappingInfo.outputDir, `PLANE-${safeId}.md`);
      const existing = await readExisting(filePath);
      const manualSections = extractManualSections(existing);
      const previousLastSynced = extractLastSynced(existing);
      const comparableMarkdown = renderTicket(
        ticket,
        mappingInfo,
        previousLastSynced || lastSynced,
        manualSections
      );
      const markdown =
        existing === comparableMarkdown
          ? comparableMarkdown
          : renderTicket(ticket, mappingInfo, lastSynced, manualSections);

      if (await writeIfChanged(filePath, markdown)) written += 1;
      seen += 1;
    }
  }

  console.log(
    `Plane sync complete: ${seen} ticket snapshot(s), ${written} file(s) changed, ${skippedProjects} Plane project(s) skipped.`
  );
}

syncPlaneTickets().catch((error) => {
  console.error(`Plane sync failed: ${error.message || error}`);
  process.exitCode = 1;
});

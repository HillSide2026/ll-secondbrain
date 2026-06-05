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

const MATTER_TIERS = ["ESSENTIAL", "STRATEGIC", "STANDARD"];
const MATTERS_ROOT = "05_MATTERS";
const TICKET_DIR = "plane";

const PORTFOLIO_ENTRIES = [
  {
    name: "LL Portfolio",
    identifier: "LLPORT",
    description: "Levine Law firm portfolio projects",
    project_path: "04_INITIATIVES/LL_PORTFOLIO",
    ticket_dir: TICKET_DIR,
  },
  {
    name: "HillSide Portfolio",
    identifier: "HILLSIDE",
    description: "HillSide personal and business projects",
    project_path: "04_INITIATIVES/HillSide_PORTFOLIO",
    ticket_dir: TICKET_DIR,
  },
];

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

function parseMatterYaml(content) {
  const fields = {};
  for (const line of content.split("\n")) {
    const m = line.match(/^(\w+):\s*"?([^"\n]+?)"?\s*$/);
    if (m) fields[m[1]] = m[2].trim();
  }
  return fields;
}

function derivedIdentifier(matterId) {
  // "25-927-00003" -> "M2592700003" (max 12 chars, uppercase)
  return ("M" + matterId.replace(/-/g, "")).slice(0, 12).toUpperCase();
}

function resolveIdentifier(base, existingIdentifiers) {
  if (!existingIdentifiers.has(base)) return base;
  for (let i = 2; i <= 9; i++) {
    const alt = base.slice(0, 11) + String(i);
    if (!existingIdentifiers.has(alt)) return alt;
  }
  return null;
}

async function scanMatterEntries() {
  const entries = [];
  for (const tier of MATTER_TIERS) {
    const tierPath = path.join(process.cwd(), MATTERS_ROOT, tier);
    let dirs;
    try {
      dirs = await fs.readdir(tierPath, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const d of dirs) {
      if (!d.isDirectory() || d.name.startsWith("_")) continue;
      const yamlPath = path.join(tierPath, d.name, "MATTER.yaml");
      let content;
      try {
        content = await fs.readFile(yamlPath, "utf8");
      } catch {
        console.warn(`  No MATTER.yaml: ${tier}/${d.name} — skipping`);
        continue;
      }
      const f = parseMatterYaml(content);
      const matterId = f.matter_id || d.name;
      const matterName = f.matter_name || d.name;
      const practiceArea = f.practice_area || "";
      entries.push({
        name: `${matterName} (${matterId})`,
        identifier: derivedIdentifier(matterId),
        description: `${tier} matter — ${practiceArea}`,
        project_path: `${MATTERS_ROOT}/${tier}/${d.name}`,
        ticket_dir: TICKET_DIR,
      });
    }
  }
  return entries;
}

async function fetchJson(url, apiKey) {
  const res = await fetch(url, {
    headers: { "x-api-key": apiKey, "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(
      `Plane API ${res.status} ${res.statusText}: ${url}\n${body}`
    );
  }
  return res.json();
}

async function postJson(url, apiKey, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "x-api-key": apiKey, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const responseBody = await res.text();
    throw new Error(
      `Plane API ${res.status} ${res.statusText}: ${url}\n${responseBody}`
    );
  }
  return res.json();
}

async function fetchExistingProjects(env) {
  const url = `${env.apiBaseUrl}/api/v1/workspaces/${encodeURIComponent(
    env.workspaceSlug
  )}/projects/?limit=100`;
  const payload = await fetchJson(url, env.apiKey);
  return Array.isArray(payload)
    ? payload
    : payload.results || payload.projects || [];
}

async function readExistingMapping(mappingFile) {
  try {
    return JSON.parse(await fs.readFile(mappingFile, "utf8"));
  } catch {
    return { projects: [] };
  }
}

async function setupPlane() {
  const dryRun = process.argv.includes("--dry-run");
  if (dryRun) console.log("DRY RUN — no Plane projects will be created.\n");

  const env = requireEnv();

  const matterEntries = await scanMatterEntries();
  const allEntries = [...PORTFOLIO_ENTRIES, ...matterEntries];
  console.log(
    `Manifest: ${allEntries.length} projects` +
      ` (${PORTFOLIO_ENTRIES.length} portfolio + ${matterEntries.length} matters)\n`
  );

  const existingProjects = await fetchExistingProjects(env);
  const existingByName = new Map(existingProjects.map((p) => [p.name, p]));
  const existingIdentifiers = new Set(existingProjects.map((p) => p.identifier));
  console.log(`Plane workspace: ${existingProjects.length} existing project(s)\n`);

  const existingMapping = await readExistingMapping(env.mappingFile);
  const mappedPaths = new Set(
    (existingMapping.projects || []).map((p) => p.project_path)
  );
  const newEntries = [...(existingMapping.projects || [])];

  let created = 0;
  let alreadyMapped = 0;
  let linked = 0;
  let failed = 0;

  for (const entry of allEntries) {
    if (mappedPaths.has(entry.project_path)) {
      alreadyMapped++;
      continue;
    }

    // Project already exists in Plane but not yet in our mapping
    if (existingByName.has(entry.name)) {
      const existing = existingByName.get(entry.name);
      console.log(`  Linking existing Plane project: ${entry.name}`);
      if (!dryRun) {
        newEntries.push({
          plane_project_id: existing.id || existing.pk,
          plane_project_name: entry.name,
          project_path: entry.project_path,
          ticket_dir: entry.ticket_dir,
        });
        mappedPaths.add(entry.project_path);
      }
      linked++;
      continue;
    }

    const identifier = resolveIdentifier(entry.identifier, existingIdentifiers);
    if (!identifier) {
      console.error(`  Identifier conflict, could not resolve: ${entry.name}`);
      failed++;
      continue;
    }

    console.log(`  Creating: ${entry.name} [${identifier}]`);
    if (dryRun) {
      created++;
      continue;
    }

    try {
      const created_project = await postJson(
        `${env.apiBaseUrl}/api/v1/workspaces/${encodeURIComponent(
          env.workspaceSlug
        )}/projects/`,
        env.apiKey,
        {
          name: entry.name,
          identifier,
          description: entry.description,
          network: 0,
        }
      );
      const projectId = created_project.id || created_project.pk;
      newEntries.push({
        plane_project_id: projectId,
        plane_project_name: entry.name,
        project_path: entry.project_path,
        ticket_dir: entry.ticket_dir,
      });
      existingIdentifiers.add(identifier);
      mappedPaths.add(entry.project_path);
      created++;
    } catch (err) {
      console.error(`  Failed: ${entry.name} — ${err.message}`);
      failed++;
    }
  }

  if (!dryRun) {
    await fs.mkdir(path.dirname(env.mappingFile), { recursive: true });
    await fs.writeFile(
      env.mappingFile,
      JSON.stringify({ projects: newEntries }, null, 2) + "\n",
      "utf8"
    );
    console.log(`\nMapping written: ${env.mappingFile}`);
  }

  console.log(
    `\nDone: ${created} created, ${linked} linked, ${alreadyMapped} already mapped, ${failed} failed.`
  );
}

setupPlane().catch((err) => {
  console.error(`Setup failed: ${err.message || err}`);
  process.exitCode = 1;
});

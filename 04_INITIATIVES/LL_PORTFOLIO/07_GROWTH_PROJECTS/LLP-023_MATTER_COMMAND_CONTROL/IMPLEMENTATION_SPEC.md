# Implementation Spec

## 1) Target Daily Outputs

- Firm Matter Digest: what moved, what is stuck, what is due
- Per-matter Work Packet baseline (Slice 1 includes status + comm routing)
- Exception lists: unmapped inbox, mapping gaps

## 2) Canonical System Rules

- Clio = matter registry authority
- SharePoint = document authority
- Gmail = communication authority
- ML2 stores only derived/admin artifacts + source pointers
- Every generated assertion must include a source pointer

## 3) Deterministic Paths

Active implementation paths:

- `05_MATTERS/DASHBOARDS/MATTER_DIGEST.md`
- `05_MATTERS/DASHBOARDS/MATTER_INDEX.md`
- `05_MATTERS/DASHBOARDS/INBOX_UNMAPPED.md`
- `05_MATTERS/<tier>/<matter_id>/MATTER_STATUS.md` (generated for routed matters)
- `cache/*.json` snapshots for connector normalization and run state

## 4) Connector Normalization Contracts

### Clio -> MatterRef
`{ clio_matter_id, matter_number, name, status, responsible, client, source_pointer }`

### Gmail -> ThreadRef
`{ thread_id, subject, participants, last_message_at, labels, latest_snippet, source_pointer }`

### SharePoint -> DocRef (Slice 2)
`{ drive_item_id, path, name, modified_at, size, web_url, source_pointer }`

## 5) Matter Resolution Rules

Primary key: Clio matter number.

Routing order:
1. Gmail label path contains matter number (canonical)
2. Subject/snippet fallback contains matter number (review-required)
3. Otherwise route to `INBOX_UNMAPPED.md`

SharePoint mapping:
- Prefer deterministic folder naming with leading matter number
- Use `05_MATTERS/_REGISTRY/matter_sharepoint_map.yml` for explicit overrides

## 6) Agent Responsibilities (Operational)

1. Matter Index Agent
2. Inbox to Matter Router
3. Deadline Extractor (Slice 3)
4. Document Delta Agent (Slice 2)
5. Comms Drafting Agent (Slice 4)
6. Matter Digest Compiler

## 7) Orchestration Modes

- `RUN_MATTER_ADMIN_DAILY`
- `RUN_MATTER_ADMIN_ONE(matter_number)`

## 8) Managed Config Files

Under `00_SYSTEM/CONFIG/`:

- `systems_of_record.yml`
- `matter_folder_rules.yml`
- `gmail_label_rules.yml`
- `deadline_taxonomy.yml`
- `run_schedule.yml`

## 9) Snapshot Store

- `cache/clio_matters.json`
- `cache/gmail_threads.json`
- `cache/sharepoint_files.json`
- `cache/run_state.json`

## 10) Delivery Slices

- Slice 1: matter index + Gmail routing + digest/unmapped
- Slice 2: SharePoint doc index + deltas
- Slice 3: deadline extraction + radar
- Slice 4: comms draft packets

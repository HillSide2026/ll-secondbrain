---
id: POL-035
title: Model Context Protocol Governance
owner: ML1
status: draft
version: 0.1
created_date: 2026-03-09
last_updated: 2026-03-09
tags: [policy, mcp, governance, context, tools, auditability]
---

# POL-035 — Model Context Protocol Governance

## 1. Policy Objective

Policy Statement: Model Context Protocol (MCP) is the mandatory governance layer for model context access and tool execution in ML2.

This policy ensures that:
- Context access is controlled and auditable.
- Tool execution is constrained and permissioned.
- Model interaction with external systems occurs only through structured interfaces.
- ML2 remains the authoritative knowledge system.
- LL consumes only approved outputs.

## 2. Foundational Principle

Models do not access systems directly.
All external interaction must occur through MCP-mediated requests.

Required outcomes:
- Traceability
- Reproducibility
- Security boundaries
- Deterministic workflows

## 3. Architectural Position of MCP in ML2

Canonical stack:
1. User / ML1
2. Application Layer
3. Agent / Orchestrator
4. Language Model
5. MCP (Context and Tool Protocol)
6. Context Servers / Tool Servers / Data Stores / Integrations

Key rule:
- Models cannot bypass MCP.
- All context retrieval and tool invocation must pass through MCP.

## 4. MCP Governance Model

### Layer 1 — Context Governance
Controls what knowledge the model can retrieve.

Includes:
- Documents
- Files
- Knowledge graphs
- Structured records

Rules:
- Context must be retrieved through declared resources.
- Raw prompt stuffing is prohibited.

### Layer 2 — Tool Governance
Controls what actions the model may request.

Examples:
- File read
- SQL query
- API call
- Document generation
- Report compilation

Each tool must define:
- Tool name
- Description
- Input schema
- Output schema
- Permission level
- Execution environment

Rule:
- Tool execution occurs only through the host, never directly by the model.

### Layer 3 — Permission Enforcement
The MCP host enforces permissions for:
- Resource access
- Tool invocation
- System modification

Permission levels:
- `Read`: Access context only
- `Write`: Modify approved documents
- `Execute`: Run defined tools
- `Restricted`: ML1 approval required

### Layer 4 — Auditability
All MCP interactions must produce structured logs.

Each interaction must record:
- Timestamp
- User request
- Model prompt
- Retrieved resources
- Tool calls
- Tool outputs
- Final model output
- System decisions

Rule:
- Logs must be persisted inside ML2.

## 5. MCP Host Policy

The MCP host is the model execution environment (for example: AI application, coding environment, document assistant, orchestration agent).

The host must:
- Enforce tool permissions
- Validate schema inputs
- Mediate tool execution
- Maintain execution logs
- Prevent direct system access by the model

Rule:
- The host is the policy enforcement layer for runtime behavior.

## 6. MCP Server Policy

MCP servers expose resources and tools.

Each server must publish:
- Server name
- Capability type
- Resource schemas
- Tool schemas
- Authentication requirements
- Permission scope

Server categories may include:
- Document servers
- File servers
- Database servers
- API servers
- Tool servers

Rule:
- Servers must not expose unbounded capabilities.

## 7. Context Resource Policy

Resources are structured information sources (documents, repository files, datasets, knowledge graphs).

Each resource must include metadata:
- `resource_id`
- `type`
- `location`
- `version`
- `access_level`
- `owner`
- `last_modified`

Resource retrieval must be:
- Explicit
- Deterministic
- Logged

Rule:
- Blind prompt injection is prohibited.

## 8. Tool Invocation Policy

Tools are model-requested actions (for example: `read_file`, `run_query`, `generate_document`, `create_summary`, `run_script`).

Every tool must define:
- Name
- Description
- Input schema
- Output schema
- Execution environment
- Permission level

The model may:
- Request tool usage
- Propose parameters

The host must:
- Validate parameters
- Enforce permissions
- Execute tools
- Return results through MCP

## 9. Structured Output Policy

MCP interactions must return structured response objects.

Typical fields:
- `model_output`
- `retrieved_context`
- `tool_calls`
- `tool_results`
- `execution_logs`
- `confidence`

Rule:
- Opaque text-only outputs are discouraged for operational workflows.

## 10. Security Policy

MCP implementations must protect against:
- Prompt injection
- Capability escalation
- Arbitrary code execution
- Data leakage

Hard requirements:
- Untrusted context must not gain tool execution authority.
- Models cannot invent or dynamically authorize new tools.
- Only declared tools may be used.
- Shell/scripting/system-modification tools must be sandboxed and permission-gated.
- Sensitive resources require explicit access permissions.

## 11. Interoperability Policy

All external systems integrated into ML2 must expose capabilities through MCP-compatible interfaces.

Examples:
- Repositories
- Document stores
- Internal databases
- Compliance APIs
- Research databases

Rule:
- Heterogeneous integrations must conform to a consistent MCP access pattern.

## 12. Relationship to Agents

Separation of duties:
- Agents determine task strategy and sequencing.
- MCP governs context and system interaction.

Stack:
1. Application
2. Agent
3. Model
4. MCP
5. Tools / Data

Rules:
- Agents may decide tasks and sequence operations.
- Agents may not bypass MCP governance.
- Agents may not directly execute uncontrolled system operations.

## 13. Change Control for MCP Capabilities

All MCP capability changes are governed changes.

Change types include:
- New tools
- Schema modifications
- New resource servers
- Permission changes

Each change requires:
- Change description
- Risk assessment
- Impacted systems
- Rollback plan
- ML1 approval

## 14. LL Execution Boundary

LL may consume outputs that are:
- ML1-approved doctrine, or
- Deterministically derived from approved templates and governed artifacts.

LL must not rely on:
- Raw model output
- Non-audited MCP interactions
- Experimental tool use outside approved capability boundaries

## 15. Known Risk Areas

ML2 must continuously monitor for:
- Context drift
- Unauthorized tool exposure
- Schema inconsistency
- Undocumented integrations

Rule:
- These risks must be recorded in the ML2 system risk register.

## 16. Operational Review

MCP governance review cadence:
- Weekly light review
- Monthly full review

Review topics:
- New integrations
- Security issues
- Tool usage logs
- Context retrieval accuracy
- Schema drift

## 17. Alignment with Second Brain Architecture

MCP governance supports Second Brain architecture by:
- Preserving file-based knowledge authority
- Maintaining inspectability and version control
- Enforcing structured interaction between models and knowledge systems

Target properties:
- Deterministic
- Auditable
- Operator-controlled

Authority (Principles referenced): PRN-020, PRN-022, PRN-024, PRN-026, PRN-028, PRN-029
Enforcement expectation: Any runtime flow that bypasses MCP mediation, invokes undeclared tools, violates permission scope, or omits required audit logs is non-compliant and must be blocked or escalated to ML1.
Supersedes: None
Version: 0.1
Status: Draft

# CODEX Rules

These rules define how Codex contributes to this repository.

## Workflow
- **PR-only contributions:** All changes must be made through pull requests; avoid direct pushes to protected branches.
- **Branch policy:** Use short-lived feature branches named after the change (e.g., `feature/description`). Rebase on main before opening a PR when possible.
- **Small, focused changesets:** Keep pull requests scoped and reviewable, preferring smaller, incremental updates over large batches.
- **No doctrine invention:** Do not introduce new doctrines or policies beyond what is documented. If guidance is missing, ask for clarification rather than inventing rules.

## Pull Request Checklist
Before requesting review, ensure the PR description includes:
1. **Summary:** What changed and why.
2. **Testing:** Commands run and results.
3. **Rollback plan:** How to revert or disable the change safely if issues arise.

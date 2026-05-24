#!/bin/bash
# health.sh — Repo Health Command
#
# Runs all core validation checks for ll-secondbrain_fresh.
# This is the single entry point for "is the system healthy?"
#
# Usage:
#   ./scripts/health.sh            # full check, exit 1 on any error
#   ./scripts/health.sh --quick    # skip slow checks (matter YAML validation)
#   ./scripts/health.sh --fail-on-warn
#                                  # exit 1 on warnings for commits/CI
#
# Exit codes:
#   0 = All checks passed (warnings allowed unless --fail-on-warn)
#   1 = One or more checks FAILED

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

QUICK=false
FAIL_ON_WARN=false
for arg in "$@"; do
  [ "$arg" = "--quick" ] && QUICK=true
  [ "$arg" = "--fail-on-warn" ] && FAIL_ON_WARN=true
done

OVERALL_STATUS=0
WARN_STATUS=0

run_check() {
  local name="$1"
  local cmd="$2"
  echo ""
  echo -e "${BOLD}── $name${NC}"
  if eval "$cmd"; then
    echo -e "${GREEN}PASSED${NC}: $name"
  else
    echo -e "${RED}FAILED${NC}: $name"
    OVERALL_STATUS=1
  fi
}

run_warnable_check() {
  local name="$1"
  local cmd="$2"
  echo ""
  echo -e "${BOLD}── $name${NC}"
  set +e
  eval "$cmd"
  local status=$?
  set -e
  if [ $status -eq 0 ]; then
    echo -e "${GREEN}PASSED${NC}: $name"
  elif [ $status -eq 2 ]; then
    echo -e "${YELLOW}WARN${NC}: $name"
    WARN_STATUS=1
    if [ "$FAIL_ON_WARN" = true ]; then
      OVERALL_STATUS=1
    fi
  else
    echo -e "${RED}FAILED${NC}: $name"
    OVERALL_STATUS=1
  fi
}

echo "========================================"
echo "  ll-secondbrain_fresh Health Check"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# ------------------------------------------------------------
# Check 1: Safety rails (governance, .env, agent specs)
# ------------------------------------------------------------
run_check "Safety Rails" "bash scripts/safety-rails.sh"

# ------------------------------------------------------------
# Check 2: Matter registry integrity (counts + duplicates)
# ------------------------------------------------------------
run_check "Matter Registry Integrity" "python3 scripts/validate_matter_registry.py"

# ------------------------------------------------------------
# Check 3: Governed repo lint
# ------------------------------------------------------------
REPO_LINT_CMD="python3 scripts/repo_lint.py"
if [ "$FAIL_ON_WARN" = true ]; then
  REPO_LINT_CMD="$REPO_LINT_CMD --fail-on-warn"
fi
run_warnable_check "Governed Repo Lint" "$REPO_LINT_CMD"

# ------------------------------------------------------------
# Check 4: HillSide business project packet completeness
# ------------------------------------------------------------
HILLSIDE_PACKET_CMD="python3 00_SYSTEM/scripts/check_hillside_project_packets.py --warn-on-findings"
if [ "$FAIL_ON_WARN" = true ]; then
  HILLSIDE_PACKET_CMD="python3 00_SYSTEM/scripts/check_hillside_project_packets.py --fail-on-findings"
fi
run_warnable_check "HillSide Project Packets" "$HILLSIDE_PACKET_CMD"

# ------------------------------------------------------------
# Check 5: Matter YAML schema validation (skip in --quick mode)
# ------------------------------------------------------------
if [ "$QUICK" = false ]; then
  run_check "Matter YAML Schema" "python3 scripts/validate_matter_yaml.py"
else
  echo ""
  echo -e "${YELLOW}SKIPPED${NC}: Matter YAML Schema (--quick mode)"
fi

# ------------------------------------------------------------
# Check 6: .env is not tracked in git
# ------------------------------------------------------------
echo ""
echo -e "${BOLD}── Secret Files Not Tracked${NC}"
ENV_TRACKED=false
for secret_file in .env tokens.json oauth_state.json; do
  if git ls-files --error-unmatch "$secret_file" 2>/dev/null; then
    echo -e "${RED}FAIL${NC}: $secret_file is tracked in git"
    OVERALL_STATUS=1
    ENV_TRACKED=true
  fi
done
if [ "$ENV_TRACKED" = false ]; then
  echo -e "${GREEN}PASSED${NC}: No secret files tracked in git"
fi

# ------------------------------------------------------------
# Check 7: MCP server scripts exist
# ------------------------------------------------------------
echo ""
echo -e "${BOLD}── MCP Server Scripts Present${NC}"
MCP_OK=true
for mcp_script in scripts/gmail_mcp_server.py scripts/sharepoint_mcp_server.py; do
  if [ ! -f "$mcp_script" ]; then
    echo -e "${RED}FAIL${NC}: Missing $mcp_script"
    OVERALL_STATUS=1
    MCP_OK=false
  fi
done
if [ "$MCP_OK" = true ]; then
  echo -e "${GREEN}PASSED${NC}: MCP server scripts present"
fi

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
echo ""
echo "========================================"
if [ $OVERALL_STATUS -eq 0 ]; then
  if [ $WARN_STATUS -eq 0 ]; then
    echo -e "${GREEN}HEALTH CHECK PASSED${NC}"
  else
    echo -e "${YELLOW}HEALTH CHECK PASSED WITH WARNINGS${NC}"
  fi
else
  echo -e "${RED}HEALTH CHECK FAILED${NC} — see errors above"
fi
echo "========================================"
exit $OVERALL_STATUS

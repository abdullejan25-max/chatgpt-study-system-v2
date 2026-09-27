# Phase 4 Checkpoint — Architecture Rebaseline

## Implemented

- Adopted ADR-007: the active external Agent is the only intelligence layer; runtime/Core stays deterministic and provider-client-free.
- Kept MCP transport-specific schemas and error projection outside Core/Gateway. stdio MCP is the local reference transport; remote MCP remains an optional future transport.
- Documented that Tunnel and Responses API are not Core dependencies or phase exit gates.
- Added architecture regression coverage over runtime imports/dependencies, with positive fixtures to ensure normal HTTP and test-only references do not cause false positives.

## Verification

- Phase 4 full regression: `152 passed, 3 skipped`.
- Skips at this checkpoint were the host's symlink restriction and the two explicitly opt-in real-QMD smoke tests.
- Phase 3 read-only Gateway, QMD, and MCP regression remained covered by the suite.

## Decision and limitation

- Static dependency checks are regression guardrails, not a proof against indirect/dynamic model invocation; runtime dependencies still require review.
- Local commits: `2a69328` and test-coverage follow-up `dcbe931`.

# P12 Obsidian Generated Writer Design

## Goal and scope

Add a local, explicitly invoked writer for the existing in-memory Obsidian projection. The writer prepares deterministic rebuild and cleanup behavior for O8 using synthetic data and temporary directories. It does not select a real Vault, read Gateway data, or run during normal application startup.

## Ownership boundary

The caller must pass the dedicated `V2Projection` directory. The writer owns only files listed in a versioned manifest inside that directory. On first use, the directory must be new or empty. On later use, the writer may replace previously listed generated files and remove stale files listed by the previous manifest. It preserves unknown files and directories, never recursively removes a directory, and never follows symlinks. A malformed manifest or unsafe path aborts before mutation.

## Data flow

`ProjectionSnapshot` → existing deterministic in-memory renderer → explicit `write_projection(files, projection_dir)` call → generated Markdown plus manifest. The writer receives rendered strings only; there is no Gateway, database, or source-file dependency. Study remains outside the generated directory.

## Failure behavior

Reject absolute paths, drive prefixes, backslashes, empty/dot/traversal path segments, reserved manifest collisions, symlink components, and non-empty unowned first-use directories. Validate all proposed paths and the existing manifest before writing. Write each generated file through a sibling temporary file and replace it atomically; publish the new manifest last. Preserve unknown content. If an operation fails, raise a fixed-message writer error without echoing paths or content. A partial update can be safely rerun because the previous manifest remains authoritative until the new manifest is published.

## Verification

Temporary-directory tests cover first write, deterministic repeat, stale generated-file removal, unknown-file preservation, path traversal, malformed manifests, symlinks where supported, and manifest-last behavior under a simulated replacement failure. Tests use only synthetic Markdown. A real Vault, GUI, and P12 release gates remain outside this design.

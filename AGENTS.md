# Working on Bifoil Language

Read [README.md](README.md) for this repository's intended role and current status. This is a standalone repository
root, not a dependency on an adjacent checkout. Parent foundation instructions apply when present; this file preserves
the essential context for a future independent clone. The user's latest instructions take precedence.

## Project direction

The specification and conformance examples for Bifoil, a planned ChoiceScript-compatible superset language.

This repository defines the language. Compiler implementation belongs in bifoil-compiler; execution belongs in
bifoil-runtime.

The foundation's broader goal is a FOSS ecosystem comprising a ChoiceScript-compatible superset language, shared
language services, editor integrations, a toolchain, libraries, and potentially a standalone studio. This root contains
provisional steering/specification documents. The initial compiler/runtime slice is implemented; full-spec
implementation is now authorized in the separate repositories. Human readability, maintainability, and cleanup of
unneeded task-generated files are required. implementation-status.md records tested paths and unfinished work.
Existing Bifoil ChoiceScript code remains in its own repository.

## Shared preferences

- Use Bifoil Foundation branding and **Chinay** as the public maintainer identity. Keep local account names and personal
  filesystem paths out of public documentation and identifiers.
- Preserve independence from Choice of Games and upstream ChoiceScript, with separate licenses and provenance for
  third-party material. Do not invent legal status or transfer copyright to an assumed entity.
- Use pnpm for TypeScript work and the Gradle wrapper for Kotlin when those stacks are selected. Use system-installed
  **uv** for Python. Prefer idiomatic code, including multiline Kotlin statements.
- Where Prettier is adopted, preserve the founder's intentional `printWidth: 120` and use defaults otherwise. Add
  plugins only for formats the repository actually contains.
- Keep builds independent of sibling checkouts and chat workspaces. Reuse components through explicit, versioned
  interfaces or dependencies rather than silently copying or duplicating semantics.
- Use `git mv` for tracked moves, preserve unrelated edits, and follow the user's commit/signing workflow.
- Keep public guides separate from regression inputs and private reports. Use original minimal examples; do not copy
  externally supplied game sources or private corpus identities into the repository.
- Keep local agent records under ignored `.codex/` and development reports under ignored `.bifoil/development/`.
- Limit generated artifacts and large downloads to the task's needs. Validate relevant behavior and report actual
  results without claiming that a scaffold, build, or one-platform check proves release readiness.

The foundation's existing release and acceptance deferrals still apply unless the user changes their scope. Creating
this root does not publish it, select a license, authorize a release, or begin implementation of unspecified features.

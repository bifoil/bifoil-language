# Bifoil Language

The specification and conformance examples for Bifoil, a planned ChoiceScript-compatible superset language.

A Bifoil Foundation project maintained by **Chinay**. This repository contains the provisional design and review record.
The first compiler/runtime slice is implemented in its separate public repositories. No release is established.

## Intended scope

- Define syntax, semantics, compatibility expectations, and extension behavior.
- Maintain original examples and a conformance corpus that implementations can share.

## Design documents

- [Language steering](language-steering.md) records accepted decisions, stable IDs, source notes, and open details.
- [Provisional specification](language-specification-draft.md) organizes the selected language and compiler contracts.
- [Implementation status](implementation-status.md) links the first supported profile, interface, and validation
  results.

Continue specification work from the draft's
[completion sequence](language-specification-draft.md#completion-sequence) and
[review cases](language-specification-draft.md#review-cases-with-outcomes-already-determined-by-steering).

## Boundaries

This repository defines the language. Compiler implementation belongs in bifoil-compiler; execution belongs in
bifoil-runtime.

Repository boundaries are an initial organizational plan and can be revised when the language and integration contracts
are defined. No source has been extracted from the existing Bifoil ChoiceScript project.

## Status and next decisions

A native Rust compiler and JavaScript runtime implement a growing development profile. Full-spec implementation is
authorized, with human readability, maintainability, and cleanup required. Full-language
conformance, legacy bridges, wider platform acceptance, and releases remain unfinished. The design documents retain
accepted features beyond that slice and explicitly mark unresolved details.

Bifoil is independent of Choice of Games and upstream ChoiceScript. Any future use of upstream material must preserve
its applicable licenses and notices.

## Sonar analysis

[SonarQube Cloud](https://sonarcloud.io/dashboard?id=bifoil_bifoil-language) analyzes this public repository.
[Scanner settings](sonar-project.properties) separate original production sources from tests. Run the standard
`sonar-scanner` with `SONAR_TOKEN` supplied through the environment; never save a token in source or command arguments.
Scanner output stays under ignored `.bifoil/development/sonar/`. Use scanner-based analysis with automatic analysis
disabled for this project. A completed analysis and its quality gate are separate from passing local tests.

Sonar checks the Python validation tools. It does not understand `.bfl` semantics; language acceptance remains the
responsibility of the metadata validator and native conformance runner.

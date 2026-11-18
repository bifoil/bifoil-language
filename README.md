# Bifoil Language

The specification and conformance examples for Bifoil, a planned ChoiceScript-compatible superset language.

A Bifoil Foundation project maintained by **Chinay**. This repository contains the provisional design and review record.
The first compiler/runtime slice is implemented in its separate public repositories. No release is established.

## Intended scope

- Define syntax, semantics, compatibility expectations, and extension behavior.
- Maintain original examples and a conformance corpus that implementations can share.

## Design documents

- [Language steering](language-steering.md) records accepted decisions, stable IDs, source notes, and open details.
- [Accepted clarifications](accepted-clarifications.md) records comparison views, option filtering, copy collisions,
  nominal map-key conversion, Unit-context returns, and shared module values.
- [Equality through comparison views](comparison-view-equality.md) describes the v3 instruction and retained type
  identities.
- [Clarification conformance](clarification-conformance.md) maps those rules to regression projects and implementation
  boundaries.
- [Provisional specification](language-specification-draft.md) organizes the selected language and compiler contracts.
- [Development source grammar](development-source-grammar.md) defines implemented lexical, layout, declaration, type,
  expression, and prose forms, with their precedence and profile restrictions.
- [Compatibility contract](compatibility-contract.md) defines supported format/profile combinations, producer
  obligations, cache keys, package identities, and checkpoint rejection rules.
- [Implementation status](implementation-status.md) links the first supported profile, interface, and validation
  results.
- [Capability derivation](capability-semantics.md) defines automatic equality/key eligibility and symbolic proofs
  through recursive generic and projected field graphs.
- [Binding and flow proofs](binding-flow-semantics.md) defines delayed assignment, recursive capture requirements,
  publication boundaries, and conservative refinement invalidation.
- [Collection graph interactions](conformance/collection-graph-interactions.md) combines source-free cyclic data, keys,
  copies, projections, runtime identities, and repeated checkpoints.
- [Computability review](computability.md) gives a tape-simulation argument and separates semantic completeness from
  finite implementation guards.
- [Complete implementation checklist](language-implementation-checklist.md) tracks every steering decision, remaining
  engineering work, and full-language acceptance gates.

Continue specification work from the draft's [completion sequence](language-specification-draft.md#completion-sequence)
and [review cases](language-specification-draft.md#review-cases-with-outcomes-already-determined-by-steering).

## Boundaries

This repository defines the language. Compiler implementation belongs in bifoil-compiler; execution belongs in
bifoil-runtime.

Repository boundaries are an initial organizational plan and can be revised when the language and integration contracts
are defined. No source has been extracted from the existing Bifoil ChoiceScript project.

## Status and next decisions

A native Rust compiler and JavaScript runtime implement a growing development profile. Full-spec implementation is
authorized, with human readability, maintainability, and cleanup required. Full-language conformance, legacy bridges,
wider platform acceptance, and releases remain unfinished. The design documents retain accepted features beyond that
slice and explicitly mark unresolved details.

Bifoil is independent of Choice of Games and upstream ChoiceScript. Any future use of upstream material must preserve
its applicable licenses and notices.

## Sonar analysis

The Sonar workflow requires at least **80% coverage in every production source file**, using covered executable lines
and condition outcomes from the configured reports. The comparison uses exact counts; project averages and rounded
percentages cannot hide a failing file. Missing coverage or test evidence fails the check. Files without executable
Sonar coverage locations retain their separately verified compilation or command-test evidence and report `N/A`.
This per-file floor is additional to the 100% overall/new condition requirement and the existing issue-count limits.

[SonarQube Cloud](https://sonarcloud.io/dashboard?id=bifoil_bifoil-language) analyzes this public repository. [Scanner
settings](sonar-project.properties) separate original production sources from tests. Run the standard `sonar-scanner`
with `SONAR_TOKEN` supplied through the environment; never save a token in source or command arguments. Scanner output
stays under ignored `.bifoil/development/sonar/`. Use scanner-based analysis with automatic analysis disabled for this
project. A completed analysis and its quality gate are separate from passing local tests.

Sonar checks the Python validation tools. It does not understand `.bfl` semantics; language acceptance remains the
responsibility of the metadata validator and native conformance runner.

Generate portable Python coverage for the validator before scanning:

```sh
uv run --no-project --with coverage python -m coverage run -m unittest discover -s tools -p test_validate_conformance.py
uv run --no-project --with coverage python -m coverage xml
```

For the five validator regressions, measured statement coverage is 92.77% and branch coverage is 91.18%. Coverage.py
displays 92% combined coverage. These figures describe the Python validator, not execution of Bifoil cases.

[Text and comparison contracts](text-semantics.md) specify triple-string whitespace, primitive formatting, explicit
conversions, cycle-aware diagnostic rendering, and ordinary repeated-comparison grouping.

[Collection operations and copy timing](collection-operations.md) defines the built-in update/copy signatures, Entry
snapshots, dynamic bounds checks, and receiver-first generated copy behavior.

[Pinned progression membership](progression-membership.md) records the immutable Kotlin source reference, search-index
failures, constant-work implementation, and terminal iteration checks.

[Equality and nullable results](equality-and-nullability.md) defines ordinary comparison and fallback typing, with
source-free positive and rejection controls.

[Modules, aliases, and shared storage](modules-and-names.md) specifies module interfaces, enum lookup, and visit
storage.

[Projection views](projection-semantics.md) defines sound reads and writes through hidden arguments.


The [bounds and inference contract](type-constraints.md) connects recursive interfaces, automatic capabilities,
subtyping versus conversions, compatible joins, and conservative termination/failure. The [module/name
contract](modules-and-names.md) specifies separate type/value namespaces, distinct exports, and nested persistent shared
storage.


The [prose contract](prose-semantics.md) connects directive/callable modes, code-mode interpolation, separator
ownership, newline escapes, source formatting, and source-free suspended output.


The [source-selection contract](file-selection.md) describes manifest/explicit command selection without claiming every
file with the shared .bfl extension.


The [function interaction contract](function-contracts.md) connects result inference, guard coverage, overload ranking,
and Unit-context anonymous returns, including the selected retained-argument covariance rule.

The [specification resolution index](specification-contracts.md) distinguishes current focused contracts from the
historical open-detail notes retained in the steering record and consolidated draft.

The [text contract](text-semantics.md#scalar-validation-and-limits) defines development runtime String admission,
checked result assembly, Unicode diagnostics, and rejection behavior at host input/output boundaries.

[Legacy compatibility](legacy-compatibility.md) enumerates the pinned native command surface and the built-in bridge's
prepared-input, value-validation, rendering, and platform-service boundaries.

The [large narrative measurements](../bifoil-compiler/NARRATIVE_CAPACITY.md) retain explicit workload dimensions,
Windows-mount and Linux-filesystem results, failed edits, and separate aggregate-resource qualification.

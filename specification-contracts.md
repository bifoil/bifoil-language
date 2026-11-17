# Specification resolution index

Updated: 2026-11-05.

The user's latest direct instruction takes precedence. The [steering record](language-steering.md) preserves all
305 decision IDs and their historical wording. The [accepted clarifications](accepted-clarifications.md), later dated
steering additions, and focused contracts below supply their completed rules. Earlier notes saying a detail is open
remain historical wherever a later clarification or contract resolves it. A working implementation alone does not
approve an observable scope change.

The [consolidated draft](language-specification-draft.md) retains the original drafting sequence and review examples.
Use this index to read its earlier incomplete notes alongside current contracts. The [implementation
checklist](language-implementation-checklist.md) records completion separately; contract text, executable checks,
resource qualification, production-host acceptance, and release authorization are different obligations.

## Current focused contracts

- [Source grammar](development-source-grammar.md): lexical forms, layout, declarations, expressions, patterns,
  embedded directives, precedence, and formatter boundaries for the development profile.
- [File selection](file-selection.md): manifests, explicit inputs, .bfl selection, and foreign-file preservation.
- [Modules and names](modules-and-names.md): separate type/value namespaces, distinct exported names, aliases,
  imports, declaration placement, and eagerly initialized nested shared storage.
- [Bindings and flow](binding-flow-semantics.md): definite assignment, recursive/indirect calls, captures, effects,
  narrowing, suspension, and conservative rejection where safety is unproved.
- [Functions](function-contracts.md): compatible result joins, overload ordering, expected function types,
  Unit-context returns, guards, and argument inference retained under a covariant expected result.
- [Type constraints](type-constraints.md): genuine subtyping versus conversions, capability derivation, bounds,
  inference, recursive interfaces, and conservative solver termination.
- [Projection views](projection-semantics.md): safe upper reads and lower writes, hidden owner arguments, and
  preservation of retained type identity.
- [Equality and nullable results](equality-and-nullability.md): ordinary operand eligibility, structural equality,
  cyclic comparison, nullable results, and lazy fallback joins.
- [Comparison views](comparison-view-equality.md): the user's declared-view rule for typed structural exact equality.
- [Text](text-semantics.md): Unicode scalars, triple-string whitespace, conversions, rendering, malformed external
  input, per-value development limits, and checked combined-result admission.
- [Collection operations](collection-operations.md): Entry, methods, copies, map-key reconstruction, evaluation
  order, bounds-check timing, and current-field copy defaults.
- [Progressions](progression-membership.md): the pinned Kotlin behavior, approved constant-time equivalent,
  signed-index failure, endpoint iteration, and checked receiver views.
- [Prose](prose-semantics.md): embedded executable suites, callable output contexts, interpolation, explicit line
  breaks, physical source positions, and paragraph separator ownership.
- [Compatibility](compatibility-contract.md): current module v6 producers, runtime profiles, package layouts,
  same-build checkpoint rejection, and independently compiled interfaces.
- [Legacy compatibility](legacy-compatibility.md): the pinned command inventory, explicit primitive/enum bridges,
  native interaction snapshots, transfers, and remaining host/service acceptance boundaries.
- [Computability](computability.md): language-level Turing completeness distinguished from finite implementation
  admission guards, and the unselected native-target/self-hosting direction.

## Outstanding observable boundary

Composite typed legacy bridge ownership is awaiting a direct user selection. Consider passing a mutable list with
one element to native code that changes that element. Copying the reachable graph leaves the original list unchanged
unless an explicit writeback occurs. Sharing checked handles makes that mutation observable through the original
Bifoil alias. Both also require precise alias, cycle, type-check, and persistence rules. The existing primitive/enum
bridge profile does not silently select either composite policy. CON-17 and LEG-10 remain unchecked.

## Outstanding engineering and acceptance work

The full resource protocol still requires a qualified process-wide metric, measurement/enforcement method, reference
environment, and representative workload envelope. The selected requirements remain below 250,000,000 bytes of
aggregate compiler/helper memory and below ten seconds for incremental end-to-end builds. Clean builds scale with
input. [Compiler resource observations](../bifoil-compiler/RESOURCES.md) keep measured workloads separate from full
capacity acceptance. A configured admission limit, a sampled RSS value, or a rejected build cannot establish success.

The outstanding memory choice has a concrete distinction: a job with 80 MB of resident process memory and 400 MB
of unmapped filesystem cache satisfies a process-memory interpretation and fails a cache-inclusive interpretation.
Neither a low process peak nor successful disk-backed compilation settles that language contract. The direct user
selection is pending; the existing numeric budget is unchanged.

The development grammar identifies its profile boundaries explicitly. Complete whole-language review, unsupported
legacy/platform services, production persistence/host acceptance, all claimed compiler platforms, and the remaining
checklist obligations retain their individual gates. None is waived by this index. Future native story binaries,
self-hosting, general inheritance, and release commitments remain unselected.

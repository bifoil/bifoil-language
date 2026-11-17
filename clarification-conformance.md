# Accepted clarification conformance

The [accepted clarification rules](accepted-clarifications.md) define source behavior. Their original decision IDs
remain in [the steering ledger](conformance/steering.json). These original regression projects exercise the selected
rules through the native compiler and runtime; they do not establish whole-language or release acceptance.

## Anonymous Unit returns

[The source-free callback project](conformance/cases/unit-early-discard-source-free-checkpoint/helpers.bfl) checks that
value-bearing early returns and final expressions evaluate once, discard their results, and return Unit. Nested named
and anonymous functions keep their own result types. A suspending return value crosses a prepared input wait, and the
conformance executor restores that wait in a fresh host before selecting an option.

[The capture project](conformance/cases/unit-discarded-capture-source-free/helpers.bfl) returns a Unit callback that
creates and discards an unread closure. Its uninitialized captured cell is retained without being read or published
as a result. An expression-position return has the same boundary. Invalid counterparts reject actual uninitialized
reads, suspension in ordinary callbacks, and non-Unit returns from named Unit functions. The native regression suite
also checks that invoking a closure still requires its captured reads to be safe.

The compiler keeps complete lexical names for runtime cell retention and a separate execution summary for the Unit
callback's reads and publications. Discarding a direct closure creation does not erase effects from calls,
constructors, or other expressions evaluated to produce a discarded result.

## Choice preparation

[The preparation project](conformance/cases/once-filter-effects-source-free-checkpoint/helpers.bfl) records each
visibility, enabling, and label expression in order. It covers visible, hidden, disabled, and consumed options. A
consumed once option's visibility would fail if evaluated again; later visits skip it along with its enabling and
label work. Disabled visible options prepare labels, while hidden options skip enabling and labels. The fresh-host
checkpoint path preserves the prepared snapshot and story-wide consumption history without replay.

## Generated members and module values

[The clarification index](conformance/clarifications.json) pairs copy-member collision errors with a case-sensitive
positive control. Public/private fields, methods, and overload attempts cannot replace the generated copy member.
Unrelated names and a module-level function named copy retain their ordinary namespaces.

Module-level ordinary val/var declarations are rejected, including exported and delayed declarations.
[The library project](conformance/cases/module-shared-library-source-free-checkpoint/helpers.bfl) uses shared
initializers, two scene modules, independently compiled library code, and restored input waits. Initialization runs
once, shared mutation survives visits, and ordinary local bindings remain available. Typed legacy-storage declarations
retain their separate interface role.

## Nominal map keys

[The conversion project](conformance/cases/nominal-map-key-copy-checkpoint/main.bfl) combines nominal key conversion,
scalar value widening, family copying, nullable lifting, and checkpoint restoration. Rebuilding retains key instances
and their construction types, preserves insertion order, and gives each copied container independent storage.
[The generic project](conformance/cases/nominal-map-key-generic-bound-source-free/helpers.bfl) checks nominal map-key
bounds and inference alongside contravariant callback constraints. Invalid counterparts retain mutable invariance and
reject implicit function adapters that would need map reconstruction.

[Runtime conversion tests](../bifoil-runtime/test/conversions.test.mjs) exercise both implicit reconstruction and
explicit copies with changed key types. They verify retained key aliases, duplicate searches, and rejection of a
duplicate before attempting that entry's value conversion. Copies with unchanged validated key types retain their
existing fast path.

## Declared-view exact comparison

[Comparison-view equality](comparison-view-equality.md) documents the v3 instruction, retained construction identities,
recursive comparison contexts, and original source-free/checkpoint cases. The selected comparison-view contract now
has an explicit execution path; whole-profile qualification remains separate from focused regression results.

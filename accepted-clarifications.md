# Clarifications accepted on 2026-11-04

These rules resolve the six observable-contract questions answered by the user after the original steering
questionnaire. Existing decision IDs remain stable. Their source record is the dated clarification section in [language
steering](language-steering.md#clarifications-accepted-2026-11-04); implementation evidence remains in the
[checklist](language-implementation-checklist.md). [Conformance details](clarification-conformance.md) describe the
implemented paths and the remaining comparison-view work.

## Exact equality and comparison views

E29-E30 use the declared types of the evaluated operands as the comparison views for composite exact equality.
Flow-proven refinements may contribute the operand's static type at its evaluation point. Comparing values does not
change their retained construction types, aliases, or later type-test/cast behavior.

Match collection families and comparison-view arguments, or nominal comparison types, before recursively comparing
eligible contents. Nullable wrappers do not distinguish present values from the corresponding non-null comparison under
E29; two nulls remain equal. Primitive values retain exact primitive-kind comparison without numeric or Char widening.
Different active sum variants remain unequal under U22.

Recursive fields and container positions use the types exposed by their comparison views. A hidden or universal position
does not erase the actual primitive kinds of the contained values. Equality eligibility still requires the existing
static proof; a broad view alone does not supply an Equatable capability. Eligible cyclic comparisons remain cycle-safe,
and alias-sharing layout does not determine equality.

For example, this Box has an Int field, so its equality eligibility is independent of its covariant parameter:

```bifoil
data class Box<out T>:
    val number: Int
scene start():
    val original = Box<Int>(3)
    val viewed: Box<Any> = original
    val constructed = Box<Any>(3)
    prose:
        ${viewed === constructed}
        ${viewed is Box<Int>}
        ${constructed is Box<Int>}
```

The results are true, true, and false respectively. The exact comparison uses Box<Any> on both sides; subsequent type
tests still observe the retained construction identities. Comparing original directly with constructed instead uses
different comparison-view arguments and is false.

Empty containers follow the same rule; their contents do not choose a replacement runtime argument:

```bifoil
scene start():
    val original: List<Int> = []
    val viewed: List<Int?> = original
    val constructed: List<Int?> = []
    prose:
        ${viewed === constructed}
        ${viewed is List<Int>}
        ${constructed is List<Int>}
```

These results are again true, true, and false. The view is not an implicit element conversion or a container copy.
Required comparison context must cross any compiled-module, suspension, or checkpoint boundary without replay. Changes
to required wire information follow the [compatibility contract](compatibility-contract.md).

## Consumed once options

T14 filters a consumed once option before running any of its preparation expressions. Skip visibility, enabling, and
label interpolation entirely for that option. For each remaining option, retain source order and evaluate visibility
first, then enabling and label when visible. A visible disabled option still prepares its label under the existing
rules. Store the resulting snapshot until selection.

Consumption occurs on selection and is story-wide for that source option site. Later function calls and scene visits
share its history. Saving and restoring a prepared input wait preserves that history and its current snapshot, without
rerunning completed preparation. A consumed option cannot trigger a later visibility error or mutate state through its
skipped preparation expressions.

## Reserved generated copy member

U29 reserves the data-member name copy for the generated shallow-copy operation. A field or method named copy is a
compile error, including private members and overload attempts. Visibility does not hide a collision with a generated
member. The existing case-sensitive naming rule applies.

The restriction concerns that generated member namespace. Other names and ordinary no-shadowing rules keep their
existing scope. Generated copy arguments still use the selected calling rules; omitted fields retain their current
values and referenced fields retain their ordinary sharing semantics. Separate evaluation-timing obligations remain in
force.

## Nominal Map-key conversion

D22 additionally permits immutable Map key types to widen through genuine nominal subtyping. Convert by rebuilding an
independent map with the requested key type, preserving entry order and checking duplicate keys. For example,
Map<Outcome.Success, Int> may convert to Map<Outcome, Int> when both key types meet StableKey requirements.

Map key positions remain invariant for genuine subtyping under D30. This conversion does not create a no-copy subtype
relationship between the two Map types. Same-family mutable type arguments remain invariant. Previously approved
container-family copies may combine with the key conversion, preserving the existing conversion timing and rank
categories. Ordinary Int/Float and Char/String conversion rules are unchanged.

Retain the values' nominal construction identities while exposing the requested key type. Check each converted key for
duplication before converting its value. Reject a provable duplicate at compile time where the ordinary constant rules
establish it; otherwise report a runtime error. Do not silently drop or replace an entry during conversion. Rebuilding
the container does not recursively copy referenced data instances or freeze mutable objects.

These rules apply through the already selected nullable lifting and recursive immutable conversion positions. They do
not permit mutable-to-mutable widening, arbitrary Any inference, or implicit function-signature adapters. Explicit
expected types and supplied facts retain their existing roles in generic inference.

## Unit-context anonymous returns

F34 applies to both the final expression and value-bearing early returns when constructing an anonymous function with an
expected Unit result. Evaluate the return expression under ordinary type, effect, and evaluation-order rules; discard
its value and return Unit. Completed effects still occur exactly once. A nested function or lambda retains its own
return boundary and expected result.

```bifoil
scene start():
    val callback: (Int) -> Unit = (number: Int) =>:
        if number > 0:
            return number * 2
        number - 1
    callback(3)
```

The early return exits callback with Unit. It does not change a caller binding or convert an existing function value to
a different signature. A suspending return expression still requires a suspending anonymous function. A discarded value
must be a valid expression; discarded closure creation does not invoke that closure or publish it as the return value.
Named functions keep their existing return-type checks.

## Module-level values

M01 requires shared for every ordinary file/module-level val or var value. Library initialization happens through
non-suspending shared initializers, in the existing dependency order and once per new playthrough. A load restores that
state without rerunning the initializers.

```bifoil
shared val title: String = "An original story"
shared var visits: Int = 0
```

Ordinary val/var declarations remain available inside scene visits, functions, and their lexical blocks. Instance fields
and typed declarations of external legacy storage retain their separate roles; they do not create an ordinary
library-initialization form. Existing functions, types, aliases, imports, and exports remain declarations.

The subsequent shared-placement clarification extends storage to lexical bodies. The [module/name
contract](modules-and-names.md) defines explicit forwarding and modifiers. Illustrative local sketches do not introduce
ordinary file-level initialization.


## Separate namespaces and unique exports, 2026-11-05

The user selected separate type/value namespaces: a type alias and an ordinary value may share a visible name.
Same-namespace no-shadowing remains in force. A module must use distinct exported names for distinct entities;
co-exporting an alias and a value under one name is a compile error.

## Nested shared storage, 2026-11-05

The user selected nested shared declarations with lexical visibility and initialization before the first scene.
Initializers cannot use enclosing parameters, ordinary locals, or function type parameters. Receivers and class type
parameters are equally unavailable because initialization precedes any instance/call. The [storage
contract](modules-and-names.md#shared-state-and-visits) defines source-site cells, lexical aliases, ordering, and
restored state. This supersedes M14's pending placement note without removing its decision history.

## Retained generic arguments clarification (2026-11-05)

The user selected retaining argument-inferred Int for covariant Box<out T> when box(4) is used with expected Box<Any>.
Expose the broader view by covariance; the retained runtime type remains Box<Int>, so its type test is true. Expected
types still supply missing arguments and constrain invariant or conversion-requiring cases. The [function
contract](function-contracts.md#argument-inference-and-expected-result-views) specifies the combined rule. This direct
clarification resolves the previously recorded distinguishing prototype without changing the historical decision rows.


## Copied legacy value graphs

On 2026-11-05 the user selected copying the reachable graph at typed legacy boundaries. Preserve aliases and cycles
within each transferred graph. Native mutations affect Bifoil only through an explicitly returned or assigned value.
The [value-graph contract](legacy-value-graphs.md) defines the boundary obligations; implementation remains a separate
checklist gate. This resolves the ownership choice in CON-17 without rewriting historical decision rows.

## Compiler resident-memory budget

On 2026-11-05 the user selected aggregate resident process memory for the strict 250,000,000-byte compiler/helper
budget. Include native allocations, stacks, and mapped libraries; exclude unmapped OS filesystem caches. Use kernel
peak accounting and a conservative continuous limit. The [resource contract](compiler-resource-contract.md) separates
that selected quantity from workload acceptance and other host-platform enforcement. No earlier failed job becomes a
successful compilation because the metric is now selected.

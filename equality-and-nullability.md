# Equality and nullable results

This contract completes ordinary comparison eligibility and nullable fallback result typing from E03, E28-E34,
D08, U06, U22, and B11-B19. It applies the selected compatible-type joins and conversions; transparent aliases add no
runtime identity. Capability derivation and exact comparison views retain their separate linked contracts.

## Static eligibility

Comparing either operand with null is permitted, including when the other value is a function or has unknown equality
capability. Otherwise both operand types must establish Equatable. A favorable current value does not establish that
proof for Any, an unconstrained parameter, a function, or a composite containing such an unknown position.

Ordinary equality requires compatible operand types. Compatible scalar pairs include Int/Float and Char/String.
Nullable forms use the corresponding present-value relationship. A genuine subtype relationship or a compatible
common type also establishes compatibility. Generic bounds may establish a shared value family, while a capability
marker alone does not make unrelated families compatible.

Collections of the same kind compare when corresponding argument types have compatible joins and both complete
types support equality. Mutable and immutable forms may compare with each other; this comparison does not authorize
mutable assignment covariance. Thus List<Int> and MutableList<Float>, or MutableList<Int> and MutableList<Float>,
can compare numerically without converting either container. A List and Set remain unrelated ordinary operands.

Data instances retain nominal declaration identity. Equal-looking fields do not make separately declared classes
compatible. Generic instantiations must satisfy the selected subtype/common-type relationships; scalar widening does
not become nominal generic variance. A data type's fields must all support equality, including private and mutable
fields. For a sum viewed through its parent, every variant's payload must qualify. An individual variant uses its own
payload capability. These rules follow [automatic capability derivation](capability-semantics.md).

Exact comparison permits otherwise unrelated eligible types and compares without widening or copying. Different
primitive kinds are unequal, so Int 3 differs exactly from Float 3 and Char 'a' differs exactly from String "a".
Unknown capability and function-value comparisons remain errors. Nulls compare independently of their annotations;
a present nullable operand uses its contained value. Composite exact comparison follows the approved
[declared-view rules](comparison-view-equality.md), retaining construction identities for later tests and casts.

## Value comparison

Ordinary numeric and text widening is observational: matching Int/Float numeric values and Char/String scalar
sequences compare equal without replacing their stored values. Boolean, Unit, enums, and other eligible values retain
their value rules. Strings preserve scalar sequences without normalization.

- Lists compare element counts and corresponding elements in order.
- Sets compare equal members independent of insertion order, with one matching member per candidate.
- Maps compare equal keys and their corresponding values independent of insertion order.
- Entries compare their key and value.
- Data instances compare corresponding fields. Different active sum variants are unequal; matching variants compare
  payloads. Equality does not call authored methods.

The operation reads current referenced fields. Capturing the left operand before evaluating the right retains that
instance rather than snapshotting its fields. If the right operand mutates it, comparison observes that update after
the right operand completes. Only operand evaluation may suspend; comparison itself does not call story code.
The negated operators invert the completed Boolean result and preserve evaluation failures.

Eligible cyclic graphs compare by tracking operand pairs within that comparison. Revisiting a pair terminates that
recursive step, while every reached field and element must still match. A one-node cycle can equal a two-node cycle;
shared-reference layout does not decide equality. Failed unordered candidate trials cannot leave facts that falsely
prove later candidates. Pair state is local to the operation, so later mutation cannot reuse an earlier result.
Explicit work frames keep graph depth off the host call stack. Exact comparisons additionally retain the declared
view in pair identities.

## Nullable fallback typing

For left ?: right, evaluate left once. A present value selects its contained value; null selects right, evaluated only
then. False, zero, and empty text remain present values. Repeated fallback associates right to left.

Without a needed explicit result context, infer the compatible common type of the left operand's non-null type and
the right result. A literal null on the left contributes only the right type. Nothing contributes no result on a
transferring path. Supported joins include scalar/nullable widening, genuine subtyping, and approved widening through
immutable containers. These examples infer Float, String, and List<Float>:

~~~bifoil
fun number(value: Int?, fallback: Float) = value ?: fallback
fun text(value: Char?, fallback: String) = value ?: fallback
fun items(value: List<Int>?, fallback: List<Float>) = value ?: fallback
~~~

Inference does not invent Any or copy between container families to manufacture a common type. When that ordinary
join is unavailable, an explicit expected result type may establish the result if both the present-left type and
right result can convert to it under already approved rules:

~~~bifoil
fun frozen(value: MutableList<Int>?, fallback: List<Float>) -> List<Float> = value ?: fallback
fun broad(value: Int?, fallback: String) -> Any = value ?: fallback
~~~

The selected operand converts when that path executes. A required family copy produces an independent outer
container; referenced descendants retain the approved shallow semantics. A skipped fallback performs no effects,
allocation, or conversion. An unsuitable expected Boolean does not accept either example. Without the annotations,
both examples fail rather than infer those extra operations.

An expected result can guide a contextual fallback literal, callable, or overloaded reference under its existing
rules. It does not change explicit arguments, generic ownership, mutable invariance, or function-adapter restrictions.
Both paths still require valid syntax, types, initialization, and effects, even when one is known to be skipped.

## Other nullable operations

Safe member access, calls, and indexing evaluate the receiver/callable once. Null yields null and skips argument,
index/key, and call evaluation. A present receiver follows its ordinary bounds and argument rules. Applying
nullability to an already nullable result flattens it; a map's missing value and stored null share the same result.
Safe function calls retain positional/variadic function-value interfaces and checked suspension permissions.

Postfix assertion evaluates once, reports a located runtime error for null, and yields the non-null type otherwise.
Approved nullable conversions preserve null and convert only a present value. Flow narrowing remains subject to
[binding, call, alias, and suspension proofs](binding-flow-semantics.md).

If selected evaluation suspends, saved state retains computed operands, callable/receiver identities, and temporary
conversions. Resumption continues without repeating completed evaluation or copying. This follows the existing
same-build input-checkpoint contract and does not add new save points.

## Evidence

The [original source-free cases](conformance/equality-nullability.json) combine ordinary and exact comparisons,
ordered and unordered collections, eligible cyclic data/sum payloads, mutation during a suspended right operand,
nullable scalar/immutable joins, contextual copies, lazy safe paths, and dynamic assertion failure. Each wait restores
into a fresh host. Paired rejections cover nominal and unrelated operands, hidden or function capabilities, inference
that would need copies or Any, invalid expected types, and statically checked skipped arguments/effects.

[Native regressions](../bifoil-compiler/src/tests/equality_contracts.rs) assert inferred signatures and corresponding
rejections. Existing [runtime equality tests](../bifoil-runtime/test/equality.test.mjs) exercise 6,000 nested unordered
values and failed-candidate isolation; [comparison-view tests](../bifoil-runtime/test/comparison-views.test.mjs) check
context-sensitive pairs, deep values, retained identities, and package/checkpoint boundaries. These tests do not
establish target-scale compiler resource compliance or production-host release acceptance.

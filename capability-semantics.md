# Capability derivation

This document defines automatic eligibility for `Equatable` and `StableKey` under G09-G10 and D12. It does not add
user-defined equality methods, general inheritance, or a reference-identity operator. Ordinary and exact comparison
retain their separate operand-compatibility and value rules.

## Eligibility judgments

Write `Q(T)` when values of static type T support structural equality and `K(T)` when that equality cannot change
while a value is stored as a set member or map key. `K(T)` entails `Q(T)`. Qualification depends on the checked type
and its complete field/payload graph, rather than a favorable current value or an author-supplied marker.

- Numeric, Boolean, String, Char, and Unit values have fixed value equality. Nullable application preserves the
  contained type's eligibility. Comparing a nullable value with null remains permitted independently of Q.
- Any, Any?, unconstrained hidden arguments, and function values do not establish Q. An unconstrained generic parameter
  can qualify only when its actual type or declared bounds establish the required capability.
- A list or set qualifies when its element type qualifies; a map or entry requires both key and value types to qualify.
  Mutable collection families may satisfy Q, but cannot satisfy K. Immutable containers satisfy K only when all
  contained
  types satisfy K; an immutable outer container does not freeze mutable descendants.
- A data declaration satisfies Q when every field type does. It satisfies K when all fields have fixed bindings and
  every field type satisfies K. Public/private visibility and constructor defaults do not hide mutable state from this
  analysis. Methods do not replace the selected field-based equality.
- A closed sum requires every variant's payload graph to qualify. Each variant separately uses its own fields. Plain
  enum constants have stable equality. Fixed payload bindings retain the mutability of referenced values.

Types must already be well formed. In particular, set elements and map keys satisfy K at construction. A projected
`Set<*>` or map key hides a checked key type; it does not erase that guarantee. A projected List element or map value
has no corresponding unconditional guarantee.

## Generic and projected requirements

A nominal declaration can have a conditional capability. For example, `Box<T>` with one fixed field of type T requires
Q(T) for equality and K(T) for stable-key use. Instantiation substitutes the supplied type arguments into those
requirements. Aliases do not create another capability identity.

For `Owner<*>`, a hidden parameter retains the guarantees of its declared bounds. Known sibling arguments are
substituted first. Hidden siblings keep distinct parameter identities so their own bounds remain available. An outer
parameter stays symbolic until its owning declaration is instantiated or the generic caller's bounds establish proof.
An unconstrained body must not permanently reject a property that a later concrete argument can establish.

A parameter's source constraints are conjunctive: every bound must hold. A capability proof may use any bound that is
sufficient. For example:

```bifoil
data class Inner<A, B, T> where T: A, T: B:
    val value: T

data class Outer<X, Y, Z>:
    val first: Inner<X, Y, *>
    val second: Inner<Y, Z, *>
```

`K(Outer<X, Y, Z>)` holds when `(K(X) OR K(Y)) AND (K(Y) OR K(Z))` holds. Either K(Y) alone, or K(X) together with K(Z),
suffices. Requiring every bound to establish K would reject valid types. Choosing only the first sufficient-looking
bound before substitution would lose other valid proofs. An unknown or mutable argument still cannot become stable
merely because one concrete hidden instance currently contains an Int.

A StableKey bound proves both capabilities. An Equatable bound proves Q alone. Bounds on ordinary types use their
existing qualification rules; scalar conversions and container copying do not become subtype bounds or proof adapters.

## Recursive graphs and termination

A declaration's capability is a monotone Boolean function of its generic arguments' capability facts. Recursive nominal
references retain declaration identity and those facts; they do not expand recursive source types into infinite trees.
The implementation queries only reached `(declaration, argument facts)` states. Equality and key stability have separate
state tables.

A newly reached nominal state begins eligible. Field and payload obstructions propagate until no reached state changes;
only then may the result enter the catalog's completed-state cache. Changed facts enqueue their recorded dependents;
unaffected completed states remain cached. An immutable cycle with no obstructing field can
qualify. A mutable or ineligible descendant invalidates every dependent state before results are retained. Provisional
success inside a cycle cannot escape as a final proof.

Hidden argument facts begin unproved. Repeatedly apply sufficient bounds until no additional fact is established.
Known argument facts remain fixed; a StableKey marker is a fact, while a circular payload dependency is not. Generic
parameter proof tracks active identities separately. Direct cyclic upper bounds remain invalid source.

Only reached argument-fact configurations are evaluated. Independent alternative bounds are tested directly; the
compiler does not enumerate every sufficient combination of them. A shared type graph is also visited once per
unchanged argument-fact context. Memoized physical-node identities do not survive their borrowed type graph or cross a
changed proof context.

There are finitely many argument-fact vectors per finite declaration. Nominal obstructions only accumulate, and hidden
proof facts only accumulate within each fixed context, so each query reaches a fixed point. Completed state caches are
invalidated with the owning declaration catalog. This is a termination argument, not a claim that all possible source
workloads have constant or linear complexity. Target-scale time and aggregate-memory acceptance remain separate.

## Implementation and evidence

The compiler separates [catalog-scoped capability state caching](../bifoil-compiler/src/declarations/capabilities.rs)
from [fixed-point queries and projected bound proofs](../bifoil-compiler/src/declarations/capabilities/query.rs).
[Native regressions](../bifoil-compiler/src/tests/projected_inputs.rs) cover every combination of three argument
stability facts, recursive nominal declarations, safe generic callers, and paired unstable controls.

The [source-free composition case](conformance/cases/projected-capability-compositions-source-free-checkpoint/main.bfl)
checks recursive data, sum payloads, duplicate stable keys, generic constraints, and restoration after source removal.
[Mutable equality](conformance/cases/projected-capability-composition-mutable-equality/main.bfl) remains available while
[mutable keys](conformance/cases/projected-capability-composition-mutable-key-error/main.bfl) and
[unknown key guarantees](conformance/cases/projected-capability-composition-unknown-key-error/main.bfl) are rejected.

The [wide source-free case](conformance/cases/projected-capability-wide-state-source-free-checkpoint/helpers.bfl)
contains 28 independent alternative-bound pairs in a small original declaration. Its client constructs a stable key,
removes the helper source before compilation, and preserves the resulting graph across a checkpoint. It guards against
materializing hundreds of millions of sufficient-bound combinations; it does not establish target-scale capacity.

The [long source-free rejection](conformance/cases/projected-capability-long-dependency-source-free-error/helpers.bfl)
propagates a terminal mutable field through 1,000 nominal declarations before the client attempts key construction.

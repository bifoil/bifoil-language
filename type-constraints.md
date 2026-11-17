# Bounds, capabilities, and generic inference

This contract combines definition-time bounds, capability derivation, genuine subtype relations, compatible joins, and
conservative inference. Finite development guards do not establish the required large-project capacity.

## Definitions and recursion

Check generic declarations against their written requirements even when unused. Unconstrained T can stand for nullable
types; T: Any requires non-null values. Equatable and StableKey are capabilities, not implicit non-null bounds. All
inline and repeated where requirements must hold after substituting the actual arguments.

Resolve declaration identities before checking complete bounds. Nominal recursive bounds such as Loop<T: Loop<T>> are
permitted; referring to an established nominal identity does not require expanding its fields indefinitely. Reject
direct/indirect cycles consisting only of parameter upper bounds, including nullable wrappers. Transparent aliases must
expand finitely; recursive structure must pass through a nominal data or sum declaration.

Mutually importing modules first establish provisional names, then resolve complete interfaces and bounds. Pending types
and incomplete constraints cannot escape into reusable artifacts. A recursive nominal alias can refer to its established
declaration identity. Unknown bounds, incorrect arity, and invalid instantiations remain errors even when the declaring
body is unused.

The [capability contract](capability-semantics.md) defines automatic finite-graph qualification and symbolic proofs.
Mutable values can satisfy Equatable without satisfying StableKey. StableKey additionally requires equality that cannot
change while stored. Nullable eligibility follows the contained type. An unbounded parameter cannot compare values or
store map keys merely because one eventual call might supply an eligible concrete value.

## Subtypes, conversions, and joins

Nothing is a subtype of every result type. Non-null values may satisfy Any; nullable lifting preserves genuine subtype
relations. A sum variant is a subtype of its parent. Generic variance is checked against fields and methods. Mutable
container arguments remain invariant. Immutable List/Set elements and Map values are covariant, while Map keys remain
invariant under genuine subtyping.

Functions are contravariant in parameters and covariant in results with matching arity/variadic shape. An ordinary
function may satisfy its otherwise compatible suspend type. Numeric widening, Char-to-String conversion, container
copying, and nominal map-key reconstruction are value conversions, not subtype relations or callable adapters.

Joins use identity, bottom elimination, compatible nullable/scalar widening, a proved subtype upper view, a common sum
parent, and approved widening through immutable container layers. They do not infer container-family copies or invent
Any for unrelated types. An explicit expected type can request an approved conversion. The [nullable-result
contract](equality-and-nullability.md) distinguishes contextual conversion from an inferred join.

## Inference and applicability

Infer generic arguments from supplied argument facts and expected result types when unambiguous. Explicit arguments
remain fixed: a bound cannot silently turn an explicitly supplied Int into Float. Inferred arguments may use approved
scalar joins/widenings through immutable conversion positions. Do not infer arbitrary family copies, mutable argument
adaptation, or implicit function adapters.

Dependent bounds use the complete substituted argument assignment. A later bound cannot be accepted against a stale
preliminary argument after an earlier inferred argument widens. Input/output positions constrain direction; invariant
positions require exact compatibility. Every proposed instantiation must satisfy all requirements and the ordinary
contextual argument checks before selection. A successful preliminary inference is not an accepted call.

Overload alternatives remain candidates until complete applicability and ranking resolve them. Exact, widening, copying,
and combined conversion categories retain their selected ordering, followed by nonvariadic, fewer-default, and
nongeneric tie-breakers. Distinct equally applicable instantiations are ambiguous. Declaration order and solver budget
exhaustion cannot silently select a candidate.

An overloaded reference uses its expected function type. Unresolved callback relationships contribute constraints
without premature overload selection; only facts shared by viable candidates may propagate. Defaults and variadics
retain their declared interfaces. Inference emits no runtime effects. Lowering evaluates supplied expressions and
conversions in source order, then omitted defaults in parameter order, preserving progress across suspension.

## Termination and failure

Alias and direct-bound checks track active declaration paths. Shared type-graph queries visit immutable child identities
without repeatedly expanding common descendants. Capabilities use a finite dependency fixed point; recursive nominal
references reuse established identities.

Inferred bound widening replaces scalar leaves only by approved targets, such as Int by Float, and stops when those
finite choices stop changing. Directional solving revisits dependent substitutions until assignments stabilize. The
development compiler also bounds type depth, solver rounds, and explored alternative states. Exhaustion reports an
actionable error suggesting explicit arguments; it never publishes an unchecked candidate or partial artifact.

These are development implementation guards, not a claim of complete inference for arbitrary inputs or target-scale
resource compliance. Completed-query cache limits are storage optimizations: evicting an entry cannot change a type
checking result. Aggregate memory and end-to-end timing require their separate workload and host measurements.

## Evidence and implementation

The [constraint cases](conformance/constraint-contracts.json) combine source-free cyclic interfaces, recursive nominal
bounds/aliases, dependent widening, symbolic capabilities, and preserved evaluation through checkpoints. Negative
controls cover direct/nullable parameter cycles, unknown unused bounds, insufficient symbolic capabilities, explicit
argument failures, incorrect recursive arguments, non-null bounds, and mutable map keys.

The compiler separates [directional constraints](../bifoil-compiler/src/generics/call_constraints.rs), [inferred
widening](../bifoil-compiler/src/generics/constraints.rs), and [overload
alternatives](../bifoil-compiler/src/compiler/overloads/constrained.rs). The [projection
contract](projection-semantics.md) defines hidden receiver inputs without guessing a concrete argument.

The [expected-result inference rule](function-contracts.md#argument-inference-and-expected-result-views) preserves
supplied arguments when the completed result fits by genuine subtyping. Expected types can fill missing parameters;
scalar conversions, invariant positions, explicit arguments, and function adapters keep their existing separate rules.

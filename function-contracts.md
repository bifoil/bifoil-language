# Function results, overloads, and contextual checking

This contract connects F02/F23 with the existing generic, conversion, control-flow, and anonymous-function rules.
The dated user clarification preserves supplied generic arguments when the result already satisfies the expected type
by genuine subtyping, including covariance.

## Parameter and result types

Every named or anonymous parameter has a written type. A signature may omit its result when the compiler can establish
one from its body. Named expression bodies return their expression; named block bodies use explicit return statements.
Anonymous blocks return their final executable expression and permit early returns from that anonymous function.

Resolve scope-wide function names before result inference. Concrete return paths may anchor self/mutually recursive
groups, including forward calls. An unanchored recursive result requires an explicit annotation. Missing annotations on
unresolved results never become dynamic types or escape into reusable artifacts.

Only normally completing, reachable result paths contribute to an inferred join. Use the [constraint
contract](type-constraints.md) for scalar/nullable joins, genuine subtype views, common sum parents, and immutable
container layers. Do not infer an arbitrary Any result or a container-family copy for incompatible branches. Full body
checking still validates expressions, annotations, returns, and effects; inference is not a way to hide an invalid
unused body or operand.

Named blocks with no value-return paths infer Unit, even when their statements happen not to terminate. An explicit
return of a Nothing expression can infer Nothing; a bare call statement does not implicitly return its value.
Value-returning blocks must return on every reachable normal path. A mixture of a value return and normal fallthrough
does not silently discard the return value.

A null-only inferred function result denotes the internal null-only value type, rather than choosing an arbitrary T?. It
can satisfy a nullable result view, including () -> Nothing?, through ordinary safe function variance. A binding whose
initializer supplies only null still requires an expected type under the selected binding rule. Authors may annotate a
public nullable result directly for its intended interface.

## Guard coverage and value branches

Evaluate a when subject once, then alternatives and guards in source order until selection. A false guard continues
testing later cases. Matching payload names are immutable branch-local bindings and are available to the guard.

An unguarded case contributes its matching domain to exhaustive coverage. A guarded case contributes that domain only
when its guard is proved true whenever it is reached. A constant true guard may therefore cover an enum case; an unknown
Boolean guard cannot. A later unguarded case can cover the same variant, including cases with payload bindings. The
coverage proof does not remove runtime evaluation, effects, or the selected evaluation/suspension order.

Value-producing if/when branches supply their final expression and require complete normal coverage. Statement forms can
continue without a matching branch where already specified. Early transfers contribute Nothing rather than a fabricated
value; result joins and definite assignment still use normally completing paths.

## Overload applicability and ranking

Overloads differ by parameter types or counts. Return types alone cannot distinguish declarations. First validate the
positional/named binding, omissions, variadic shape, generic instantiation, and argument compatibility.
The selected call must satisfy effect, capture, and initialization rules.
An unknown name or duplicate supplied argument does not become another overload's positional input.

Compare conversion ranks for supplied arguments: exact, widening, container copying, and copying plus widening. A
candidate dominates only when no worse for every supplied argument and better for at least one. Crossing preferences,
such as (Int, Float) versus (Float, Int) for two Int arguments, remain ambiguous.

Otherwise tied candidates prefer a nonvariadic signature, then fewer omitted defaults, then a nongeneric declaration. A
generic exact match can therefore beat a nongeneric match needing Int-to-Float conversion. An explicit expected type can
constrain generic inference or resolve a function reference; it does not make return-only overloads legal.

For an overloaded reference, require one compatible selection using the expected function type and applicable
reference-resolution rules. Numeric/result conversions and container copies do not automatically create a callable
adapter. Write an anonymous function when value conversion is needed. Genuine parameter contravariance, result
covariance, and ordinary-to-suspend widening retain their selected meanings.

Inference explores types and proofs without executing argument/default expressions. Once a call is selected, capture the
callable/receiver first, evaluate supplied arguments and their conversions left to right as written, then omitted
defaults in declaration order. Snapshot/copy conversions happen before the next supplied argument can mutate a source.
Completed evaluation survives suspension. Function values retain their positional interface and variadic shape rather
than parameter-name/default metadata.

## Unit-context anonymous construction

An expected Unit result can discard values from a newly constructed anonymous function's final expression and early
return statements. Evaluate those expressions and their effects exactly once, then return Unit. This does not adapt an
existing value-returning named reference or allow arbitrary value returns from a named Unit block.

The expected type may arrive through an imported alias or generic argument context. Nested functions/lambdas retain
their own return boundaries. Captured binding initialization, mutability, alias invalidation, and suspend restrictions
remain checked; discarding a result is not permission to skip those proofs.

## Argument inference and expected result views

Infer generic arguments from supplied argument types using the selected compatible joins and declared bounds.
Expected result types can fill parameters that remain unresolved. When those arguments satisfy every declared bound
and the substituted result is already a genuine subtype of the expected result, retain the inferred arguments.
Covariance, nullability, and safe callable variance may expose a broader view without constructing a different generic
instance. The runtime retains the instantiated arguments for type tests and casts.

For covariant Box<out T> and fun <T> box(value: T) = Box(value), an expected Box<Any> with box(4) therefore keeps T=Int.
After viewing the result as Box<Any>, testing it as Box<Int> is true. The same rule applies to a generated constructor,
nullable/immutable-container/callable result layers, and methods. Type aliases do not introduce a different identity.
Known arguments stay fixed while an expected result fills other missing parameters when that completed result fits.

If the result does not fit by subtyping, the existing contextual inference and applicability rules still apply. For
example, Box<Float> may require T=Float and widening the supplied Int argument; invariant Cell<Any> may require T=Any.
This rule does not make Int a Float subtype, change mutable-container invariance, or construct a function conversion
adapter. An explicitly supplied generic argument remains authoritative. Inference uses static argument types rather
than inspecting the runtime value hidden behind an Any view. No unanchored argument receives an arbitrary Any fallback.

## Evidence

The [combined inference cases](conformance/inference-contracts.json) cover typed result references, anchored recursion,
null-only callable views, compatible scalar joins, overload/default ordering, Unit early
returns, guarded coverage, and the selected retained-argument covariance rule.

Negative controls reject missing parameter types, unanchored recursion, incompatible/missing returns, return-only
overloads, crossing conversion preferences, unrelated generic joins, unanchored arguments, implicit callable adapters,
and unknown-guard coverage. The [existing interaction matrix](conformance/type-interactions.md) supplies broader
subtype, copied-container, reified identity, projection, and capture controls. Development inference guards and resource
failure boundaries remain those in the constraint contract, not a claim of unbounded algorithmic completeness.

The [retained-argument cases](conformance/covariant-inference.json) additionally check nullable, immutable List,
callable, constructor, alias, method-owner, and partially inferred result layers after fresh-host restore. They pair
covariance with numeric/invariant contexts, bound-driven widening, explicit arguments, static Any views, overload
ranking, one-time argument effects, missing-argument rejection, and forbidden function adapters.

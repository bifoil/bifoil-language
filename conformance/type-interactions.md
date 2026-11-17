# Type-system interaction matrix

The primary [source-free checkpoint case](cases/type-interactions-source-free-checkpoint/main.bfl) combines these
contracts in one client. Its helper module is compiled independently and removed before the client build. Paired
rejections isolate operations that must remain unavailable. The ordinary conformance runner restores every input wait.

| Interaction | Accepted behavior | Rejection control |
| --- | --- | --- |
| Function variance and nullability | `(Int?) -> String` satisfies `(Int) -> String?`; invocation retains the target signature. | [An input widening adapter](cases/function-input-conversion-adapter-matrix-error/main.bfl) and [a result widening adapter](cases/function-result-conversion-adapter-matrix-error/main.bfl) require explicit functions. |
| Overloaded references | An expected `(Int) -> String` selects the Int overload. | [An unresolved reference](cases/unresolved-overload-reference-matrix-error/main.bfl) is ambiguous. |
| Function-value call interface | A selected reference exposes positional argument types. | [Named arguments](cases/function-value-named-matrix-error/main.bfl) and [omitted declared defaults](cases/function-value-default-matrix-error/main.bfl) are unavailable through values. |
| Generic compatible joins | Int and Float inputs infer Float and preserve its runtime type. | [Different mutable element types](cases/generic-mutable-join-matrix-error/main.bfl) and [unrelated primitives](cases/generic-heterogeneous-join-matrix-error/main.bfl) do not acquire a fabricated common type. |
| Nullable copies and widening | A present List<Int>? can become an independent MutableList<Float>?; mutating the copy preserves the source. | Mutable invariance is retained by the generic-join control and existing [conversion controls](foundations.json). |
| Contextual Unit and aliases | A callback annotated through an imported alias discards its final String value and retains its effects across a checkpoint. | Adapting an existing function's result remains unavailable; contextual construction does not change reference conversion rules. |
| Ordinary-to-suspend widening | An ordinary function can be called through a suspend view in a scene. Its completed result survives the wait. | [A suspend view in prose](cases/suspend-view-prose-matrix-error/main.bfl) is rejected even when its current target is ordinary. |
| Reified callable identity | A wider exposed signature and suspend view preserve the original target type for runtime tests. | Numeric signature adaptation does not become subtyping. |
| Static equality eligibility | A concrete immutable generic key derives equality and coalesces equal set entries. | [Unknown Any equality](cases/unknown-equality-matrix-error/main.bfl) requires more static information. |
| Transitive key stability | Immutable containers and bounded generic data may be keys when their contents remain stable. | [An immutable container around mutable data](cases/nested-unstable-key-matrix-error/main.bfl) is rejected. |
| Dependent projected bounds | [Known and hidden sibling bounds](cases/dependent-projected-capabilities-source-free-checkpoint/main.bfl) retain sufficient equality/key guarantees after source removal and restoration. | [Equatable-only](cases/dependent-projected-equatable-key-error/main.bfl) and [unbounded](cases/dependent-projected-unbounded-key-error/main.bfl) hidden mutable contents do not become stable. |
| Projected bounds through outer parameters | [Source-free compositions](cases/projected-capability-compositions-source-free-checkpoint/main.bfl) retain alternative sufficient bounds through multiple fields, recursion, and sum payloads. | [Unknown guarantees](cases/projected-capability-composition-unknown-key-error/main.bfl) and [mutable keys](cases/projected-capability-composition-mutable-key-error/main.bfl) are rejected; [mutable equality](cases/projected-capability-composition-mutable-equality/main.bfl) remains available. |
| Captured state and lifetime | [Compact closures](../../bifoil-runtime/test/compact-captures.test.mjs) share one mutable cell after collection and restoration. | Existing publication and initialization controls prevent reading uninitialized captured cells. |
| Bound receivers and generic views | [Saved bound methods](cases/bound-method-reified-view-source-free/main.bfl) preserve their captured instance and reified result after source removal and a wait. | Reassigning the source binding does not retarget the reference or create a conversion adapter. |

The [generic result conversion case](cases/generic-result-conversion-source-free-checkpoint/main.bfl) checks callback,
invariant input, named/spread vararg, nested immutable widening, and copied mutable result paths together. Its
independently compiled helpers are removed before the client build; a suspended callback resumes in a fresh host without
repeating earlier calls or conversions. Result-only generic arguments still use the expected type. Paired rejections
retain explicit arguments, bounds, callback signatures, and mutable element invariance. The [overload
control](cases/generic-result-overload-source-free/main.bfl) checks omitted-default and nongeneric tie-breaks after a
valid supplied-argument specialization is found.

The [overloaded callback checkpoint](cases/overloaded-callbacks-source-free-checkpoint/main.bfl) combines partial
generic shapes, later argument constraints, nested literal groups, reified callback types, and a receiver retained
before a suspending later argument. Its source-free helpers and restored host preserve the selected instance and single
evaluation. Separate [cyclic artifacts](cases/overloaded-callbacks-cyclic-source-free/main.bfl) and [variance/variadic
controls](cases/overloaded-callbacks-variance-source-free/main.bfl) check module-interface loading and function subtype
shape. Paired failures preserve ambiguity, explicit arguments, bounds, suspension direction, variadic shape, nominal
identity, receiver flow invalidation, and enclosing generic ownership.

The [directional checkpoint](cases/directional-inference-source-free-checkpoint/main.bfl) combines contravariant
callback inputs, a receiver captured before a suspended later argument, an omitted default, a second wait inside the
callback, and exact effect ordering. [Joint references](cases/directional-inference-joint-source-free/main.bfl) require
one complete instantiation across overloaded references and nested list/map literals. [Cyclic
artifacts](cases/directional-inference-cyclic-source-free/main.bfl), [value
widening](cases/directional-inference-value-widening-source-free/main.bfl), [contextual
containers](cases/directional-inference-container-context-source-free/main.bfl), [owner
parameters](cases/directional-inference-owner-source-free/main.bfl), and [nominal
variance](cases/directional-inference-nominal-variance-source-free/main.bfl) retain their selected rules after helper
source removal. Paired errors preserve explicit types, null safety, mutable invariance, capability bounds,
ordinary/suspend direction, and ambiguity; no function adapter is inferred. These cases exercise directional and
alternative constraints without establishing every generic inference interaction.

The [whole-literal checkpoint](cases/directional-inference-whole-literals-source-free-checkpoint/main.bfl) infers
complete list, map, nested, and mutable collection shapes from joint overloaded elements, before any expected collection
shape exists. Source-free functions and reified collection types survive the wait. Its [ambiguity
control](cases/directional-inference-whole-literal-ambiguity-error/main.bfl) rejects multiple complete solutions. The
existing mutable-join rejection remains mandatory; a bare inference variable cannot reconstruct incompatible mutable
literals into a common type.

The [higher-order checkpoint](cases/lambda-inference-source-free-checkpoint/main.bfl) infers an anonymous factory
returning an overloaded bound method. Creation leaves its body effects deferred; a saved visit changes the captured var,
and a later bound reference retains the selected instance. [Branch
results](cases/lambda-inference-branch-source-free/main.bfl), [whole
literals](cases/lambda-inference-whole-literals-source-free-checkpoint/main.bfl), [cyclic
modules](cases/lambda-inference-cyclic-source-free/main.bfl), and [partial generic
references](cases/lambda-inference-generic-reference-source-free/main.bfl) share the same result-provider path after
source removal.

The [suspending factory](cases/lambda-inference-choice-checkpoint/main.bfl) returns through a final choice and preserves
its count and callback over two restored waits. [Private lexical
scope](cases/lambda-inference-method-scope-source-free/main.bfl) remains available to an escaping factory defined inside
its class; the paired [outside-access rejection](cases/lambda-inference-private-result-error/main.bfl) remains enforced.
[Missing fallthrough results](cases/lambda-inference-missing-return-error/main.bfl), [authored
returns](cases/lambda-inference-authored-return-error/main.bfl), ambiguous references, capture guards, signature
adapters, and invalid unused bodies retain rejection controls. [Unit
construction](cases/lambda-inference-unit-source-free/main.bfl) preserves its final effect and discarded value.

The [dependent-bound checkpoint](cases/dependent-bounds-source-free-checkpoint/main.bfl) combines numeric and Char
widening, dependent chains and nested immutable bounds after helper sources are removed. Two restored waits preserve the
completed first argument and the exact `AB` effect trace. [Structural
bounds](cases/dependent-bounds-structural-source-free/main.bfl) infer an otherwise missing element argument and respect
invariant nominal fields. [Callbacks](cases/dependent-bounds-callbacks-source-free/main.bfl) and [anonymous
results](cases/dependent-bounds-lambda-source-free/main.bfl) retain contravariant inputs and covariant results without
adapting function signatures. [Cyclic artifacts](cases/dependent-bounds-cyclic-source-free/main.bfl) and [recursive
generic calls](cases/dependent-bounds-recursive-source-free/main.bfl) preserve parameter identities. Both cyclic helpers
declare dependent generic bounds. Provisional declaration rounds resolve parameter names before the complete-interface
pass validates their bounds; invalid unused bounds remain errors before publication.

Paired failures reject explicit incompatible arguments, unrelated observations, invariant nominal/mutable changes,
container-family copies and callback-result adapters. Unobserved bounds cannot invent arguments, and direct upper bound
cycles remain definition errors. These cases do not establish complete generic-constraint acceptance.

These rows define an acceptance matrix, rather than a claim that every type-system interaction is complete. In
particular, complete flow/publication proofs, other projection operations, and unresolved observable contracts remain
separate checklist obligations. Exact equality through covariant views follows the separate [declared-view
contract](../comparison-view-equality.md); this matrix alone does not certify that behavior.

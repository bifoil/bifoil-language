# Determined review obligations

This maps all 26 numbered cases in the draft's
[review section](../language-specification-draft.md#review-cases-with-outcomes-already-determined-by-steering) to
targeted
assertions or an explicit remaining gap. An entry identifies evidence for the stated part; it does not certify the
entire decision or every interaction. Compilation, execution, runtime fixtures, and resource measurements have different
scopes.

| Review | Targeted evidence | Scope and remaining limits |
| --- | --- | --- |
| 1. Integer boundaries | [Dynamic multiplication overflow](cases/numeric-dynamic-multiply-overflow-failure/main.bfl), [division overflow](cases/numeric-dynamic-division-overflow-failure/main.bfl), [remainder](cases/numeric-dynamic-division-remainder-and-truncation/main.bfl) | Dynamic failure pairs include an unreachable output marker; remainder and truncation assert values. |
| 2. Finite Float | [Zero division](cases/numeric-dynamic-float-zero-division-failure/main.bfl), [nonfinite product](cases/numeric-dynamic-float-nonfinite-failure/main.bfl) | Dynamic checks rather than constant-folding substitutes. |
| 3. Fairmath | [Endpoints and signed modifiers](cases/fairmath-dynamic-endpoints-and-modifiers/main.bfl), [compound source-free reads](cases/compound-fairmath-read-source-free/helpers.bfl) | Explicit endpoint values, unrestricted finite modifier signs/magnitudes, and Int.MIN negation. Parser grouping has native negative controls. |
| 4. Safe-call laziness | [Nullable calls and indexes](cases/nullable-lazy/main.bfl), [skipped indexing](cases/safe-index-skipped-initialization/main.bfl) | Skipped effects and definite-assignment controls; ordinary invalid indexing remains checked. |
| 5. Evaluation order | [Copies before later arguments](cases/collection-copies/main.bfl), [overload order](cases/overload-evaluation-order/main.bfl), [defaults](cases/suspended-defaults-checkpoint/main.bfl) | Callable capture, supplied conversions, and defaults have targeted assertions. |
| 6. Duplicate keys | [Duplicate before value](cases/duplicate-key-before-value/main.bfl) | The first value prints; the duplicate's value must not execute. |
| 7. Nullable map lookup | [Presence and missing lookup](cases/collection-order/main.bfl) | Key presence with a stored null and missing lookup are asserted; broader value/key combinations remain partial. |
| 8. Family copies/invariance | [Independent copies](cases/collection-copies/main.bfl), [projected copies](cases/generic-projected-copy-reification/main.bfl) | Native conversion tests cover copying plus widening and mutable invariance; no arbitrary intermediate conversion chains are introduced. |
| 9. Shallow sharing | [Container aliases](cases/collection-copies/main.bfl), [data aliases/copy](cases/data-methods-copy/main.bfl) | Instance sharing and container independence are explicit; deeper cyclic combinations remain wider acceptance work. |
| 10. Stable keys | [Mutable data key rejection](cases/data-mutable-key-error/main.bfl), [unstable bound rejection](cases/generic-bound-unstable-set-error/main.bfl) | Both direct use and unused generic-bound spelling must reject. |
| 11. Empty traversals/ranges | [Constant range](cases/invalid-range/main.bfl), [dynamic equal bounds](cases/numeric-dynamic-range-equal-failure/main.bfl), [reversed bounds](cases/numeric-dynamic-range-reversed-failure/main.bfl) | Dynamic range failures are direct. [An empty-List counter](cases/empty-list-iteration-counter-checkpoint/main.bfl) asserts zero iterations across a restored wait. |
| 12. Do-condition assignment | [Continue before initialization](cases/delayed-continue/main.bfl) | Negative direct-condition read; native loop-inference/initialization tests supply positive controls. |
| 13. Numeric equality | [Runtime primitive assertions](../../bifoil-runtime/test/runtime.test.mjs), [generic exact comparison](cases/exact-equality-independent-generic-types-source-free-checkpoint/helpers.bfl) | Runtime primitives directly assert both 3 == 3.0 and 3 === 3.0; the generic case executes after source removal/restoration. |
| 14. Generic reification | [Empty projected collections](cases/generic-projected-copy-reification/main.bfl) | Empty concrete Int arguments survive projection, copying, and a restored wait; Float tests cannot manufacture a match. |
| 15. Definition checking | [Unused unconstrained search](cases/collection-search-unconstrained-error/main.bfl), [malformed bound](cases/generic-bound-unstable-set-error/main.bfl) | Invalid operations/types reject even when never called. |
| 16. Overload ordering | [Conversion dominance](cases/overload-conversions/main.bfl), [tie breakers](cases/overload-ties/main.bfl) | Variadic/default preferences and the final nongeneric preference remain distinct. |
| 17. Enum conflicts | [Generic expected-type conflict](cases/generic-enum-shorthand-conflict-error/main.bfl), [Unit conflict](cases/unit-enum-conflict-error/main.bfl) | Required qualification is checked; arbitrary namespace interactions remain provisional. |
| 18. Guard continuation | [False guards with effects](cases/when-guard-effects/main.bfl) | Failed guards preserve their effects and continue. Parser/native tests reject invalid fallback placement. |
| 19. Captured state | [Delayed capture](cases/delayed-capture/main.bfl), [bound receiver capture](cases/data-methods-copy/main.bfl) | Shared cells and receiver capture are separate; broader alias/lifetime combinations remain partial. |
| 20. Suspension effects | [Saved suspend lambda](cases/lambda-suspend-checkpoint/main.bfl), [invalid default effect](cases/suspended-defaults-effect-error/main.bfl) | Static function-type tests also cover ordinary-to-suspend widening; reverse widening remains invalid. |
| 21. Scene transfer | [Returning caller](cases/scene-transfer/main.bfl) and [transferring scene](cases/scene-transfer/middle.bfl) | Original caller resumes; transferred scene's trailing prose must not run. |
| 22. Saved snapshots | [Traversal and bound callback](cases/gc-traversal-and-bound-method/main.bfl), [once history](cases/once-checkpoint/main.bfl) | The runner restores at every input wait; host/browser acceptance is separate. |
| 23. Build compatibility | [Runtime owner and limits](evidence/runtime-build-compatibility.md) | Direct incompatible-ID rejection; no cross-update migration claim. |
| 24. Legacy validation | [Wrong integer](cases/legacy-wrong-integer/main.bfl), [invalid enum result](cases/legacy-invalid-enum-result/main.bfl) | Execution uses an explicitly supplied unmodified engine; composite ownership remains undecided. |
| 25. Independent artifacts | [Suspended defaults](cases/suspended-defaults-checkpoint/main.bfl), [reified equality](cases/exact-equality-covariant-empty-reification-source-free-checkpoint/main.bfl) | Named artifacts are produced, sources removed, and clients compiled/executed; old module formats are explicitly refused. |
| 26. Resource failure | [Compiler CLI boundary tests](../../bifoil-compiler/tests/cli/module_capacity.rs), [resource protocol/limits](../../bifoil-compiler/RESOURCES.md) | Explicit guard failures and preserved roots are exercised. Aggregate helper accounting, portable enforcement, and the accepted source-capacity envelope are not certified. |

# Exact equality through declared views

The [accepted E29-E30 rules](accepted-clarifications.md#exact-equality-and-comparison-views) compare composites through
their declared operand views. The compiler carries those views in a required v3 instruction. A comparison preserves
the values' construction identities, aliases, and later type-test/cast behavior.

## Distinguishing examples

A phantom covariant parameter makes the difference visible without granting equality to arbitrary Any fields:

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

The comparison is true; the type tests remain true and false. Empty List<Int> values viewed as List<Int?> follow the
same rule when compared with independently constructed empty List<Int?> values. Comparing the original narrower
value directly against a differently declared operand still distinguishes their comparison types.

Eligible child fields and container positions use the types exposed by their views. Hidden positions retain the
actual value's type when no concrete comparison type is exposed. Primitive kinds remain exact, nullable wrappers
flatten for present values, and different active sealed variants remain unequal. Static Equatable eligibility is
still required; a Box<Any> with an Any-valued field does not gain equality from its broad annotation.

## Execution and persistence

The compiler evaluates operands from left to right and captures each operand's static type before later operand
effects can invalidate flow facts. exact_compare carries left_type, right_type, and a required Boolean negate flag.
The runtime resolves generic parameters from the active frame, compares the evaluated operands, and returns Boolean.

The iterative traversal derives child types from container arguments and nominal field declarations. It caches field
substitution within that comparison. Cyclic pair facts include comparison context: an object pair that succeeds
through a broad view may still fail through a hidden view. Unordered candidate failures roll back their pair facts.
Sharing layout does not determine equality, and traversal depth does not consume the host call stack.

A suspended expression retains evaluated operands and generic frame arguments. The remaining instruction retains its
views in verified code, including after package eviction and reloading. Same-build input checkpoints resume without
repeating completed operand evaluation. No comparison rewrites or copies its operands.

## Profile and container compatibility

The current instruction profile is bifoil-vm.v3. Program v2, module v6, package v1/v2, code v1, and checkpoint v2
containers retain their structures. Their supported profile pairs are explicit in the
[compatibility contract](compatibility-contract.md).

V1/v2 runtime programs retain their prior exact-comparison behavior. V3 rejects an old binary exact operation without
required views; older profiles reject exact_compare. Current compiler module readers require v3 producer semantics
and regenerate previous-profile modules from source. Both eager and lazy package loaders require every chunk's
profile to match its root, even when its content hash is otherwise correct.

## Regression evidence

[The source case index](conformance/comparison-views.json) includes the original examples, independently compiled
helpers, recursive fields, lists, sets, maps, sealed variants, cyclic graphs, hidden views, primitive kinds, and
unsupported capability controls. Suspended right operands preserve the left operand and its view. A separate saved
Unit callback verifies that discarding an unread closure remains valid after restoration.

[Native tests](../bifoil-compiler/src/tests/comparison_views.rs) inspect emitted operand views, generic ownership, and
flow-order preservation. [Module-reader tests](../bifoil-compiler/src/module_input/tests.rs) reject missing comparison
context in ordinary and streamed input. [Runtime tests](../bifoil-runtime/test/comparison-views.test.mjs) exercise
context-sensitive memoization, unordered trials, 6,000 nested nodes, retained construction types, and mixed-profile
package rejection. These focused tests are separate from whole-language, production-host, and resource acceptance.

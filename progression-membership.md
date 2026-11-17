# Pinned progression membership

R07 uses Kotlin's implementation as the reference for stepped integer membership. The reference here is Kotlin v2.2.0 at
immutable commit [631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da][commit]. This pins the source used for the contract; it does
not claim to track Kotlin's latest release. Bifoil's separately selected integer width, checked arithmetic, range
construction, and fail-fast diagnostics retain their own rules.

## Reference paths

These are primary JetBrains source links at the same commit. They are references, not copied Bifoil implementations.

| Reference | Role |
| --- | --- |
| [Progressions.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/src/kotlin/ranges/Progressions.kt) | IntProgression's iterable representation and adjusted terminal element. |
| [ProgressionIterators.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/src/kotlin/ranges/ProgressionIterators.kt) | Stop on the final element before another increment. |
| [PrimitiveRanges.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/src/kotlin/ranges/PrimitiveRanges.kt) | IntRange's direct integer bounds membership. |
| [_Collections.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/common/src/generated/_Collections.kt) | Iterable membership delegates to index search; the index check precedes comparison. |
| [Collections.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/src/kotlin/collections/Collections.kt) | Common index-overflow declaration and error. |
| [CollectionsJVM.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/jvm/src/kotlin/collections/CollectionsJVM.kt) | The reference signed Int index check after wraparound. |
| [progressionUtil.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/src/kotlin/internal/progressionUtil.kt) | Terminal-element adjustment by the progression direction and positive magnitude. |
| [_Ranges.kt](https://github.com/JetBrains/kotlin/blob/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da/libraries/stdlib/common/src/generated/_Ranges.kt) | Positive step validation and hidden mixed floating/integer range-query overloads. |

## Integer query types

An IntRange or IntProgression accepts an Int membership query with `in` or `!in`. A generic value is accepted when its
declared bounds prove that it is non-null Int. Float, Char, nullable, and unconstrained generic values do not satisfy
that element contract. Handle null first or explicitly convert a numeric value with `Int(value)` where intended. The
pinned Kotlin source hides the ambiguous mixed floating/integer range overloads; its progression iterable has integer
elements. Bifoil retains its own approved numeric conversions elsewhere.

This restriction does not change compatible collection membership or ordinary Int/Float equality. For example, `Int(1.0)
in 1..3` is true, while a direct Float range query is a compile error. `1.0 in [1, 2]` retains ordinary
compatible-element equality. Original previously compiled instructions retain their execution behavior; tightening
source checking adds no instruction fields and does not reinterpret old programs.

## Search results and overflow

IntRange uses its direct Int bounds check. A stepped value, including `range step 1`, has the progression search
contract. Search considers yielded integers in their traversal order and returns true at the first equal value. An empty
progression has no match. A missing value returns false only if the reference search can exhaust normally.

The reference progression search uses a signed 32-bit index. Before comparing each yielded element, it verifies that the
index has not wrapped negative. The last valid element index is 2,147,483,647. A match at that index succeeds.
Exhausting exactly 2,147,483,648 elements without a match also returns false: the increment after the final comparison
does not cause another check when there is no next element. Attempting to examine element index 2,147,483,648 fails
before comparing it, including when that element would match.

For example, a progression from the minimum Int through -1 with step one has exactly the exhaustible count above. Its
final -1 is present; a query for zero is absent. Extending that progression through zero makes the zero query fail with
`progression search index overflow`. An earlier match still succeeds. A sufficiently long missing search also fails,
even when the queried integer lies outside the progression's endpoints, because the reference encounters the index
failure before it can finish. Descending progressions have the same traversal-index rule.

`!in` negates a completed membership result and preserves a failure. Runtime failures use Bifoil's fail-fast diagnostic
and the original operation location. They are not catchable Kotlin exceptions. The original ascending-empty-range
construction errors remain in force; membership does not manufacture an empty ascending range to avoid them.

## Approved constant-time optimization

On 2026-11-05 the user explicitly permitted constant-time calculation with identical results and failures. This
supersedes the earlier unselected-algorithm note without removing that design history. The checked receiver view still
selects the reference path: IntRange uses direct bounds, while IntProgression uses search-index behavior. An IntRange
viewed as IntProgression retains its original type identity but adopts progression search at that operation. A proven
smartcast back to IntRange uses direct bounds again.

The compiler encodes a progression search view by normalizing a temporary operand copy with its existing step. This uses
existing v3 instructions and leaves original stored/captured/container values unchanged. Module format v4 requires this
lowering; older reusable modules must be regenerated because their bodies have lost the source receiver view. The VM
profile and program/package/code/checkpoint formats remain unchanged.

Bifoil preserves the selected search result/failure without enumerating billions of integers. The following is a
closed-form derivation of the reference behavior, rather than a claim that Kotlin's source performs this optimization.
For a nonempty progression with first f, last l, signed step s, and integer query q:

1. Let d be the direction sign, h = abs(s), width = (l - f) * d, and distance = (q - f) * d.
2. The count is floor(width / h) + 1. A mathematical match requires distance within 0..width and divisible by h. 3. For
a match, its search index is distance / h. Without a match, the final examined index is count - 1. 4. Reject when that
examined index exceeds 2,147,483,647; otherwise return the mathematical match result.

An empty progression returns false before this calculation. Int32 endpoints give differences no larger than
4,294,967,295 and counts no larger than 4,294,967,296. These integer intermediates are exact in the selected binary64
runtime. Internal wider calculations do not perform a source-level overflowing Int subtraction. The operation uses a
fixed number of arithmetic checks and constant extra storage; it does not allocate a traversal snapshot.

The reference's check position matters: implementing the hidden index as ordinary checked Bifoil Int increment would
fail too early after the final valid index. The closed form preserves normal exhaustion at that boundary. It also
preserves the difference between a direct full-domain IntRange check and a `step 1` progression search.

## Terminal iteration

A progression's terminal element is aligned to its step within the selected direction. Iteration yields that terminal
once and stops before another addition. Reaching the maximum Int while ascending or minimum Int while descending does
not require an overflowing sentinel value. Saved iteration state must retain whether the terminal has already been
yielded, including a wait inside that final loop body. Positive step validation and the selected ascending range
construction errors remain separate checks.

## Verification and limits

The [source-free reference cases](conformance/progression-reference.json) check the last valid search index, gapped
membership, direct-range comparison controls, generic Int proofs, missing/found/descending overflow, explicit numeric
conversion, and terminal iterations at both Int limits. Helper source is removed before client compilation. Suspended
queries and every terminal loop body restore into a fresh runtime host in both output modes. Paired compile errors
reject unsupported query types without changing numeric collection membership.

[Native tests](../bifoil-compiler/src/tests/range_membership.rs) exercise query typing and generic proof boundaries.
[Runtime tests](../bifoil-runtime/test/progression.test.mjs) compare small progressions with explicit enumeration,
assert exact exhaustion/overflow boundaries, and execute full-domain queries in a child process with an external
three-second test deadline. The deadline bounds this operational test; the derivation supplies the complexity argument.
It is separate from the compiler's incremental-build resource contract and whole-game performance acceptance. No
Kotlin/JVM executable comparison is claimed: this reference was inspected as immutable official source. Capacity and
production-host acceptance remain separate obligations.

[commit]: https://github.com/JetBrains/kotlin/commit/631e9fdbe59cc92ac1e88e6ff3bbf4418b3ab9da


The current reusable format is v5, which adds the namespace producer obligations in the [compatibility
contract](compatibility-contract.md#namespace-and-nested-storage-producer-requirement). Its progression requirements
remain those introduced by v4 and still use VM profile v3.

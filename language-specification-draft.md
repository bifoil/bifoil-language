# Bifoil language specification draft

Updated: 2026-10-25 Status: Provisional design draft; an initial compiler/runtime slice is implemented and tested
separately.

## Reading this draft

This document consolidates the accepted language direction in [language-steering.md](language-steering.md). The steering
record preserves decision IDs and their detailed history. The latest direct user instruction takes precedence over both
documents.

Statements here describe the selected design. The narrower implemented subset and evidence are linked from
[implementation status](implementation-status.md); examples in this draft remain original syntax sketches. Open items
are explicitly incomplete; an example does not settle surrounding grammar, representation, or APIs. Review-derived
obligations explain consequences of selected contracts. Working interpretations remain proposals; they do not add
accepted steering decisions.

The planned steering questionnaire is complete. Remaining work is specification drafting and feasibility review. A
material conflict or a change to accepted scope may require user input. Routine details should be proposed together in
the draft instead of becoming another open-ended sequence of feature questions.

This repository defines the language. Compiler implementation belongs in Bifoil Compiler and execution components in
Bifoil Runtime. Native story executables, self-hosting, general inheritance, and release commitments remain unselected.

## Targets and compiler contract

Steering: S01-S15.

Bifoil is a strongly statically typed language with Kotlin- and Python-inspired syntax. New Bifoil source has its own
grammar. Projects may also contain unchanged legacy ChoiceScript through a compatibility front end; legacy source
retains its original semantics.

The compiler must be a native implementation written in C++, Rust, or Go. The initial slice uses Rust. This requirement
concerns the compiler program; it does not require native machine-code output for a story.

The first compiler milestone must support ahead-of-time Bifoil-to-ChoiceScript compilation and reusable, independently
compiled module artifacts. Compiling a project only when a player executes its source does not fulfill that contract.

A required Bifoil runtime layer or engine extensions may implement language features. The output must preserve Bifoil
semantics and state its runtime requirements. Compatibility with an unmodified ChoiceScript interpreter is not an
initial requirement. Existing vendored engine sources remain subject to their provenance and modification policies.

### Resources and measurement

Aggregate peak memory for the compiler and its helpers must remain strictly below 250,000,000 bytes at every moment.
This is an aggregate compiler-job budget, not an average or an allowance limited to its managed heap.

An incremental end-to-end compilation using precompiled modules must complete in strictly less than ten seconds for a
published workload on reference hardware. Clean builds scale with total source input. Inputs beyond the supported
envelope receive an explicit diagnostic. Resource-budget failure is a failed build, not a successful compilation.

The capacity target is tens to hundreds of millions of source lines. The current small development limits do not
establish compliance. Disk-backed interfaces, streaming compilation/linking, and lazy runtime code loading remain
necessary at that scale. Source size does not itself bound active runtime allocations or executed loop iterations.

The acceptance protocol still needs a concrete workload, type-complexity limits, reference hardware, memory metric,
cache conditions, and measurement procedure for the complete language milestone. The initial slice has a published
workload and measured results in its resource report; full-milestone performance compliance remains unverified.

### Resource acceptance protocol: review requirements

The numeric limits in S13-S14 are selected; this protocol is still a draft. Define the memory quantity and the
measurement boundary before reporting a pass. Reserved address space, committed memory, resident memory, and a managed
heap counter are different quantities; substituting one without explanation does not establish the aggregate contract.

For a quantity measured across processes, the relevant peak is the maximum simultaneous total over the compiler job.
Independent per-process peaks are not the same quantity, and a single compiler-process peak excludes its helpers.
Periodic samples can miss short spikes; the protocol needs a justified peak-accounting method.

Language/runtime settings alone are insufficient evidence. Go documents GOMEMLIMIT as a soft limit and allows the
runtime to exceed it; its runtime accounting also does not cover every external memory source. Go remains an allowed
implementation language, but setting GOMEMLIMIT is not proof of the hard compiler-and-helper bound. [Go GC guide][r1]

Platform mechanisms also need qualification. Linux cgroup accounting includes descendants and records a group peak, but
includes more than an ordinary process heap, and memory.max can be exceeded temporarily. Windows JobMemoryLimit limits
committed virtual memory for the job; it is not the same metric as resident memory. These are candidate accounting
tools, not a selected platform contract or a demonstrated hard bound. [Linux memory controller][r2], [Windows job
limits][r3]

The acceptance procedure must specify all of the following:

1. The supported source bytes, module/dependency graph, type complexity, and diagnostic workload.
2. The reference machine, operating environment, storage, concurrency, and cache conditions.
3. Which precompiled dependencies already exist, which modules are rebuilt, and what work is included in a clean build.
4. The measured memory quantity, process membership, peak measurement, enforcement behavior, and required headroom.
5. A monotonic end-to-end timing boundary covering required startup, compilation, linking, and artifact completion.
6. The complete run results, including failures and worst observed resource use; a median alone cannot demonstrate the
   selected worst-case-within-envelope requirement.

Budget enforcement, successful compilation, and measurement are separate obligations. A process killed by a limit has
not compiled successfully. A configured limit does not prove that every transient peak stayed below the selected bound.
Actual workload limits, hardware, memory metric, measurement tools, and results remain open.

### Independently compiled modules

Reusable compiled modules are required from the first milestone. Their interfaces must carry enough information to
preserve static checking and observable calling behavior, including exported types, suspension effects, and the
applicable named/default/variadic argument contracts.

The following interface obligations are derived from independently compiled modules and the already-selected language
behavior. They specify information that must remain recoverable, not a binary format or a new source syntax:

1. Exported symbol identities and type graphs, including nominal declarations, variant relationships, type parameters,
   variance, constraints, nullable forms, and transparent aliases.
2. Callable contracts: parameter order, types, names for direct calls, default availability and behavior, variadic
   shape, return type, overload identity, and suspension effect.
3. Definition-scope access needed by defaults and closures. Importing a module must not make a default read the caller's
   similarly named local variable or turn a per-call default into a one-time constant.
4. Runtime requirements needed to preserve type tests, checked operations, captured bindings, scene transfer behavior,
   and the selected call interface.
5. Initialization dependencies and original source identities sufficient for deterministic shared initialization and
   source-mapped diagnostics.
6. Artifact/dependency/runtime compatibility information sufficient to reject an incompatible artifact instead of
   silently treating its interface as current.

A decisive review case is a client compiled against an artifact without access to the dependency's source. Direct
named/default calls, taking a function reference, generic type tests, and calls that can suspend must retain the same
specified behavior. Removing source access must not erase names/defaults from direct calls or add them to function-value
calls. Exact supported artifact combinations remain to be defined.

The artifact extension, format, versioning, ABI, linking strategy, generic representation, and compatibility validation
remain open. This draft does not select native object files, a virtual machine, a particular intermediate representation
for the full language. The restricted implemented instruction profile is documented separately.

## Source files, projects, and modules

Steering: M01, M08-M09, M16-M19.

The preferred source extension is `.bfl`, replacing the earlier `.bifoil` default in this provisional design. The
extension has known collisions with Betaflight flight logs and IBM Bus Functional Language source. See the [dated
conflict check](language-steering.md#preferred-extension-and-conflict-check). It is a preferred candidate, not a claim
of exclusive use or universal editor recognition.

Sources live under `src/`. Directory and file paths determine dotted module names; for example, `src/story/stats.bfl`
corresponds to module `story.stats`. A `bifoil.toml` manifest names the entry scene. Exact manifest keys, path
validation, module-name restrictions, and conflict handling remain to be written.

A scene file has one executable scene body plus declarations. Library modules contain reusable declarations and
non-suspending initialization. Top-level symbols are private by default. Export intended interfaces and explicitly
import the symbols another file uses:

```
import story.stats.gold as coins
```

Use the `export` modifier on exported declarations. Detailed import resolution, re-exports, and modifier ordering remain
open. The file's module name and a scene header's logical scene name have distinct roles.

As integration guidance, use project context or explicit language selection alongside the extension. A suffix alone
cannot distinguish Bifoil source from every existing `.bfl` format.

## Layout, spelling, and lexical modes

Steering: L01-L11, E08, F01-F03, T01-T02, T09-T11.

Ordinary blocks open with a colon and use indentation. Each leading tab and each complete group of four spaces
contributes one structural level. Leftover spaces are alignment. One tab plus four spaces contributes two levels; six
spaces contributes one level plus two alignment spaces. Tabs and spaces may be mixed under this counting rule.

Ordinary expressions may continue within parentheses or after an unfinished operator such as `+` or `=`. Continuation
indentation is alignment. Block expressions embedded within expressions retain structural indentation.

Corresponding branch headers align, and their bodies use the same structural level. Both `elif` and `else if` are valid
and equivalent; formatting preserves the author's spelling. Use `fun` exclusively for named functions.

Names and keywords are case-sensitive. Logical operators are `&&`, `||`, and `!`. The ordinary and exact equality
operators are distinct.

Narrative enters a separate unquoted mode through `prose:`. Line-leading `@` directives after indentation return to
executable Bifoil syntax; nested conditional and loop bodies remain in prose mode by default.

Complete tokens, comments, identifier rules, newline handling, indentation jumps, and continuation/block interactions
remain open. No complete formal grammar is claimed by this draft.

## Bindings, scope, and initialization

Steering: B01-B10, C01, C07-C08, F07-F08, F14-F21.

`val` declares a binding that cannot be reassigned; `var` declares a reassignable binding. Binding mutability is
separate from the mutability of referenced contents. Reassignment retains the binding's static type.

Infer a binding's type where possible. Permit explicit annotations and require them when inference cannot establish a
type. A local declaration may omit its initializer only with an explicit type. Every read requires proven
initialization; each delayed `val` binding may be initialized at most once.

Bindings have lexical block scope. A local variable name is visible from its declaration onward, including nested
blocks, and is unavailable outside that scope unless retained through a supported capture.

Reject declarations that reuse currently visible binding names. Same-scope function overload sets are allowed; nested
shadowing remains prohibited. Receiver/member lookup interactions still need formal specification.

Named functions are visible throughout their enclosing scope, including before their declarations. A local function may
read enclosing bindings visible where it is declared and may reassign an enclosing `var`. Reads observe that binding's
current value. Escaping functions retain captured bindings; captures of the same binding share its state.

A function may be declared before a visible captured binding is initialized. Every call that could read it requires
compile-time proof of initialization. Definition order does not extend local variable name visibility.

## Primitive and universal types

Steering: P01-P16, N01-N07, B20, E25, F06.

The initial scalar types include `Boolean`, `Int`, `Float`, `String`, and `Char`. Boolean literals are `true` and
`false`; conditions do not use truthiness.

`Any` accepts every non-null value. `Any?` also accepts null. Operations still require suitable static type information.
Universal types do not introduce an arbitrary `Any` fallback when inferring common types.

`Unit` is an ordinary type with one value. A function returning no meaningful value may infer `Unit`, end naturally, or
use bare `return`. The source spelling of the Unit value remains open.

`Nothing` has no values and is compatible with every result type. A path that never produces a value does not force an
incompatible branch-result type.

### Integers and floating-point values

`Int` is signed 32-bit: −2,147,483,648 through +2,147,483,647. Out-of-range constants are compile errors. Arithmetic
overflow is checked at runtime.

`Float` is finite binary64 with ordinary floating-point rounding. Division by zero, infinity from overflow, and invalid
non-finite results are errors.

Automatically widen `Int` to `Float` in assignments, arguments, and mixed arithmetic. All Int values are exactly
representable in the selected Float model. Float-to-Int conversion is explicit, truncates toward zero, and rejects a
converted result outside the Int range. Its API spelling remains open.

`Int / Int` returns an Int truncated toward zero. A Float operand makes division produce Float. Integer remainder
satisfies the mathematical rule `a % b = a − (a / b) × b` and follows the dividend's sign when nonzero.

```
3 / 2
-3 / 2
3 / 2.0
-5 % 3
```

The respective results are `1`, `-1`, `1.5`, and `-2`. The minimum Int divided by −1 overflows; its remainder by −1 is
mathematically zero. Lowering must distinguish those cases.

Numeric literal grammar, negative zero, floating remainder, and remaining checked-operation edge cases need completion.

### Text and characters

String contents are immutable. A Char contains exactly one Unicode scalar value, excluding surrogates. String length,
indexing, and substring bounds count scalar values, not UTF-16 code units or displayed glyphs.

Use double quotes for String literals and single quotes for Char literals. Triple double quotes introduce multiline
strings with ordinary escapes and interpolation. Strip common leading indentation from nonblank lines while retaining
newlines and other content. Exact mixed-whitespace and delimiter-line treatment remains open.

Quoted literals support braced Unicode escapes with one to six hexadecimal digits, such as `\u{41}` and `\u{1F600}`, and
fixed-width forms such as `\u0041` and `\U0001F600` with four and eight digits respectively. Also support `\\`, `\"`,
`\'`, `\n`, `\r`, `\t`, and `\${`. Unknown escapes and invalid scalar values are errors.

Ordinary strings support `${expression}` interpolation. Evaluate substitutions left to right with the enclosing
expression's suspension permissions and preserve completed work across suspension. Narrative and option labels use the
narrower non-suspending rules described below.

`text.length` produces Int. Indexing `text[i]` uses zero-based, nonnegative Int positions and produces Char.
`text.substring(start, endExclusive)` requires both bounds, with `0 <= start <= endExclusive <= text.length`. Equal
substring bounds produce an empty String. Provably invalid constant bounds are compile errors; other invalid bounds are
runtime errors.

Char automatically widens to a one-element String in assignments, arguments, and string operations. Exact Char parameter
matches remain preferable in overload resolution.

When either `+` operand is String, the other may be a directly renderable non-null primitive and is formatted as
interpolation would format it. This does not introduce general numeric or Boolean-to-String assignment conversions.

String preserves exact scalar sequences without Unicode normalization. String equality compares those sequences.
Ordering is case-sensitive scalar lexicographic order; a matching shorter prefix sorts first.

Exact primitive rendering, conversion APIs, external encoding, malformed input, and residual mixed Char/String
comparison and join rules remain open.

## Nullable values, type tests, and casts

Steering: B08-B09, B11-B19, B21-B25, G15.

Types are non-null by default. `T?` permits null. Null checks and successful type tests narrow values automatically
where control flow proves that writes, calls, aliases, and suspension cannot invalidate the proof.

Nullable application flattens to one layer; explicitly repeated syntax such as `Int??` is an error. A declaration
initialized only with null needs an expected type: `val name: String? = null` is valid, while `val name = null` is an
error. Empty and all-null collection literals also require sufficient context.

Safe operations evaluate their receiver or callable once:

- `value?.member` and `value?.method(...)` yield null for a null receiver; method arguments and the call are skipped.
- `items?[index]` skips the index or key expression when the receiver is null.
- `callback?.(arguments)` skips arguments and invocation when the callable is null.
- `value ?: fallback` evaluates the fallback only when the left value is null.
- `value!!` reports a runtime error for null and otherwise produces the non-null value.

A present receiver follows its ordinary indexing, invocation, and suspension rules. Map lookup in a map whose value type
is already nullable still produces one nullable layer; absence and a stored null are distinguished by key presence.

Approved conversions lift through nullable types: convert present values and preserve null. This includes scalar
widening and the approved collection conversions.

Ordinary type tests use `is` and `!is`. Runtime tests retain generic arguments, including for empty collections, and
follow subtype rules without converting scalar values or copying containers.

`value as T` checks compatibility and fails on a dynamic mismatch. `value as? T` yields null on mismatch. Casts do not
perform scalar conversions or container copies. A cast provably impossible between concrete types is a compile error.
Complete cast grammar, precedence, and compatibility proofs remain open.

## Expressions, evaluation, and control results

Steering: E01-E14, E25-E27, N13.

Conditions require Boolean values. `&&` and `||` short-circuit and skip their right operand when the result is already
determined. Ordinary binary operators fully evaluate the left operand before the right.

Ordinary arithmetic uses conventional precedence. Multiplication and division bind before addition and subtraction;
comparisons bind before `&&`, which binds before `||`. Parentheses override grouping.

Elvis `?:` follows the selected Kotlin precedence relationship: arithmetic, ranges, and infix range modifiers bind more
tightly; membership, comparisons, equality, and logical operators bind less tightly. Repeated fallbacks associate right
to left. The full operator table, including casts and type tests, remains incomplete.

Plain and compound assignments are statements. For plain assignment, capture target receivers and indexes or keys once,
left to right, before evaluating and converting the right side and writing. Exact bounds-check timing remains open.

Compound `+=`, `-=`, `*=`, `/=`, and `%=` capture and read the target once before evaluating the right side. Apply the
ordinary operator, overflow, conversion, and assignment rules. Fairmath compounds follow the same target order.

Existing `return`, `break`, `continue`, and `goto` may appear in expression positions where the surrounding function,
loop, or story context permits them. Their transferring paths produce no value and have type Nothing.

Value-producing branch and return inference uses compatible scalar/nullable joins and approved immutable-container
widening. It does not infer a common type by copying between mutable and immutable families. An explicit expected type
may request approved copies.

Python-style chained comparisons remain unsettled. Explicit comparisons are valid; prefer range membership for suitable
bounds checks without changing invalid-range behavior.

## Fairmath

Steering: N08-N13. The [source baseline and grouping
notes](language-steering.md#fairmath-numeric-contract-and-source-baseline) remain part of this contract.

Support binary `%+` and `%-` and compound updates `%+=` and `%-=`. Both operands may be Int or Float; the rounded result
is Int. Use binary64 intermediates with the pinned ChoiceScript calculation order, rounding, and clamps.

For a base x in 0..100 and effective modifier d:

- If d > 0, take floor(x + d * ((100 - x) / 100)) and cap above at 99.
- Otherwise, take ceil(x - (-d) * (x / 100)) and raise below to 1.

For `%+`, d is the right operand. For `%-`, negate the right operand in the binary64 intermediate domain, including when
an Int operand is −2,147,483,648. The modifier may be any finite numeric value, including negative values and magnitudes
above 100.

These are directional clamps. In particular, `0 %+ 0` is 1, `100 %+ 0` is 100, and `100 %+ 1` is 99. Invalid constant
bases are compile errors; invalid dynamic bases are runtime errors.

Fairmath has no implicit chain associativity. Require parentheses when it combines with another binary operation or a
fairmath chain. `50 %+ (10 + 20)`, `(50 %+ 10) + 20`, and `(50 %+ 10) %+ 20` specify distinct written groupings.
Ordinary Int division and checked Int intermediate arithmetic do not replace the selected fairmath calculation.

## Equality and ordering eligibility

Steering: E03, E28-E31, E34, D08, D12, U06-U08, U22, G09-G10, F39.

Ordinary `==` and `!=` require compatible types. Int/Float equality uses the selected widening; unrelated types are
compile errors. Nullable values may be compared with null.

Exact `===` and `!==` compare exact type and value without widening or copying. Different non-null value types are
unequal, so `3 === 3.0` is false. Two nulls are equal regardless of their nullable annotations; a present Int?
containing 3 is exactly equal to Int 3. Prior value conversions still determine the value that is compared.

Lists compare elements in order. Sets and maps compare members or entries independently of iteration order. Data classes
compare corresponding fields of compatible nominal types. Through a compatible sum type, different variants are unequal
and matching variants compare payloads. Equality requires eligible component types.

Exact composite equality requires matching collection families and type arguments or the matching nominal value type,
then recursively applies exact equality to eligible contents.

Structural equality handles eligible cyclic graphs using tracked comparison pairs so a revisited pair does not recurse
forever. Shared-reference layout does not determine equality. Ordered and unordered cyclic algorithms still require
formalization and conformance cases.

Capability qualification is automatic. `Equatable` permits supported equality; `StableKey` additionally requires
equality that cannot change while stored. Immutable containers qualify for stable-key use only when their contents do.
Mutable composites do not qualify.

A value with static type Any or Any? and unknown equality capability requires narrowing or other static proof before
comparison; existing null comparisons remain available.

Function values support ordinary equality only for nullable comparisons with null. Their full exact-equality eligibility
remains open. No reference-identity equality operator has been selected.

### Static type views and runtime type identity

A zero-copy subtype view and a value conversion must remain distinguishable. Immutable covariance, nullable views, and
function variance do not authorize arbitrary numeric conversions or container copying. Runtime generic tests must still
retain the information required by G15, and transparent aliases must not acquire a nominal identity.

A remaining formalization case is comparing two collections through different covariant views when their runtime type
arguments or original construction types differ. The exact-equality rule must say which retained type identity is
compared and how it interacts with the static view. This draft does not invent a Boolean outcome for that unresolved
case. The same rule must hold for direct source, imported precompiled modules, and restored suspended state.

## Collections and conversions

Steering: D01-D30.

Provide immutable `List<T>`, `Set<T>`, and `Map<K, V>` and mutable `MutableList<T>`, `MutableSet<T>`, and `MutableMap<K,
V>`. Immutable containers cannot have their own contents changed through any alias. Referenced element values retain
their own mutability.

Use `[a, b]` for lists, `{a, b}` for sets, and `{key: value}` for maps. Without expected context, literals infer the
immutable family. A `mutable` prefix requests mutable construction; an expected mutable type may also guide it.

Infer compatible element/key/value joins: `[1, 2.5]` infers List<Float>, and `['a', "b"]` infers List<String>. Combining
T with null yields T?. Unrelated values require an appropriate explicit expected type or are errors.

Empty and all-null literals need sufficient expected types. `[]` is a list. `{}` is a set or map according to context;
insufficient context is a compile error.

Same-family mutable assignment and argument passing share the container. Corresponding mutable/immutable families may
implicitly convert by copying into an independent container. These copies preserve referenced element semantics and do
not recursively freeze or copy referenced objects.

Approved scalar widening lifts through immutable elements, keys, and values, recursively through immutable layers. A
family copy may combine with such widening. Stop recursive lifting at mutable contained types. Same-family mutable type
arguments remain invariant; implicit conversion chains must not bypass that rule.

Separately, immutable List/Set elements and Map values are covariant through genuine subtype relationships without
copying. Map keys remain invariant. Subtyping is distinct from scalar value conversion and container-family copying.

### Access, membership, and traversal

Use `size` for collection counts, with an Int result. List indexes are zero-based, nonnegative Int positions. Provably
invalid constant indexes are compile errors; other invalid indexes are runtime errors.

`mapping[key]` produces V?, returning null for absence or a stored null. `in` and `!in` test list/set elements and map
keys, including keys with stored null values.

Mutable lists permit indexed replacement; mutable maps permit indexed insertion or replacement. Add/remove method names
and their results remain open.

Set elements and map keys require StableKey eligibility. Sets coalesce equal members. Maps reject duplicate construction
keys, at compile time when provable and otherwise at runtime.

Evaluate literal elements and entries in source order. For each map entry, evaluate its key and reject a dynamic
duplicate before evaluating its value.

Sets and maps retain first-insertion order. Updating a map value retains its key's position; removing and reinserting
moves it to the end.

A collection for loop snapshots its traversal at entry. Lists and sets yield elements; maps yield entries with `.key`
and `.value`. Mutations to the original container do not change that traversal. Referenced elements retain their own
semantics. Entry type naming and further destructuring remain open.

## Integer ranges and loops

Steering: R01-R07, C01-C08.

Ranges are immutable first-class values. `a..b` is ascending and inclusive; `a..<b` is ascending with an exclusive end.
Invalid or empty ascending ranges are errors, statically when constant and otherwise at runtime. This includes `5..1`
and `5..<5`.

`a downTo b` explicitly selects inclusive descending traversal. `step n` requires a positive Int; direction comes from
the range form. Membership of a stepped progression follows the values it produces. The selected Kotlin reference does
not replace Bifoil's invalid/empty ascending-range rule.

`1..8 step 2` produces 1, 3, 5, and 7. An unreachable endpoint is not appended. The existing [stepped-membership
reference and cost issue](language-steering.md#integer-ranges-and-membership) remain unresolved; this draft does not
replace the requested reference implementation with a constant-time alternative.

`for i in range:` creates a fresh inferred immutable binding for each iteration, scoped to its body. `break` exits the
innermost loop; `continue` starts its next iteration. Optional labels use `outer@ for ...:`, with `break@outer` and
`continue@outer`. Targets must be enclosing loops in the same function.

Support pre-test `while` and post-test `do/while`. A post-test body runs at least once:

```
do:
    val finished = true
while finished == false
```

The trailing while aligns with do and has no colon. Direct body declarations are visible to the condition but not after
the loop. Every condition read requires initialization on every reaching path, including continue paths.

Descending invalid bounds, range type relationships, terminal-step overflow, and loop-bound evaluation timing remain
open. A rewrite to `0..<count` must account for the invalid empty range when count is zero.

## Functions, closures, and calls

Steering: F01-F44, A01-A08.

Declare named functions with `fun`. Parameters require type annotations. Return types may be inferred when unambiguous;
otherwise require an annotation with `->`.

```
fun double(value: Int) -> Int:
    return value * 2

fun increment(value: Int) = value + 1
```

Named block bodies use explicit return for values and must return on every reachable value-producing path. Expression
bodies return their expression. Unit-returning functions may end naturally or use bare return. Function-type annotations
always include a return type, including Unit.

Parameters are immutable bindings by default. `var` permits local parameter reassignment without rebinding the caller's
variable. Passing referenced mutable values retains their ordinary aliasing semantics.

Support self and mutual recursion, forward calls, and named local functions in functions or ordinary blocks. Each call
has fresh parameters and locals. Lexical capture and escaping lifetimes follow the binding rules above.

Function values are statically typed, storable, passable, and returnable. Take references with `::name`. For overloaded
references, an expected function type must identify a unique compatible overload.

Bound methods use `receiver::method` and capture the receiver once on reference creation. Reassigning the original
variable does not retarget the saved method.

### Anonymous functions and function types

Anonymous expressions use `(x: Int) => x + 1`. An anonymous block uses `(x: Int) =>:` followed by an indented body.
Their final expression supplies the value; an early return exits the anonymous function itself.

Optional return annotations precede the arrow body, as in `(x: Int) -> Float => x * 2`. Mandatory parameter annotations
remain in force. Anonymous functions may also declare a final variadic parameter.

When an anonymous function is constructed with an expected Unit result, evaluate and discard its final non-Unit result.
This contextual construction rule does not convert an existing function value into another signature.

Function types use forms such as `(Int, Int) -> Int` and `() -> Unit`. With matching parameter count and variadic shape,
subtype variance permits broader input types and narrower result types. Signature adaptation requiring scalar
conversions or copies needs an explicit anonymous function.

### Argument binding and evaluation

Support positional and named `name = value` arguments. Positionals precede named arguments; named arguments may appear
in any order. Unknown names and duplicate bindings are compile errors.

Evaluate and capture the callable or method receiver first. Evaluate supplied arguments left to right as written,
completing each applicable conversion before the next argument. Then evaluate omitted defaults in parameter order.

Defaults are evaluated at each call only when omitted. They may reference already-resolved earlier parameters and
bindings visible at the function declaration, but not later parameters. Defaulted parameters may precede required ones.

Calls through function values expose no names or defaults and require explicit positional fixed arguments. Variadic
shape is retained.

A `vararg values: Int` parameter accepts zero or more Int values and exposes a fresh immutable List<Int>. At most one
vararg is allowed, in the final parameter position. An omitted group produces a fresh empty list; explicit vararg
default expressions are forbidden.

Use star spreads of List or MutableList values, including interleaved groups:

```
gather(1, *first, 2, *second)
```

Expand groups at their source positions under the chosen evaluation order. A declared function name also accepts a named
list group, such as `gather(values = numbers)`, with applicable conversions and a fresh immutable callee list. Do not
supply the same group both positionally and by name. A function value may retain a type such as `(vararg Int) -> Unit`.

### Overloads

Overloads differ by parameter types or counts, not return type alone. Compare supplied arguments using conversion
categories: exact, widening, family copying, then copying plus widening.

A candidate dominates on argument types only when no worse on every supplied argument and better on at least one.
Otherwise tied candidates prefer nonvariadic shape, then fewer omitted defaults, then a nongeneric over a generic
candidate. Other unresolved ties are compile errors. Complete inference/overload interaction remains open.

## Type declarations and generics

Steering: U01-U33, G01-G15.

Types are nominal where declared as data classes, enums, sums, or variants. Transparent aliases denote existing types.
Permit top-level and local aliases, visible throughout their enclosing scope. Reject cycles in alias expansion;
recursive structures must pass through nominal data or sum types.

Plain enum aliases retain qualified case access: `typealias Color = Mood` permits `Color.Happy`, with the original
`Mood` identity. This applies to file and local aliases, including uses before the alias declaration in the same scope.
An alias does not make an enum namespace into a runtime value. Generic and other constructor-alias interfaces still
require further implementation coverage.

### Data classes

Use an indented field block with explicit field types. Fields use val or var. Methods use fun or suspend fun and have an
implicit receiver named this.

```
data class Character:
    val name: String
    var health: Int = 100

    fun heal(amount: Int):
        health += amount
```

A generated constructor follows field order and the existing positional/named/default rules. Field initializers are
defaults evaluated per construction when omitted. Assigning or passing an instance shares it.

Fields and methods are public by default, with public/private exceptions. Inside a method, bare member names are allowed
when unambiguous; explicit this.member remains available. Private field access does not hide the generated constructor
input from an otherwise permitted external construction.

Generate `instance.copy(...)` for an explicit shallow copy. Supplied fields replace values; omitted fields retain their
current values. Referenced field values retain their ordinary sharing semantics. Private copy inputs follow the
constructor-input policy. Exact copy evaluation timing and generated-name collisions remain open.

### Enums and sealed sums

Use `enum Mood:` with named cases on separate indented lines, without an enum class keyword. Qualified references use
Mood.Happy. A uniquely expected enum type may enable bare Happy.

If a visible ordinary binding and an expected enum case are both interpretations of a bare name, report a name conflict
and require qualification. Enums support stable equality and exhaustive case coverage.

Use sealed class for a closed sum, with explicitly typed case payloads:

```
sealed class Outcome:
    case Success(value: String)
    case Pending
```

Each variant has a nameable nominal subtype and may widen to the parent sum. Use Outcome.Success("Ada") for construction
and Outcome.Pending for a payload-free constant. Payload bindings are fixed; referenced values keep their ordinary
mutability.

Tests and patterns include `case is Outcome.Success:` and `case is Outcome.Success(value):`. Payload names are inferred
immutable branch-local bindings. Use `_` to ignore a position without declaring a name. After narrowing, named payload
fields are accessible on the variant subtype.

Patterns initially stop at one level; inspect nested values in another when. No recursive nested-pattern grammar or
general class inheritance is selected by sealed sums.

### Generic declarations

Support type parameters on named functions, data classes, sealed sums, and transparent aliases. Function parameters
precede the name, as in `fun <T> identity(value: T) -> T = value`. Type declarations use name-following parameters such
as Box<T>.

Infer type arguments from supplied arguments and expected types when unambiguous. Explicit forms such as
`identity<Int>(3)` resolve cases inference cannot settle. Compatible argument joins may infer Float from Int/Float, but
inference does not invent container-family copies or arbitrary Any fallback.

Unconstrained T may be nullable. `T: Any` excludes nullable arguments. Inline bounds and trailing where clauses express
nominal and capability requirements. Multiple requirements are conjunctive, for example `where T: Outcome, T:
Equatable`. Full declaration grammar and capability rules remain open.

User-defined generic types are invariant by default, with checked declaration-site `in` and `out` variance. Variance
uses subtyping and does not create conversion adapters. Star projections such as Box<*> permit only operations proved
safe from bounds. The development implementation derives field and method read types from usable upper bounds, including
bounds expressed through known arguments and multiple constraints. Covariant result layers may preserve these safe upper
views. Invariant hidden-dependent results remain conservative. A hidden-dependent callable input exposes `Nothing`,
which has no values. An explicit outer nullable form, such as `T?` or `List<T>?`, exposes `Nothing?`, admitting only
null.
A bare unconstrained `T` does not promise null acceptance, since its actual argument may be non-null. These input views
apply to methods, function-valued fields, and returned functions while preserving result bounds, suspension, and
variadic
shape. They introduce no conversion adapter or invented hidden argument.

Declared methods retain their defaults, so an inaccessible input may be omitted when the original declaration provides
a default. A variadic input of `Nothing` may receive an empty group. Defaults execute under the original reified callee
contract. Function values retain positional calls without default metadata. Other inputs requiring a present value of a
hidden type remain unavailable; generic-method constraints depending on hidden owner arguments remain conservative.

Reading an element from a projected collection through indexing, removal, traversal, or an entry never exposes a shared
standalone star type. Its unknown value is Any? until narrowed, preventing values from one hidden container from being
written into an unrelated hidden container. Expected projections do not constrain concrete generic inference. Container
copies retain the source's reified arguments in projected slots, including for empty collections.

Check generic bodies against their declared constraints at definition time, including unused definitions. Every
instantiation must satisfy the constraints. Retain runtime generic type arguments for the selected type tests. These
contracts do not choose monomorphization, erasure machinery, a runtime dictionary, or another lowering strategy.

## Conditionals and pattern matching

Steering: E06-E08, E13-E24, E32-E33, U20-U21, U31-U33.

If and when support statements and value-producing expressions. An if expression requires an else. Value-producing
branches use their final expression and need compatible result types.

When supports both subject-based `when value:` and subjectless `when:` forms. Branch headers use `case ...:` and
indented bodies. A when may have at most one else fallback, and it must be last.

Evaluate a subject once. Test branches in source order and run only the first match. Subjects and tests may suspend when
the enclosing context permits; retain completed evaluation across suspension. Overlaps are allowed; provably unreachable
later branches may receive warnings.

Subject cases support compatible values, null for nullable subjects, membership, and the selected type/variant patterns.
Comma-separated alternatives are tested left to right until one matches. Alternatives introducing bindings must all
declare the same names with compatible types, joined for the shared body.

A Boolean pattern guard follows a matched pattern, with payload names in scope: `case is Outcome.Success(value) if value
!= "":`. Evaluate the guard once under the enclosing suspension permissions; false continues to later cases.

`when val value = expression:` introduces a local immutable subject binding visible in tests and branch bodies. Subject
cases can refine null/type information where proof remains safe.

A value-producing when must cover every path; it may omit else only when coverage is proven. An unmatched statement when
executes no branch and continues. Guarded-case coverage and complete pattern grammar remain to be formalized.

## Narrative, choices, and suspension

Steering: T01-T24, E09, A04.

`prose:` introduces unquoted narrative. After structural indentation is removed, single newlines join a paragraph and
blank lines separate paragraphs. The explicit line-break form and residual-whitespace rules remain open.

Prose interpolation uses `${expression}`. It accepts non-suspending value expressions, including ordinary function
calls, yielding a directly renderable non-null String, Char, Int, Float, or Boolean. Other types and nullable values
require explicit conversion. Exact rendering formats remain open.

Inside prose, line-leading `@` after indentation introduces executable syntax. Conditional and loop bodies remain prose
by default; further statements and branch headers use the same prefix. `\${` escapes the interpolation introducer, `\@`
escapes a directive introducer, and `\\` produces one backslash.

### Choice preparation and continuation

Use `choice:` with `option "Label":` headers and indented bodies. Labels support the same non-suspending, renderable
interpolation as prose. After the selected body completes normally, execution continues after the choice.

Headers may include Boolean visibility and enabling conditions: `option "Open" if visible enabledIf allowed:`. False
visibility hides an option; false enabling displays it disabled.

Prepare the choice once in source order. Evaluate visibility first, then enabling and label for visible options. Hidden
options skip enabling and label evaluation. Non-suspending state changes are allowed. Retain the prepared results until
selection.

An optional else fallback handles having no selectable options. Without it, provably empty choices are compile errors
and dynamically empty choices are runtime errors.

Options are reusable by default. `once` consumes an option on selection and hides it on later visits. History is
playthrough-wide per source option site, including later scene visits and function calls. Stable site identities and
history-filter timing relative to effectful visibility tests remain open.

### Suspension effects

Functions that can wait for interaction carry `suspend` in declarations and function types. Scene bodies may suspend
automatically. Ordinary function bodies require the modifier. Suspending calls use ordinary call syntax and require a
context permitted to suspend.

```
suspend fun ask() -> Boolean:
    choice:
        option "Continue":
            return true
        option "Stop":
            return false
```

Ordinary function values may satisfy otherwise compatible suspend function types. A suspend function cannot satisfy an
ordinary function type. Suspending expressions preserve evaluation order and already-computed operands, arguments, and
temporaries without replay.

## Scenes and shared story state

Steering: M02-M07, M09-M15.

A scene header names the entry and typed inputs, for example `scene forest(danger: Int = 0):`. Inputs belong to the
current visit. Ordinary scene-body bindings are visit-local.

Scene references are typed first-class values: `Scene<Int, Float>` or bare Scene for zero inputs. Take a reference with
`::forest`. A reference-valued target requires all inputs explicitly and positionally. A named target retains the
existing named/default argument rules. Ordinary strings are not scene destinations.

`visit forest(danger = 3)` enters a fresh visit and returns Unit. `goto forest(danger = 3)` replaces the current visit
and abandons its active function frames while retaining earlier scene-call callers. If A visits B and B transfers to C,
C completes back to A. Transfers require a scene body or suspend function context.

On natural completion, a scene returns to a scene caller when one exists; otherwise it finishes the story. Use suspend
functions for value-returning routines.

At file/module scope, `shared val` and `shared var` declare persistent playthrough state. Initialize shared state once
before the first scene on a new playthrough with non-suspending initializers. Loading restores saved state without
replaying initialization.

Shared names resolve throughout their module. Every dependency must finish initializing before any part of the dependent
initializer begins. For shared val a = record() + b, initialize b before calling record(). Discover dependencies
conservatively through branches, function calls, and defaults; reject dependency cycles conservatively. Loading saved
state must not rerun this process.

The development compiler analyzes resolved instructions and all branches/defaults of reachable calls. Taking a function
reference does not invoke its body. An indirect call with an unresolved target includes all available ordinary
non-suspending functions, so some safe initializers may be rejected conservatively. Linking repeats analysis over all
linked module bodies, including source-free artifacts. Independent values use lexical module order and source
declaration order. Cyclic imports now resolve normalized declarations and inferred interfaces before lowering every
member, with shared dependencies checked against complete bodies. Cyclic artifacts validate the whole component; import
cycles do not exempt shared initialization cycles. Ordinary library bindings and shared declarations inside bodies still
need completion.

## Saves, legacy boundaries, and failure

Steering: T24-T26, S11-S12, S15, E35.

Initial saves are supported at fully prepared player-input waits. Preserve full suspended state: calls, locals, captured
bindings, computed temporaries, traversal snapshots, choice snapshots, shared state, and option history. Restore without
repeating completed evaluation.

Preserving values alone is insufficient when mutation makes sharing observable. Captures of the same variable must still
refer to the same binding after restoration. Two aliases of a mutable data instance or container must still observe each
other's writes. Separate bindings and containers must not accidentally become shared. Cycles must restore without losing
their relationships. These obligations follow from the selected aliasing and full-state contracts; they do not introduce
a reference-identity equality operator.

Choice snapshots and collection traversal snapshots must remain the already-prepared snapshots. Loading must not
re-evaluate a label, repeat an enabled-condition side effect, rebuild a traversal from a now-mutated container, or
replay an operand completed before suspension.

Restore only against the same compiled build and reject incompatible saves clearly. Save encoding, build identity,
validation, and graph representation remain open. Compatibility across game updates and migrations are outside the
initial save contract.

Unchanged legacy ChoiceScript retains its own scope, case, expression, and control-flow semantics. Cross-language calls
and shared-state access go through explicit typed bridges with declared interfaces and checked conversions. Unknown or
dynamic legacy values are never implicitly trusted as typed Bifoil values. The current development grammar declares
explicit interfaces separately from unchanged `.txt` source:

```bifoil
legacy var gold: Int = "gold"
legacy fun award(amount: Int = 1) -> Int = "helpers" label "award" result "gold"
legacy suspend fun ask() -> String = "questions" label "ask" result "answer"
legacy transfer fun enter(danger: Int = 0) = "forest"
```

The project manifest's optional `legacy_path` names a project-relative directory. The compiler embeds its unchanged
UTF-8 sources, validates literal destinations and labels, and records typed interfaces in reusable module artifacts.
Native ChoiceScript executes its own expressions, commands, scope, and case rules. This development profile accepts
primitive values, plain enums, and their nullable forms; `Unit` is also available as a return type. A plain enum crosses
as its exact declared case-name String, such as `"Happy"` for `Mood.Happy`. The expected nominal enum type determines
which names are valid; decoding never converts an arbitrary String to a trusted enum without checking it. Null remains
native null. Generic and other composite boundary representations remain unfinished. Numeric bridge values must be
actual finite native numbers; a native numeric string is not implicitly accepted as `Int` or `Float`. This matters
because ChoiceScript can store a literal number as text.

Ordinary wrappers retain Bifoil defaults, named arguments, effects, and function references. A last typed variadic
parameter is flattened from its fresh immutable list into native parameters. The native routine uses `*params` under its
original rules. A declared result is read from the named global only after native `*return`; boundary failure does not
undo completed native effects.

A legacy global is a live external proxy. It cannot be flow-narrowed as though it were an immutable local snapshot. A
local copy can be narrowed under the usual proof rules.

Bridge interfaces carry explicit suspension and transfer behavior. A legacy call that can wait for player input cannot
be treated as an ordinary non-suspending Bifoil function merely because its argument and return types match. Unknown
values require checking before typed use; checked conversion does not imply transactional rollback of earlier legacy
side effects. Ordinary bridges must return and reject native scene transfers and termination before they occur. The
explicit `legacy transfer fun` form is suspending, returns `Nothing`, accepts no result binding, abandons Bifoil callers
when entered, and lets native scene transfers and termination proceed. It cannot return to Bifoil.

Prepared native choices, page breaks, text input, and number input can suspend. Checkpoints retain the active native
scene, temporary variables, native call stack, statistics/navigation state, prepared labels/options or input bounds, and
the Bifoil continuation. Restoring into a fresh host does not replay preparation. A host-neutral graph encoding
preserves aliases, cycles, undefined properties, and special native numeric values. Further native UI/platform commands
and their persistence contracts require additional host acceptance.

Compile-time errors reject compilation. Checked runtime failures stop the story and report the original Bifoil source
location. This includes overflow, invalid indexing, failed checked casts, and other selected runtime checks. Catchable
language-level exceptions are deferred. Nullable operations that explicitly return null keep that behavior.

## Remaining specification work

The [detailed open-issue register](language-steering.md#remaining-design-work-and-holes) remains authoritative. This
completion sequence replaces a general list of questions with concrete drafting deliverables. It does not select new
language features or remove accepted ones. The subsequent implementation authorization covers the initial slice
described in the linked status document.

### Completion sequence

1. **Close the lexical and grammar draft.** Write layout/prose token rules and productions for declarations, types,
   expressions, directives, patterns, and imports. Publish the complete precedence table. Each unresolved choice must
   remain visibly proposed, with a concrete counterexample where two readings differ.
2. **Define module and runtime interfaces.** Specify the manifest and module interface model, named/default call
   metadata, generic identity, initialization dependencies, runtime requirements, and compatibility rejection rules. A
   client must be describable against an independently compiled dependency without reading its source.
3. **Define the resource acceptance protocol.** Publish the supported workload envelope, reference environment,
   accounting metric, full pipeline boundary, and failure reporting. Account for helpers and module preparation. Keep
   success claims blocked until an actual commissioned implementation is measured under that protocol.
4. **Write static-semantics judgments.** Separate subtyping from value conversion; define capability qualification,
   inference, overload selection, exhaustiveness, definite assignment, and narrowing. Cover recursion, captured writes,
   indirect calls, suspension, and the already-selected conservative rejection of unproved initialization.
5. **Define the suspended-state contract.** Describe live calls, shared binding cells, object/container aliasing,
   expression progress, prepared choices, traversal snapshots, scene callers, and build identity. A same-build restore
   must preserve those relationships and must not replay completed work.
6. **Complete operations and diagnostics.** Specify numeric/text conversions and rendering, collection methods, bounds
   timing, range edge cases, equality/key rules, and source-mapped failures. Record precise expected outcomes for the
   review cases below, then organize executable conformance inputs only when that work is commissioned.

These drafting and review tasks remain for the complete language. Rust, artifact encoding, runtime representation, and a
benchmark profile are selected for the initial slice, documented separately. Accepted first-milestone requirements
include reusable precompiled modules; staged work cannot silently drop that requirement.

### Review cases with outcomes already determined by steering

These are original specification review cases, not executed tests or proof of compiler correctness. Runtime cases refer
to runtime inputs; they do not force a decision about constant-folding every expression.

1. **Checked integer boundaries — N02, N06-N07.** A runtime Int multiplication whose mathematical result is outside the
   signed range fails. Minimum Int divided by −1 overflows; minimum Int remainder −1 is zero.
2. **Finite Float — N03.** Runtime floating division by zero or a non-finite result is an error. It cannot silently
   introduce an infinity into a Float binding.
3. **Fairmath endpoints — N09-N13.** The results of `0 %+ 0`, `100 %+ 0`, and `100 %+ 1` are respectively 1, 100, and
   99. Mixed binary operations and fairmath chains need explicit grouping; compound targets are captured and read once.
4. **Safe-call laziness — B11, B15-B16.** A null receiver/callable skips argument or index side effects and yields null.
   A present list receiver still reports an invalid index normally.
5. **Supplied arguments and defaults — A04, A06, F10-F11.** Capture the callable/receiver first, complete supplied
   expressions and conversions left to right, then evaluate omitted defaults in parameter order. Later argument effects
   cannot retroactively change an earlier completed copy.
6. **Duplicate map keys — D14, D29.** A dynamically duplicated key fails before its value expression executes. Any
   effects from previously evaluated entries have already occurred.
7. **Presence versus nullable lookup — D07, D19.** A stored null and a missing key both look up as null, but key
   membership distinguishes them.
8. **Copying versus mutable invariance — D21-D22, D25.** List<Int> may convert to an independent MutableList<Float>.
   MutableList<Int> does not implicitly become MutableList<Float> through an intermediate copy chain.
9. **Shallow sharing — D05, U05, U29.** Aliases of a mutable container observe indexed replacements. A copied container
   has independent container contents; referenced mutable element objects retain their existing sharing semantics.
10. **Stable keys — D12, G09-G10.** An immutable container holding a mutable composite does not become a stable key
    merely because the outer container is immutable.
11. **Empty iteration and ranges — D16, R04.** Iterating an explicitly typed empty List performs no iterations. The
    constant range `5..<5` is an error; the same empty ascending range from dynamic bounds fails at runtime.
12. **Loop condition initialization — C07-C08.** A direct do-body declaration is visible to the trailing condition, but
    a continue path that reaches a read without initializing it makes the program invalid.
13. **Exact numeric equality — E03, E28.** `3 == 3.0` is true through approved widening; `3 === 3.0` is false.
14. **Runtime generic tests — G15.** An empty List<Int> stored through a universal value still supports a List<Int> type
    test. Testing it as List<Float> cannot perform numeric conversion to manufacture a match.
15. **Definition-time generic checking — G08-G10.** An unused generic body performing an unsupported operation is an
    error. Calling it nowhere does not bypass its declared capability requirements.
16. **Overload tie-breakers — F28-F29, F42.** Conversion dominance precedes variadic/default preferences; an otherwise
    tied generic/nongeneric pair chooses the nongeneric overload only at the final selected tie-breaker.
17. **Enum-name conflicts — U13, U24.** A bare name that can denote both a visible binding and the expected enum case is
    a name conflict requiring qualification.
18. **Guard continuation — E18-E20, E32-E33.** A matching pattern with a false guard continues to later cases. A when
    has at most one else, after every case. A failed guard does not itself execute that branch body.
19. **Current captured state — F17-F18, F21, F43-F44.** Two closures capturing the same var observe and update one
    shared binding. A later method-reference receiver reassignment does not retarget a previously created bound
    reference.
20. **Effect widening — T08, T15, T20-T22.** An ordinary function may satisfy a compatible suspend function type; the
    reverse is invalid. Ordinary function bodies cannot hide a potentially suspending call.
21. **Scene transfer — M12-M13.** If A visits B and B transfers to C, C's natural completion returns to A. Active B
    function frames are abandoned, while earlier scene callers remain.
22. **Prepared snapshots after load — D16, T14, T24-T25.** Saving at an input wait and restoring the same build retains
    choice and traversal snapshots, computed operands, and shared captured state. It does not repeat preparation
    effects.
23. **Build compatibility — T26.** A save from an incompatible compiled build is rejected explicitly. Cross-update
    migration is not inferred merely because scene names or source paths still match.
24. **Typed legacy boundary — S12, E35.** An unknown legacy result is checked before typed use. A required conversion
    that fails cannot be silently trusted; the selected runtime failure policy reports the Bifoil source location.
25. **Independent artifacts — S10, F09-F12, A05, G15.** A source-free imported dependency must preserve direct-call
    names/default behavior, the function-value interface, and runtime generic/effect information.
26. **Compiler resource failure — S13-S15.** An out-of-envelope or budget-failed compilation reports failure. A helper's
    memory cannot be excluded to make an aggregate cap appear to pass.

### Cases that still need a formal rule

- Exact equality across covariant static views and retained runtime generic identities.
- Bare member lookup, lexical binding visibility, and no-shadowing inside methods and generated constructors.
- Alias-preserving cyclic equality for unordered sets/maps, including recursive capability qualification.
- Safe narrowing after a captured write, indirect call, or suspension that can invalidate a previous proof.
- Type-level proof of initialization for recursive or escaping functions with delayed captured bindings.
- Final-step overflow and the requested reference behavior for very large stepped progressions.
- Broader shared-initializer dependency proof and inference interactions across cyclic module interfaces.
- Guarded-pattern exhaustiveness, Unit-context early returns, and combined conversion/overload inference.

Document a proposed rule and its distinguishing cases for each item. Do not silently promote a working interpretation to
an accepted decision or claim that unresolved cases pass. The next drafting step is the lexical/grammar chapter,
followed by extending the module/runtime interface contract. The initial slice has separate implementation tests and
measurements; full-language conformance and performance remain unverified.

[r1]: https://go.dev/doc/gc-guide
[r2]: https://docs.kernel.org/admin-guide/cgroup-v2.html
[r3]: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information

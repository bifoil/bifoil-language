# Binding initialization and flow proofs

This document specifies conservative flow checking for B06-B10 and F19-F21, including delayed assignment, captured
reads, recursive calls, and invalidated refinements. It describes sufficient static proofs. A program whose safety
cannot be proved is rejected; source ordering, a successful run, or an assumed callback invocation is not a substitute
for proof. Namespace policy and shared-startup dependency analysis remain separate contracts.

## Declarations and state

Every lexical declaration has an identity distinct from its source spelling. The type environment maps that identity
to its declared or inferred type, mutability, owning function, and declaration scope. A local variable becomes visible
at its declaration. A named local function is callable throughout its block, but its body resolves variables in its
declaration environment. Hoisting its callable name does not hoist later variable names into that environment.

For each visible binding b at a reachable point, track:

- D(b): initialized on every reaching path.
- P(b): initialized on at least one reaching path.
- N(b): a proven refinement of its declared type, when available.
- H(b): proven member/index/key facts, each with its own stability conditions.
- C(b): retained capture and callable requirements of its current value.
- E(b): its mutable cell can be observed through a published reading capture.

D implies P. Parameters and declarations with initializers begin with D and P true. A declaration without an initializer
requires an explicit type and begins with D and P false. A new call creates fresh parameter and local bindings; a new
loop iteration creates fresh body-local and iteration bindings. The declared type does not change with later writes
or with a narrower current value.

An inferred initializer type uses the selected expression, scalar/nullable joins, contextual literals, and generic
inference rules. Missing information requires an annotation. Bare null, empty or all-null collections, unrelated
uncontextualized branch values, and unanchored recursive results do not acquire an arbitrary Any type.

## Reads and writes

A direct local read requires D(b). Reading a field or indexed element first requires a valid initialized receiver and
index/key expression; it does not initialize its containing binding. A compound update reads its target and therefore
requires initialization before its right operand runs.

An ordinary store evaluates target receivers and indexes/keys once, from left to right, then evaluates and converts
the right operand, then writes. A binding store requires an approved conversion to its existing static type. For a val,
P(b) must be false before evaluation and remain false after the right operand's effects. Checking only before that
operand would miss an assignment performed inside a value-producing branch of the operand itself.

A successful binding store sets D and P true, replaces C with the stored value's requirements, and retires refinements
invalidated by the changed binding. A field or collection store invalidates applicable heap facts; it does not rebind
the receiver. `val` does not freeze a referenced mutable object. Publication checks described below also apply when a
store makes a callback or composite value observable outside the currently checked scope.

## Reachability and branch joins

Let Paths be the normally completing reachable alternatives at a join. For each binding visible at the join:

```text
D_join(b) = AND over Paths of D_path(b)
P_join(b) = OR  over Paths of P_path(b)
```

A refinement is retained only when every reaching path supports the same proof. Retained capture requirements and
publication facts accumulate across alternatives. Bindings declared within an alternative leave lexical scope at its
exit; surviving closures retain their original cells rather than resolving a later declaration of the same spelling.

An absent if alternative, a possibly unmatched statement when, and a skipped lazy operand contribute an unchanged
entry path. Safe access/invocation/indexing, `&&`, `||`, and `?:` therefore cannot make a conditionally skipped write
definite. A proven constant condition may eliminate its impossible execution path. Unreachable source still undergoes
ordinary syntax/type checking; it cannot contribute executed writes or published values.

Return, break, continue, and goto have no normal successor at their occurrence. A valid transfer contributes its state
only to its actual destination: function completion, the selected loop exit/backedge, or the selected scene transfer.
Paths that never reach a join do not weaken definite initialization or invent a possible write at that join.

For example, both of these are valid:

```bifoil
fun select(flag: Boolean) -> Int:
    val result: Int
    if flag:
        result = 3
    else:
        result = 4
    return result

fun finish(flag: Boolean):
    val result: Int
    if flag:
        result = 3
        return
    result = 4
```

Removing select's else makes its final read invalid. Removing finish's early return makes its later assignment invalid.
These outcomes follow from D and P separately; a single initialized flag cannot represent both obligations.

## Loops and scopes

A pre-test loop may execute zero times unless the checker establishes otherwise. A for traversal can establish at least
one iteration only from a sufficient nonempty-iterable proof. A do body executes before its first condition. Direct
do-body declarations remain in scope for that condition, with initialization required on every path that reaches it,
including continue paths.

Normal iteration ends and continue destinations are backedges. An outer delayed val cannot receive another possible
write on a reachable repeated iteration. An assignment followed by a proven terminal break/return may be accepted;
the same assignment on a normal or continue backedge is rejected when it can execute again. Break states join the
corresponding loop's normal exits, including labeled breaks. A labeled transfer cannot cross a function boundary.

Iteration-body declarations are fresh on each iteration, so initializing a body-local val once per iteration is valid.
Escaping closures retain each iteration's distinct cell. A later declaration can reuse a name after its earlier block
has ended, but cannot replace the earlier declaration's retained cell or proof identity.

## Captured reads, call profiles, and recursion

A local function may refer to a visible binding that has not yet been initialized. Checking its body records the
obligation rather than assuming that declaring the function executes the read. A plain captured write retains the
cell's address without reading either its previous contents or callbacks stored in that previous value.

A callable's requirements distinguish its body from each parameter's default expression. For a selected named call:

```text
Required = BodyRequirements
         UNION Requirements(default i) for every omitted parameter i
```

Resolve and capture the callable before supplied arguments. Evaluate and convert supplied arguments in source order
before discharging requirements at the call. An argument can initialize a captured dependency before the invocation;
a transferring argument can make the invocation unreachable. Omitted defaults then execute in parameter order under
the already selected default rules. Supplying a parameter excludes that default's reads and publication effects.

A function value exposes explicit positional inputs, without names or defaults. Taking, returning, or invoking such a
value therefore does not activate its declaration's unused defaults. Its actual body requirements remain mandatory.
An unused default-only captured cell may remain uninitialized, including across a checkpoint, when the value's callable
interface cannot execute that default.

At every reachable reading call or publication boundary, follow the retained requirements transitively. The lookup is
restricted to each capture's declaration scope. Check the resolved cell's initialization before following its deferred
dependencies; track visited scoped requirements so recursive callable graphs terminate. Revisiting a dependency does
not establish a missing initialization fact or execute a write. Unselected overloads cannot lend their writes or their
defaults to the selected callable. When an indirect deferred profile cannot uniquely select an overload, all still
possible compatible reads remain obligations.

Known direct helpers may establish definite captured writes only after a checked must-analysis proves those writes on
every normal return. Recursive or opaque calls do not imply such a fact merely because another call might eventually
write the cell. Captured val initializers additionally require a proven invocation shape that cannot perform a second
write to the same cell. Multiple exclusive source sites may be valid; counting syntactic call sites alone is not a
proof of either repeated or single execution.

The development compiler bounds optional helper-write analysis. If that proof is unavailable or exceeds its analysis
budget, it retains conservative obligations or rejects a required captured-val initializer; it never assumes success.
Ordinary compiler memory/deadline failures likewise cannot yield a successful build.

## Escaping values and lexical lifetime

A closure can escape through a return, argument, container, data field, shared store, or another closure. Its retained
read dependencies must be initialized when that publication can expose them. Copies, casts, projected views, and
container nesting do not erase the obligation. Retiring a local scope expands surviving callable requirements before
its source names disappear and requires ready reads of the cells leaving that scope.

A reading capture of a mutable cell keeps an obligation on the cell itself. A later replacement of that cell's value
must discharge the replacement's retained reads before an opaque observer can see it. A write-only capture does not
expose the previous contents; its own stored values still undergo the ordinary publication checks. Local proof metadata
must not mistake this distinction for a lifetime change: both captures retain the same cell at runtime.

Captures of one var observe current shared state. Different calls and different iterations retain distinct bindings.
Preserving a cell for a closure does not make its source name visible outside its lexical block or permit shadowing a
currently visible binding. Independently compiled functions and restored checkpoints preserve the same relationships.

## Refinement invalidation

Null and type tests establish refinements only on paths where the tested value is known to satisfy them. A binding
write retires proofs about its previous value. Heap facts depend separately on receiver identity, member mutability,
index/key stability, and container mutability. An immutable outer binding alone does not make mutable descendants safe.

Calls, defaults, callbacks, and suspension can change captured/shared mutable state. The current conservative checker
invalidates mutable-binding and transient heap refinements at ordinary calls and repeated-loop boundaries. Selected
builtins invalidate according to their classified heap effects. Immutable bindings and permanently stable paths may
retain facts. Function-definition environments cannot inherit later tests that a forward call might bypass.

A when subject is evaluated once. Its captured subject can be refined independently of an original mutable binding;
the original receives a related proof only while their equality of reference/value remains established. Effectful case
tests, aliasing writes, or suspension cannot resurrect an invalidated relationship. Alternative patterns contribute a
shared refinement only when every matching alternative supports it. After an uncertain effect, explicitly snapshot or
test the value again.

This permits conservative rejection when a finer interprocedural effect proof might be possible. It does not permit
retaining an invalid proof or assuming that a currently successful callback leaves shared state unchanged.

## Implementation and evidence

[Binding state](../bifoil-compiler/src/compiler/bindings.rs),
[assignments](../bifoil-compiler/src/compiler/assignments.rs), and
[flow joins](../bifoil-compiler/src/compiler/flow.rs) own declaration facts and their transfers.
[Loop lowering](../bifoil-compiler/src/compiler/loops.rs) owns exit/backedge destinations.
[Capture requirements](../bifoil-compiler/src/compiler/captures.rs),
[call profiles](../bifoil-compiler/src/compiler/captures/requirements.rs),
[publication guards](../bifoil-compiler/src/compiler/captures/escapes.rs), and
[call lowering](../bifoil-compiler/src/compiler/calls.rs) keep deferred reads tied to their actual call interface.
[Helper must-analysis](../bifoil-compiler/src/compiler/capture_initialization.rs) and
[protected initializers](../bifoil-compiler/src/compiler/single_use_initializers.rs) supply optional direct-call proofs.

The [source-free initialization case](conformance/cases/binding-initialization-source-free-checkpoint/main.bfl) checks
exclusive writes, forward helpers, fresh iteration cells, defaults, escaping readers, and restoration with an unused
default-only capture. The [scope-reuse case](conformance/cases/binding-scope-reuse-source-free-checkpoint/main.bfl)
checks distinct retained declaration identities after scopes end. Paired failures in the
[foundation index](conformance/foundations.json) reject missing reads, repeated writes, and nested shadowing.
[Native flow regressions](../bifoil-compiler/src/tests/flow.rs) and the remaining conformance indexes cover lazy paths,
loops, recursive callbacks, heap publication, invalidated refinements, and source-free callers.

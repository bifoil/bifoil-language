# Existential projection views

G07 permits a star argument to hide a concrete generic argument while retaining operations proved safe from its
bounds. A projection does not select a concrete argument, replace the object's construction type, or copy its contents.
Known sibling arguments remain known. Runtime tests/casts, saved references, and checkpoints retain reified identities.

## Upper reads and lower inputs

Let A be a hidden argument ranging over the types allowed by its declaration. A readable view must be an upper type
of every admitted A. An input view must be a subtype of every admitted A. Those directions differ: an upper read type
does not grant permission to store every value of that type.

The unconstrained upper view is Any?. Ordinary declared bounds can improve it, including bounds through known or
hidden siblings. A non-null proof removes null. Capability requirements such as Equatable or StableKey prove operation
eligibility rather than supplying a runtime value type. Recursive or unrepresentable bounds retain a conservative
upper view; they do not fabricate a concrete type or a general intersection.

The direct lower view of a hidden argument is Nothing. Applying nullability produces Nothing?, which admits null.
This permits null inputs for an explicitly nullable position even when the receiver argument is hidden. Nullable
capability of A alone does not prove that A itself contains null: Box<*> can still hide a non-null Int argument.

Propagate the required direction structurally:

- Covariant positions retain the current direction. Immutable List/Set elements and Map values use their selected
  covariance; Map keys remain invariant.
- Contravariant positions reverse the direction.
- Callable parameter positions reverse the direction, while results retain it. Preserve suspension and variadic shape.
- Invariant hidden positions retain a star for reads. Inputs requiring a particular invariant hidden argument have no
  ordinary value available, represented by Nothing.
- Unrelated known positions retain their exact type. Projection does not weaken an independent mutable field or
  discard an owner's known generic parameter.

A projected result must remain well formed. If widening would lose a required capability or violate a nominal bound,
retain a checked star position or a sound broader view. A valid Set<*> retains the guarantee that its hidden element
type was a stable key; that does not make arbitrary Any values eligible for every comparison or input.
The [capability contract](capability-semantics.md) defines the separate recursive proof.

## Fields and mutation

A field read uses the upper view. A mutable field assignment uses the lower input view, independently of its readable
type. Preserve declaration mutability and privacy: a fixed or inaccessible field does not become writable merely
because a proposed value would fit.

~~~bifoil
data class Box<T>:
    var value: T?
    var values: List<T>
    var callback: (T) -> String

fun clear(box: Box<*>):
    box.value = null
    box.values = []
    box.callback = (item: Any?) => String(item)
~~~

These writes are safe for every hidden T. The first uses Nothing?. The second constructs an empty List<Nothing>,
which fits every admitted List<T> by covariance. The callback accepts every possible hidden input. A concrete Int
write, nonempty List<Int>, or callback accepting only String would assume a hidden argument and is rejected.
A MutableList<T> field cannot accept an arbitrary replacement through an invariant hidden argument.

Reading after a permitted write still follows the declared upper view. Projection does not rewrite the original
object's type argument to Nothing or Any. Other aliases retain the instance and observe the mutation. Flow proofs use
the underlying field's actual mutability; an upper view cannot turn a mutable field into permanently stable data.
Writes invalidate affected alias refinements under the [ordinary flow rules](binding-flow-semantics.md).

Assignment still captures its receiver before the right operand. If the right operand suspends or reassigns the
receiver's source binding, the eventual write targets the captured instance. Save/restore retains that address and
completed evaluation. Runtime cells also check their retained concrete field types.

## Methods and generic bounds

Method input positions use lower views and return positions use upper views. A callback that consumes a hidden value
must accept the corresponding upper input view. A function that produces a hidden argument cannot substitute an
arbitrary concrete value. Signature projection never creates numeric-conversion or container-copy function adapters.

Omitted declared defaults are checked in their original definition context. A projected default-only call does not
require the caller to manufacture a hidden value. Empty variadic groups are safe; nullable hidden groups can receive
null elements under the Nothing? view. Bound function references retain the same safe exposed signature and their
captured instance.

A caller-selected method type argument must satisfy every original bound for every possible hidden receiver argument.
Project each hidden-dependent bound in the input direction. For a method with U: T, the projected sufficient bound is
U: Nothing. For U: T?, it is U: Nothing?. Thus explicit Nothing and Nothing? instantiations can remain usable:

~~~bifoil
data class Box<T>:
    val value: T
    fun <U: T> unit() -> Int = 1
    fun <U: T?> maybe(input: U) -> Boolean = input == null

fun query(box: Box<*>) -> Boolean = box.maybe<Nothing?>(null)
~~~

Choosing Int would not prove either hidden-dependent bound and is rejected. Bounds alone do not invent an unobserved
generic argument; existing explicit-argument/inference rules still apply. The method retains its original parameter
identities, checked body, and concrete receiver arguments at execution. Projection changes the safe calling interface.

## Checking and persistence

Each projection query keeps distinct read/input contexts. Shared type nodes can appear in both directions without
reusing the wrong proof. Alias expansion and generic substitution retain their owner identities. Upper-bound traversal
tracks active parameter identities; completed type-view results are reusable only within that unchanged receiver query.
Finite implementation guards are separate from whole-language capacity acceptance.

The existing v3 instructions express these operations; the module format remains v4. This source-checking improvement
requires no new wire fields or reinterpretation of old executable programs. The runtime checks the same retained
object cells and callable signatures as before. Suspended operands, aliased fields, method references, and generic
arguments survive same-build checkpoints without replaying effects.

## Evidence

The [source-free projection cases](conformance/projected-fields.json) remove helper sources before compiling clients.
They combine a captured assignment address with a suspending right operand, nullable and empty-container writes,
callbacks, dependent bound reads, generic method bounds, saved bound references, and concrete identity tests. Paired
errors isolate immutable/private fields, wrong hidden values, invariant containers, narrow callbacks, and invalidated
alias guards.

[Native field regressions](../bifoil-compiler/src/tests/projected_field_writes.rs) assert upper read types and safe
lower inputs. Existing [projected-input tests](../bifoil-compiler/src/tests/projected_inputs.rs) cover defaults,
varargs, nested variance, capabilities, and mutable alias proofs. [Projection graph
tests](../bifoil-compiler/src/declarations/projections/tests.rs) check direction-sensitive shared graphs, bounds, nulls,
and preserved effects. Current source-free and runtime checks remain separate from target-scale resource,
production-host, and release acceptance.
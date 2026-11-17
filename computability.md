# Computability of the selected language

This review concerns the abstract semantics in the [steering record](language-steering.md), rather than the capacity
of a particular compiler build or runtime host. It establishes the checklist's semantic computability obligation;
it does not establish resource compliance or complete implementation.

## Storage model

Signed 32-bit integers alone provide finitely many values. Their width therefore cannot establish or refute Turing
completeness by itself. The selected language also provides heap-allocated nominal instances, nullable references,
reassignable bindings and fields, Boolean conditionals, and repeated execution. Its abstract semantics do not prescribe
a fixed total number of instances or a fixed call-depth limit. Runtime allocation failures and development guards are
implementation limits, separate from that abstract model.

A finite-alphabet tape can use linked cells without measuring its length or indexing it with an ever-growing Int:

```bfl
data class Cell:
    val symbol: Char
    val tail: Cell?
```

A stack is a nullable Cell reference. Null denotes an empty stack. Pushing allocates `Cell(symbol, head)` and replaces
its head binding. Popping a non-null head reads its symbol and replaces the head with its tail. These operations
require no unbounded arithmetic. Fixed field bindings do not prevent replacing the separate stack-head binding.

## Tape simulation

Represent the tape by a current symbol and two linked stacks. The left stack contains cells to the left of the head,
nearest first. The right stack contains cells to its right, nearest first. Outside the finite stored portion, every
cell contains the blank symbol.

A write replaces the current symbol. A move to the right pushes that symbol onto the left stack, then pops the right
stack into the current symbol. An empty right stack supplies a blank instead. Moving left performs the symmetric
operation. Each operation uses a fixed number of field reads, assignments, tests, and allocations. Cells can retain
blank symbols without changing the represented tape.

The invariant follows directly. A right move preserves the old current cell as the nearest cell on the new head's
left and selects the old nearest right cell as current. The left-move argument is symmetric. A write changes exactly
the symbol under the head. Every finite transition sequence therefore has exactly the same tape contents, head
position, and finite control state as the simulated machine.

A Turing machine has a finite state set and finite alphabet. Its transition table can be expressed with enums or
bounded state values and `when` branches. Each branch writes a symbol, moves the head, and chooses the next state.
A `while` loop repeats transitions until the halt state. No transition needs tape length, an unbounded numeric index,
unsafe casts, runtime code generation, general inheritance, or native machine-code output.

Consequently, under the selected abstract model with unbounded available heap, Bifoil can simulate an arbitrary Turing
machine one transition at a time. This provides the required semantic Turing-completeness argument despite bounded Int.
It does not assert that a physical host can execute an infinite computation or store an infinite tape.

## Executable witness and limits of the evidence

The original [linked-tape fixture](conformance/cases/linked-tape-source-free-checkpoint/helpers.bfl) implements both
tape
movements and a small unary-increment machine using these operations. Its
[client](conformance/cases/linked-tape-source-free-checkpoint/main.bfl) starts with `11`, runs until a blank, writes a
third `1`, and returns to the first cell. It then saves at a prepared choice, restores the same build, moves onto the
blank at the left edge, and moves back. The asserted output is `111`, `_|111`, and `111`.

The conformance runner independently compiles the helper, removes its source, compiles the client, and restores at the
wait. Those assertions demonstrate the implementation operations and checkpoint relationships used by the argument.
The fixture is a finite witness, rather than a test that can establish universality by running every machine.
The invariant and transition construction above supply the general argument.

Development compiler depth, byte, module, and instruction guards and runtime heap/call/checkpoint limits still apply.
They are finite implementation envelopes. Compiler resource limits below 250,000,000 bytes and incremental compilation
under ten seconds concern building supported programs; they do not bound their abstract number of execution steps.
The [capacity checklist](language-implementation-checklist.md#capacity-architecture-and-the-resource-contract) and
[implementation status](implementation-status.md) retain those separate obligations. Native story binaries and
self-hosting remain unselected deliverables.

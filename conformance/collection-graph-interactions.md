# Collection and data graph interactions

The [combined client](cases/collection-graph-source-free-interactions/main.bfl) uses independently compiled
[generic declarations and helpers](cases/collection-graph-source-free-interactions/helpers.bfl). Their source is
removed before compiling the source-free client. Companion sourceful cases use the same inputs with those sources
present. Both output modes format the source, verify formatter idempotence, and restore every prepared input wait
before continuing.

## Combined assertions

The same client combines the following contracts:

- Two separately allocated cyclic nominal graphs compare structurally equal, including under exact equality. A later
  field/payload mutation makes them unequal. Equality does not depend on their reference-sharing layout.
- A generated shallow copy has an independent reassignable field while retaining the original next-node and mutable
  payload references. Updates through aliases remain visible after two checkpoints.
- A mutable map stores nullable cyclic nodes under stable generic keys. An immutable map copy and a nested generic
  alias retain those node references while owning an independent container.
- Replacing a map value keeps its key's position. Removing and reinserting the key moves it to the end; the earlier
  copied map keeps its original order. The source-free iterator reads checked entry `.key` and `.value` fields.
- Equal nominal keys coalesce in a set, while a different ordered List payload remains distinct. A stored null map
  value is distinguished from an absent key through membership.
- Projected keys retain sufficient declared capability bounds for storage and safe runtime type tests. A concrete
  `Key<List<Int>>` retains its runtime argument through an Any binding and checkpoint restoration.
- Numeric set widening, family copying with widening, and subsequent mutable updates preserve independent containers.
  Nullable copying also widens nested immutable List layers and retains their reified Float identity.

A generic consistency property also ties equality to set size, map update size, and map lookups for projected nominal
keys, nested numeric keys, and floating signed zeros. It requires those operations to agree without choosing the
equality result for an otherwise unresolved pair of exposed views.

The exact comparisons use matching map construction types and actual numeric-container conversions. This case does
not decide exact equality through a covariance-only view or add nominal map-key conversion rules.

## Paired failures and indexes

[Mutable generic key arguments](cases/collection-graph-unstable-argument-source-free-error/main.bfl) fail the retained
StableKey bound after source removal. [Mutable cyclic node
keys](cases/collection-graph-cyclic-key-source-free-error/main.bfl)
are rejected even though those same node types are valid map values in the combined client. Shallow immutable field
bindings do not make mutable descendants stable.

[An unsafe projected read](cases/collection-graph-projected-read-source-free-error/main.bfl) cannot manufacture an Int
from a hidden payload whose StableKey bound does not establish that type. The unused function body is checked at its
definition.

[The dynamic duplicate-key case](cases/collection-graph-duplicate-nominal-key-source-free-error/main.bfl) constructs two
equal nominal keys through precompiled functions. The first value expression renders `first`; the second key is rejected
before its value expression can render `second`. This checks structural key equality and the selected early rejection
order through the actual compiler/runtime boundary, rather than constant folding.

The runtime's [index controls](../../bifoil-runtime/test/collection-index.test.mjs) and
[checkpoint key controls](../../bifoil-runtime/test/checkpoint-heap.test.mjs) complement these source cases. They cover
compatible primitive buckets, conservative composite matching, mutation/restore rebuilding, and invalid saved keys.
Together the controls keep qualification, equality, insertion coalescing, scalar widening, and transient indexes
aligned.

## Compiler-generated large ring

[The larger client](cases/compiled-large-cyclic-source-free-checkpoints/main.bfl) constructs 20,000 generic nodes
through
compiler-generated instructions. Each node has a value, a shared mutable payload, a nullable next reference, and a
reassignable stamp. The client closes the ring and retains two aliases to its root.

Four input waits are restored before selection. Each round mutates through the aliases, visits all nodes, checks the
sum `199990000`, and observes the root stamp and shared payload size. The final cursor returns to the original root.
This exercises active allocation and automatic collection during construction and traversal, along with source-free
nominal metadata, prepared loop state, and checkpoint serialization.

The independent [runtime graph control](../../bifoil-runtime/test/checkpoint-large-graphs.test.mjs) additionally checks
every node and alias, checkpoints exceeding 8 MiB, and explicit reclamation after each restore. The compiler-generated
case complements that protocol-level regression; it does not replace it.

## Reproduce the checks

Run the compiler repository's conformance tool with explicit paths:

```sh
uv run --no-project python /path/to/compiler/tools/run-conformance.py \
  --compiler /path/to/bifoilc \
  --runtime /path/to/runtime \
  --node /path/to/node \
  --format-sources --jobs 4 \
  --cases conformance/nominals.json \
  --only collection-graph-source-free-interactions \
    compiled-large-cyclic-source-free-checkpoints \
    collection-graph-unstable-argument-source-free-error \
    collection-graph-cyclic-key-source-free-error \
    collection-graph-projected-read-source-free-error \
    collection-graph-duplicate-nominal-key-source-free-error \
    collection-graph-source-interactions \
    compiled-large-cyclic-source-checkpoints
```

Run again with `--package`. The runner creates and removes isolated projects; the original sources and supplied engine
remain unchanged. These cases require no native ChoiceScript bridges. Full-corpus legacy cases still require an
explicit engine path.

These are acceptance controls within the admitted development profile. They do not establish complete type/equality
contract closure, target-scale source capacity, compiler resource compliance, production persistence, or release
readiness.

# Collection operations and copy timing

This contract completes the operation signatures, Entry interface, and evaluation timing left open under D15/D20,
E10/E11, and U29. It follows the accepted container mutability, shallow sharing, named-argument, receiver-first,
supplied-argument-first, and snapshot-traversal rules. It introduces no deep copy, general tuple destructuring,
user-defined operator, or reference-identity comparison.

## Common members

Every List, Set, or Map has an Int `size` property and a non-suspending `isEmpty() -> Boolean` method. A String retains
its separate scalar `length`. Lists are indexed by nonnegative Int; maps are indexed by their key type. Set values
cannot be indexed. List lookup returns T; map lookup returns V?, with the same null for absence and a stored null. `key
in mapping` or the map-key method below distinguishes key presence.

The following methods retain ordinary argument conversions and evaluation. K must satisfy StableKey. A `contains`
operation requires supported equality for its element/key type. A named direct method call uses the names shown. Methods
through function values expose positional parameter types and no names/defaults.

| Receiver family | Method | Result |
| --- | --- | --- |
| List<T> or MutableList<T> | `contains(element: T)` | Boolean: at least one equal element exists. |
| Set<T> or MutableSet<T> | `contains(element: T)` | Boolean: an equal member exists. |
| Map<K,V> or MutableMap<K,V> | `contains(element: K)` | Boolean: an equal key exists. |
| Map<K,V> or MutableMap<K,V> | `containsKey(key: K)` | Boolean: an equal key exists, even when its value is null. |

`containsKey` is a map member; List and Set do not expose it. New source uses `key`, including an expected-type enum
case or an argument requiring approved scalar conversion. Earlier compiled builtin calls carrying the name `element`
remain executable; that compatibility spelling is not an additional source parameter name. V1/v2 profiles retain their
stored interface. Unknown names, duplicate bindings, and named calls through a function value remain errors.

Generic inference retains G14: it does not discover missing type arguments by inventing a family copy. Supply those
types explicitly or pass an explicitly copied value such as `mapping.toMap()`. Once the target signature is known,
ordinary approved argument copies still apply. A corresponding rejection control preserves this distinction.

## Contextual construction

Without an expected type, nonempty literals construct immutable List, Set, or Map values and join compatible contents.
Approved scalar/nullable widenings may establish that join; unrelated types do not acquire an arbitrary Any fallback. An
expected type supplies element/key/value types and may request mutable construction. A mutable prefix explicitly
requests a mutable literal; an outer immutable target then uses the separately approved family-copy conversion.

Empty lists require an expected element type. Empty braces require enough context to distinguish Set from Map and supply
their arguments. All-null contents also require sufficient expected types. An explicit expected List<Any?> can accept
heterogeneous values; Set elements and Map keys still require StableKey and cannot use an unknown Any type.

List and set elements evaluate/convert left to right. For a map entry, evaluate/convert its key, reject an equal prior
key before evaluating that entry's value, then continue in source order. Sets coalesce equal members after evaluating
their element expressions, retaining first-insertion order. These literal rules do not turn an existing mutable value
into an inferred immutable type by fabricating a family copy during a compatible-type join.

## Mutating members

Only a mutable family exposes container-changing methods. An immutable binding may still refer to a mutable container;
`val` prevents binding reassignment and does not remove these methods. Immutable containers permit no container changes
through another alias. Mutating descendants retain their own selected semantics.

| Receiver | Method | Result and behavior |
| --- | --- | --- |
| MutableList<T> | `add(element: T)` | Boolean true; append one element. |
| MutableList<T> | `insert(index: Int, element: T)` | Unit; insert before index, permitting index == size. |
| MutableList<T> | `remove(element: T)` | Boolean; remove only the first equal element, or return false if absent. |
| MutableList<T> | `removeAt(index: Int)` | T; remove and return the indexed element. |
| MutableSet<T> | `add(element: T)` | Boolean; append a previously absent member and return true, otherwise return false. |
| MutableSet<T> | `remove(element: T)` | Boolean; remove an equal member and return true, otherwise return false. |
| MutableMap<K,V> | `put(key: K, value: V)` | V?; return the previous value or null when absent, then retain the new value. |
| MutableMap<K,V> | `remove(key: K)` | V?; remove the entry and return its value, or null when absent. |
| Any mutable family | `clear()` | Unit; remove all contained elements/entries. |

Set insertion leaves an existing equal member in its current position. Map replacement retains the key position; removal
followed by insertion moves it to the end. Removing an absent member/key does not change order. A previous nullable map
value is distinguished from absence by a separate presence test before mutation.

`items[index] = value` replaces one list element; it does not insert or grow the list itself. `mapping[key] = value`
inserts or replaces an entry and produces no expression result. Plain/compound assignment retains statement-only syntax.
All updates enforce the receiver's declared element/key/value types and applicable conversions.

## Explicit container copies

Each corresponding family supports the methods in this table; these methods take no arguments. They create an
independent outer container, even when the requested family equals the source family.

| Source family | Immutable result | Mutable result |
| --- | --- | --- |
| List<T> or MutableList<T> | `toList() -> List<T>` | `toMutableList() -> MutableList<T>` |
| Set<T> or MutableSet<T> | `toSet() -> Set<T>` | `toMutableSet() -> MutableSet<T>` |
| Map<K,V> or MutableMap<K,V> | `toMap() -> Map<K,V>` | `toMutableMap() -> MutableMap<K,V>` |

The copy preserves list or insertion order and shares referenced element/key/value objects according to their ordinary
semantics. It does not recursively freeze or clone a mutable descendant. Scalar values retain value semantics. Implicit
family conversion has the separately selected contextual copying/widening rules; an explicit method is not a conversion
between List, Set, and Map shapes. Changed key types in approved contextual reconstruction retain duplicate checking
under the [nominal key clarification](accepted-clarifications.md#nominal-map-key-conversion).

## Map entry values

`Entry<K,V>` is the immutable snapshot entry type produced by map traversal. It has public, fixed `key: K` and `value:
V` fields. The contained value keeps its original type: a missing-key lookup's extra nullable layer is not introduced
when an existing entry is traversed. No public Entry constructor or general tuple-unpacking syntax is selected. Write
`for entry in mapping:` and access its two fields. Existing one-level sealed-payload destructuring in when retains its
separate grammar.

Snapshot traversal captures the map's entries when the loop starts, in insertion order. Replacing an original map value
later does not change a retained Entry's value. A referenced mutable data/container value inside that Entry still shares
its ordinary state. Entry bindings and fields cannot be reassigned; retaining an Entry does not freeze its referenced
contents. Checkpoints preserve retained entries and their shared references.

## Dynamic bounds-check timing

Compile-time checks still reject provably invalid constant bounds. At runtime:

1. A plain indexed assignment evaluates its receiver, then index/key, once from left to right. It retains that address,
   evaluates and converts the RHS, and checks list bounds at the write. The RHS may change that same list's size.
2. A compound indexed update retains the same address, reads/checks the existing element before the RHS, evaluates the
   RHS once, applies the operator/conversion, and checks current list bounds again at the write. The retained old
   value supplies the operator even if an alias replaces it while the RHS runs.
3. List `insert` checks `0 <= index <= size`; `removeAt` checks `0 <= index < size`. They evaluate the receiver and all
   supplied arguments before the method performs its bounds check. Ordinary indexing checks after its receiver/index.
4. A map write checks its key/value contract and performs insertion/replacement against the current map. Its key is
   the one already captured; receiver-binding reassignment during the RHS does not retarget the address.

Suspending RHS/argument expressions retain captured addresses, old compound values, and completed arguments without
repeating their evaluation. For example, an unknown empty list may gain its first element while the plain write's RHS
runs, permitting the eventual write at index zero. An invalid compound read fails before that RHS. If a valid list is
cleared during a compound RHS, the final write fails instead of recreating an element. Failure reports the original
operation line under the fail-fast contract.

## Generated data copy

For `receiver.copy(...)`, capture the receiver once before supplied arguments. Evaluate/convert supplied replacements
left to right as written. Then resolve omitted fields in declaration order by reading their current values from that
captured instance. These reads occur after supplied arguments, including completed suspension. Constructor initializer
expressions do not run again for omitted copy fields. Construct a new instance using the resulting fields.

A supplied argument can mutate the captured instance or reassign the variable that originally named it. Omitted fields
observe the mutated captured instance; they do not switch to the replacement receiver binding. Supplied fields retain
their earlier evaluated values. Referenced field values keep normal sharing, so a copied mutable container field still
refers to that container unless the supplied replacement explicitly requests a separate copy.

Taking `receiver::copy` captures that instance once as an ordinary bound reference. Its function-value interface exposes
all field arguments positionally and does not retain direct-call defaults. Private constructor/copy inputs follow U28;
source field access remains private. The generated member name copy remains reserved under U29.

## Verification

The [operation cases](conformance/collection-operations.json) exercise method names/results, typed bound key methods,
nullable previous values, insertion order, explicit container copies, retained Entry snapshots and shallow descendants,
late plain writes, compound reads/writes, and suspended copy-field resolution. Helper source is removed before clients
compile. Every tested wait restores into a fresh host; both output modes exercise the same assertions. Invalid entry
writes, immutable mutation, wrong element types, non-map key members, old source names, and named function-value calls
have paired rejections.

[Native member tests](../bifoil-compiler/src/tests/members.rs) check the signatures and static restrictions. [Runtime
controls](../bifoil-runtime/test/collection-operations.test.mjs) check stored-name compatibility, presence of
null-valued keys, result values, first-match removal, stable replacement order, and detached shallow container copies.
This contract does not certify target-scale allocation, compiler memory/timing, or production host acceptance.

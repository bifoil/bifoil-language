# Copied values at typed legacy boundaries

Selected by the user on 2026-11-05. This resolves ownership; implementation and conformance remain separate gates.
The [accepted clarification](accepted-clarifications.md#copied-legacy-value-graphs) supplements the existing
[legacy compatibility contract](legacy-compatibility.md).

## Isolation and graph identity

Each transfer copies the reachable value graph. Reference-bearing collection/data aliases and cycles inside that
graph remain aliases and cycles in the copy. Native code receives detached values and cannot mutate the original
Bifoil object through those copies. Importing a native result or reading native shared state likewise creates a
detached Bifoil graph, so later native mutations do not silently change that imported value.

An explicit returned value or assignment may introduce the changed data into Bifoil. That operation does not
retroactively rewrite other aliases of the original object. A later transfer is a new graph copy; sharing is not
silently retained across separate transfers. Scalar values retain their value semantics.

Resolved arguments to one call form one outbound graph. Copy at native entry after ordinary supplied-argument and
default evaluation. Preserve aliases across argument roots in that transfer. Existing language conversions still
happen at their selected evaluation points; a container copy already required by an argument conversion remains a
distinct container. Each result or legacy-global read is its own incoming transfer.

## Distinguishing cases

If native code changes a passed list's first element from 1 to 2 and returns it, the original Bifoil list still starts
with 1. The imported result starts with 2. Mutating the result later changes neither the original nor a native object
retained by the routine.

If two fields, or two resolved call arguments, refer to the same mutable container, their native copies refer to one
copied container. A native update through one copied alias is visible through the other copied alias. The original
Bifoil container remains unchanged. Returning that copied graph preserves its internal alias relationship.

A list or data graph containing a cycle keeps that cycle after each transfer. Copying must terminate through memoized
graph identities instead of recursively expanding the cycle. Separate native-global reads produce separate snapshots,
even if the native global still refers to one object. To write back a changed snapshot, assign it explicitly.

## Types, effects, and persistence

Preserve supported nominal identities, generic arguments, scalar kinds, container families, and the existing alias
semantics. Copying does not broaden equality eligibility, erase retained types, or run data-field defaults again.
Exact comparison still follows its selected declared-view rule. Methods remain part of the compiled type definition.

Every incoming value must be checked against its declared interface before it becomes a trusted Bifoil value.
Malformed graphs, invalid fields or keys, incompatible retained types, and unsupported payloads require explicit
checked-bridge failures; no unchecked host object becomes a typed heap reference. Wire forms and supported payload
representations belong in the versioned runtime protocol.

Normal argument evaluation and the declared suspension/transfer effects remain unchanged. A failed conversion does
not roll back earlier native effects. Errors retain the original Bifoil operation location and must not dump private
value graphs into diagnostics.

When a supported native input checkpoint retains a copied graph, restoration must preserve that detached graph,
its aliases/cycles, and the metadata needed for subsequent checked conversion. Do not rerun argument evaluation,
repeat native preparation, or reconnect it to the original Bifoil graph. The existing same-build and supported-save
point restrictions remain in force.

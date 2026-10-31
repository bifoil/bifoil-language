# Language conformance inputs

The case indexes contain expected output, choices, failures, and steering references where assigned. Each case's
`directory` points to readable, original Bifoil source under `cases/`.

- `foundations.json`: text, nullability, collections, loops/ranges, capture checks, varargs, choices, and scenes.
- `expressions.json`: block expressions, lambdas, effect-safe narrowing, loop operand cleanup, choices, and prose.
- `nominals.json`: data, methods, copies, visibility, enums, variants, implicit-member binding conflicts, and module
boundaries.
- `generics.json`: annotation validity, inference, recursive capabilities, nested projected views, nominal parent
identity, nested copy reification, non-null refinements, bound-based operations/calls, exhaustive patterns, suspension,
nullable upper-type joins, sibling sum variants, structural scene/bound inference, safe projected callbacks and
covariant
inputs, and variance.
- `overloads.json`: conversion rankings, tie breakers, references, closures, methods, visibility, and artifact reuse.
- `shared.json`: dependency-first effects, defaults, methods, recursion, conservative cycles, and artifact reuse.
- `lifetimes.json`: allocation-heavy traversal, deep equality/rendering, execution slices, Unicode cursors, bound
receivers, suspended assignment addresses, and deferred callback initialization through branches, casts, collections,
scope exits, returns, checkpoints, enum shorthand, immutable field proofs, computed primitive/text index/key proofs,
map-entry snapshots, reassignable roots, and source-free modules.
- `modules.json`: circular scene/function imports, inferred interfaces, recursive nominal fields, generics, aliases,
initialization cycles, source-free cyclic artifacts, shared calling defaults, named-field ordering/copying, and moved
method bodies with private/defaulted helpers, overloads, recursion, shallow copies, and saved bound callbacks.
- `legacy.json`: typed proxies/calls/transfers, native scopes, strict primitive/enum boundary failures, source-free enum
aliases, and input checkpoints.
- `equality.json`: typed structural exact comparison, cycles, reified arguments, and static capability boundaries.
- `regressions.json`: ordered typing, generic bounds, numeric boundaries, namespace composition, and physical source
locations, including independently compiled inputs.
- `steering.json`: the conservative 305-decision implementation ledger.
- [Review obligations](review-coverage.md): targeted assertions and remaining gaps for all 26 predetermined draft cases.

Use the compiler repository's runner with explicit compiler, runtime, Node, and case-index paths. Its optional `--only
case-id ...` selection rejects unknown IDs, so a typo cannot report a successful empty run. It creates an isolated
project per case, compiles it, runs its output, and saves/restores at each tested input wait. Temporary projects are
removed even when a case fails. A case's optional `precompile` list requests compilation of every listed module before
removing their sources and building/executing the client. This permits cyclic module groups to be produced together. The
ledger uses `partial` for decisions with targeted passing evidence that still require broader interaction coverage. Use
`--jobs 4` for up to four isolated case processes with results printed in index order. The default is one worker;
selection, duplicate-ID errors, and malformed case metadata are checked before compiling. Unknown fields, conflicting
compile/runtime failures, empty expected diagnostics, and empty runs are rejected. Resource measurements use the
separate isolated benchmark commands.

Add `--package` to build the same cases as `bifoil.package.v1` roots plus code scenes. The runtime executor shares the
normal package loader, and every input wait still restores before continuing. Both inline and package modes passed all
1,100 cases with source formatting and idempotence checks. Module coverage also includes source-free exports and data
fields named after JavaScript object properties, including `__proto__` and `constructor`, with shallow copies and a
restored input wait.

Add `--format-sources` to normalize generated Bifoil files before precompilation and verify formatter idempotence. A
syntax-invalid input remains untouched for its normal expected compilation diagnostic; valid cases must format
successfully. The same execution, artifact, and checkpoint checks then apply to the formatted inputs. Original corpus
files are never rewritten by the runner.

Run the standalone index and evidence check before or after adding cases:

```sh
uv run --no-project tools/validate-conformance.py
```

It checks steering IDs, duplicate case IDs, source directories, expected-error fields, statuses, exact selected decision
text, reciprocal case/decision links, and both case-ID and source-file evidence paths. These checks establish metadata
integrity, rather than semantic conformance. Case metadata uses `compile_error` or `runtime_error` for expected
failures; an unknown `error` field is
rejected.

Nested-text cases include quoted braces, recursive interpolation, triple literals, Unicode escape validation, multiline
prose expressions, and suspension through a source-free module without replaying earlier substitutions. Guarded-return
cases check inferred results after early exits and reject invalidated mutable proofs. Named-capture cases restore before
a future declaration, return mutually recursive functions, and preserve their shared state. Expression-return cases
separate enclosing returns from lambda returns and preserve skipped safe-call arguments. Interpolation and branch-header
cases also validate original source locations for anonymous functions. Conditional lookahead cases combine adjacent
block expressions and retain literal prose after executable directives.

Bottom-result cases retain `Nothing` through source-free suspension and unary transfer operands. Projected-capability
cases retain explicit bounds for immutable nominal/sum values and reject unbounded or mutable stable-key claims.

Operator-continuation cases cover comparisons, membership, ranges, casts, compound updates, and member/reference access
while retaining complete generic declarations. Negation cases distinguish keyword operators from names that begin with
`in` or `is`.

Loop-result cases exercise condition exits, labeled breaks, continuing post-test bodies, and source-free suspension.
Location cases check physical lines inside continued strings, lambdas, conditions, and prose; multiline block headers
retain their opening structural level.

Projected-key cases preserve built-in set/key guarantees and closed nominal bounds without treating arbitrary hidden
values as stable keys. Copy cases exercise bounded generic receivers, projected targets, conversion ranking, and
snapshots taken before later suspended arguments mutate their source.

Generic conditional cases combine bounded enum/Boolean/sum coverage, nullable subjects, guarded remainders, and
alternative-case narrowing. Diagnostic cases require source-language type names and original locations. Value-block
cases share prefix guards, loop exits, assignment effects, builtin calls, forward local results, and anchored recursion;
source-free modules and checkpoints preserve their results. Hoisted-function cases reject later null proofs that an
earlier call could bypass, while preserving block-entry and anonymous-creation proofs. Recursive expression cases
converge from concrete branches and retain suspended recursive calls across checkpoints.

Narrowed generic binding cases retain the original `T` in typed assignments, returns, arguments, and collection
literals. Bounded variant cases and suspended source-free calls exercise the same rule. New expressions do not inherit a
binding's original identity.

Cast cases cover shared null values, covariant containers with bottom arguments, common function subtypes, and generic
runtime targets. They verify retained mutable aliases and a source-located checked failure after source removal. Numeric
conversions, family copies, and disjoint invariant keys remain compile errors in cast syntax.

Skipped-default cases supply named and function-value arguments before a captured variable is declared, then restore
that future capture at a checkpoint and initialize it before an omitted-default call. Separate groups omit only the
needed defaults, including a block with local declarations. Body and transitive reads still require initialization.

Assertion cases retain original generic identities and contextual literal types while preserving null-failure source
locations. Field cases distinguish immutable map-entry snapshots from changes to the original map. Reassignable-root
cases check writes, calls, escaping functions, prepared choices, and captured `when` values. Structural-inference cases
preserve scene input types and generic arguments through source-free suspension. Enclosing caller-selected parameters
cannot be respecialized by a nested generic call; existing invariant instances cannot be adapted to different payload
arguments.

Contextual call cases retain original binding and field identities through generic calls and variadic groups, including
saved suspension. Numeric literal joins and nullable invariant inputs remain valid; computed Strings cannot acquire a
caller-selected generic identity. Bound-result cases preserve valid primitive/capability instantiations under wider
return contexts and reify proven non-null generic arguments through suspended calls and varargs. Method-view cases
preserve actual receiver arguments, separate them from explicitly Any instantiations, and retain captured receivers
after reassignment and restoration.

Immutable-index cases retain null and type proofs through nested List/field paths, source-free helpers, generic result
inference, escaping callbacks, selected guards, and saved waits. Negative cases cover mutable containers, changing
indexes, root replacement through a call, nested mutation, and effectful `when` tests. Ordinary index checks remain in
the executable code; a refinement does not prove that an arbitrary input list is nonempty.

Immutable-map cases cover numeric and character key widening, equal signed zeros, negative integers, null, Boolean, and
Unit keys. Lookup proofs survive source-free calls, captured callbacks, selected guards, and saved waits; nested fields
retain their own mutability checks. Mutable containers, changing keys, replaced roots, nested mutation, and retargeted
`when` sources remain negative cases.

Present generic-result cases combine nullable binding, field, List, and Map reads with a caller-selected fallback.
Inferred return types support non-null Int callers and typed references through source-free helpers; saved String
returns retain progress. Explicit nullable instantiations still return null, real null-return branches remain nullable,
and computed Strings cannot acquire generic identity from the read that produced them.

Immediate-reference cases call (::function), receiver::method, and typed scene values using their positional interfaces.
Explicit generic instantiation and variadic spreads remain valid. Names, omitted inputs, and unresolved overloads or
generic references are negative cases. A source-free bound receiver remains the original instance while a suspending
argument replaces its source binding; ordinary declared calls retain defaults.

Transitive-default cases retain supplied argument shapes through named and recursive wrappers, calls before a captured
binding's declaration, escaping block-local functions, source-free artifacts, and checkpoints with unused captures still
uninitialized. Omitted defaults still require their reads, including after an earlier body-only reference to the same
function and before leaving the captured binding's scope.

Overloaded-capture cases select closed primitive calls through wrappers, retain numeric widening and direct-fit ranking,
and preserve local overload cells after returning and restoring a checkpoint. Negative cases keep selected future reads,
unknown argument profiles, and generic candidates conservative. These checks share the ordinary call ranking rather than
a second resolution policy.

Passing these cases establishes their expected behavior. It does not prove complete language conformance.

Legacy cases require the additional explicit `--engine /path/to/choicescript/web/scene.js` option. Original native
`.txt` sources remain under each case's `legacy/` directory; the runner never modifies the supplied engine.

Mutable-field cases retain local guards, assertions, safe receiver prefixes, inferred generic results, and pure `when`
provenance. Source-free checkpoints preserve a guarded nested receiver and a supplied String argument captured before a
later argument clears its source field. Negative cases include alias and conditional writes, expression-block mutation,
escaping readers, and snapshotted choice guards. A generic-bound failure now includes an actual field write after its
test, distinguishing invalidated proofs from the newly supported unchanged-field case.

Mutable-list/map cases retain guarded reads through normalized numeric/enum keys, generic results, readonly queries, and
copies. Prepared checkpoints preserve nested safe index prefixes and an argument captured before a later argument clears
the container. Alias mutators, conditional updates, escaping readers, and snapshotted choice guards invalidate the
relevant proofs. Independent object fields survive container mutations, and independent lookups survive field writes.
The old mutable-list rejection fixture now clears the list after its guard to test a real invalidation.

Compound-update cases retain the value read before an effectful RHS, including fairmath, key changes, and suspended root
replacement. Negative cases retain target-evaluation effects and missing-guard checks. A separate captured-callable case
clears its containing list during a suspended argument and resumes the already-selected closure. Generic-cast cases
preserve reified arguments and nullable results through source-free waits, while oversized shared graphs reach the
explicit publication guard.

Callable graph cases retain separate function, result, and scene-input identities through alias expansion and generic
inference. Compact unused 28-level aliases compile; 34-level aliases retain the existing depth diagnostic. Source-free
higher-order function and scene references restore input checkpoints before continuing. Function variance, suspension,
variadic shape, and the original serialized type format retain separate regression coverage.

Collection graph cases check lossless nested widening, generic argument joins, inferred return-type joins, and copied
snapshots through source-free checkpoint restoration. Large expanded signatures retain the existing canonical-size
diagnostic. Inferred common types still reject an implicit mutable/immutable family copy.

Projected read graph cases retain upper bounds and covariant nested values through independently compiled modules and
two restored input waits, including a projected function result. Large shared read graphs reach the existing canonical
publication diagnostic without expanding every repeated branch.

Normalization scope cases retain scope-wide local alias visibility without leaking names between sibling functions or
branches. Their source-free checkpoint case also keeps independently inferred String and Float results.

Generic name scope cases retain distinct class, method, local-function, and generic-alias parameter identities across
source-free checkpoint restoration. Visible generic parameter shadowing remains an error.


Shared-summary cases retain imported read/write dependencies through a helper module that has no shared declarations.
Independently compiled state and helper modules initialize before the caller, then preserve the resulting effects across
checkpoint restoration. An empty initialization pass must keep the helper's ordinary-function summaries.


Recursive dependency-query cases retain shared reads through mutually recursive helpers and conservative indirect calls.
Repeated initializer queries preserve the same dependency plan through source-free modules and checkpoint restoration.


Shared dependency-list cases preserve separately initialized values when their common seed later changes. Source-free
checkpoint restoration retains the initialization counter, while a later ordinary read sees the updated seed and
increments that counter once. Metadata sharing must not alias language values or replay initializers.


Completed-path acceptance includes source-free inferred functions whose conditional, `when`, and choice arms retain
delayed values and callback requirements. Repeated restored waits preserve earlier expression operands. A negative case
rejects a callback call when one completed arm still requires an uninitialized captured binding.


Loop-break acceptance restores waits before labeled outer breaks, counted-loop exits, and do/while exits. Latent
callbacks retain their delayed captures until initialization after the loop; accumulated expression values and shared
preparation counts survive restoration. Negative cases retain missing-initialization and possible repeated-write errors.


Projected nullable method acceptance uses source-free generic owners, named/default calls, variadic groups, saved bound
references, and suspending calls. Copies retain hidden concrete owner arguments. Negative cases reject both present
arguments and null passed to a bare hidden type whose actual argument may be non-null.


Projected callback coverage includes direct and optional fields, returned functions, type aliases, suspension, empty
variadic groups, and saved function views. Default-only methods and generated copies retain their original reified
contracts. Invalid null/present inputs keep explicit `Nothing`/`Nothing?` diagnostics.


Continue-path coverage preserves distinct correlations between initialized bindings and retained callback requirements.
A source-free loop restores each prepared wait and calls the preceding iteration's callback; an unsafe backedge still
reports its uninitialized capture. Scope-storage changes must retain these semantics rather than merging away needed
path information.

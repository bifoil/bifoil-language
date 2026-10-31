# Implementation status

Updated: 2026-10-31

The full steering specification is authorized for implementation. The native compiler is Rust; the required execution
layer is JavaScript through an explicit ChoiceScript extension. Current work uses the development `bifoil-vm.v2`
profile. The runtime also retains v1 fixture compatibility.

The full specification is **not implemented**. Passing cases below establish behavior for those cases; they do not
certify all 305 steering decisions, complete first-milestone compliance, or release readiness.

## Implemented and exercised paths

The compiler parses source into an independent AST, prepares declarations, performs semantic checks, lowers instructions
with source spans, produces reusable module artifacts, and links extended ChoiceScript output. Source-free compilation
of a client module is tested.

The current end-to-end cases exercise:

- Scalar/nullable types, Unicode text, scalar indexing, numeric conversions, exact equality, and checked arithmetic.
- Immutable/mutable collections, aliasing and copying, insertion order, snapshot traversal, and varargs.
- Ranges, loops, labels, definite assignment, captures, defaults, expression blocks, and anonymous functions.
- `if`, `when`, embedded prose directives, choices, option history, and scene visits/transfers.
- Suspension with retained operands, captured cells, traversals, generic arguments, prose state, and choice snapshots.
- Nominal data construction, methods, bound references, shallow copies, private fields, enums, and sealed variants.
- Selected generic inference, equality/key capabilities, explicit arguments, reified tests, and suspended generic
closures.
- Overloads across files, local closures, methods, and source-free module artifacts; contextual function references.
- Conversion dominance, variadic/default/generic tie breakers, visibility filtering, and ambiguity diagnostics.
- Checked generic variance through fields, methods, nested types, and function positions; copies of widened receivers.
- Definition-time type arity, bounds, aliases, and key eligibility checks, including unused declarations.
- Recursive equality/key capability formulas, bound-derived projected reads, and isolated hidden collection elements.
- Eager shared initialization through calls, defaults, methods, and artifacts, with conservative cycle rejection.
- Tracing heap collection retaining live aliases, cycles, captures, receivers, traversals, and assignment addresses.
- Typed primitive/enum legacy globals, native subroutine/transfer bridges, variadics, and boundary diagnostics.
- Native choices, page breaks, text and number input, and fresh-host restoration without replaying preparation.
- Content-validated incremental module reuse, dependency invalidation, corruption recovery, and nested artifacts.
- Content-addressed code scenes with atomic roots, source-free inputs, damage repair, and validated completed reuse.
- Bounded terminal scene reads with streaming UTF-8 decoding and oversized root/chunk rejection.
- Borrowed shared-initialization metadata with retained summaries from modules that declare no shared state.
- Bounded completed dependency queries for repeated helpers, recursive groups, and conservative indirect targets.
- Shared immutable dependency lists during source resolution and streamed metadata input, with unchanged artifact bytes.
- Early release of rejected cached interfaces, with fresh method inference and preserved output after failed edits.
- Shared parsed/checked parameter headers with isolated normalization and specialization, preserving canonical
artifacts.
- Normalized method bodies moved into lowering, and active source ASTs consumed without a full normalized duplicate.
- Ordered native paragraphs around engine-rendered images, charts, and line breaks, with empty returns left intact.
- Reified argument preservation when projected containers are copied, including empty values across checkpoints.
- Cyclic imports with normalized declarations, inferred interfaces, nominal fields, generic methods, and aliases.
- Source-free cyclic groups with complete fingerprint validation, cache reuse, and mixed-version rejection.
- Cooperative execution slices preserving partial evaluation and rejecting obsolete scheduled continuations.
- Unicode scalar operations and saved String cursors without full character-array traversal snapshots.
- Iterative deep/cyclic equality with isolated unordered-match trials, and large argument/output groups.
- Terminal checked failures retaining the original diagnostic and delivering completed output exactly once.
- Streamed canonical artifact hashing and bounded atomic writes without complete serialized-program copies.
- Disk-backed pending/completed function bodies, bounded streamed input, and verified completed-output reuse.
- Imported type isolation, nominal artifact ownership, and generated/member interface validation.
- Nested projected container/nominal reads, preserved parent identity, and generic-aware case coverage.
- Effect-safe Boolean and loop narrowing, failed-case invalidation, and proofs from final loop conditions.
- Loop transfers that discard partial expressions while preserving surrounding operands across checkpoints.
- Iterative explicit String rendering for deep graphs, active cycles, and repeated aliases.
- Ordered prose escaping for backslashes, directive markers, and interpolation delimiters.
- Shared nominal metadata queries and constant-time progression membership retaining search-index overflow checks.
- Indexed primitive set/map operations with insertion order, structural fallback, and checkpoint/collector rebuilding.
- Real browser choices and native text/number waits, full-page checkpoint restoration, and owned presentation cleanup.
- Deferred source AST construction, hash-checked rereading, and linear multiline-string layout.
- Distinct definite/possible initialization proofs, including skipped safe arguments and loop backedges.
- Generic non-null refinements through checks, assertions, closures, bounds, and precompiled module interfaces.
- Nullable type/body colons, continued Elvis expressions, and null-only fallback result typing.
- Generic upper-bound fields, methods, indexing, mutation, primitive operators, callable types, and scene references.
- Evaluation-order-aware capture proofs through lambdas, collections, casts, branches, scope exits, and loop backedges.
- `when` effects through failed tests and guards, successful-alternative joins, and subjectless null narrowing.
- Effect-free scalar condition proofs that retain ordinary evaluation and diagnose provably empty choices.
- Suspended defaults for functions and scenes, including source-free modules and repeated checkpoint restoration.
- Native host snapshots before first access, without executing legacy reads or calls while saving.
- Nested projected copy identities across nullable, nominal, and callback types, with writable invariant copies.
- Exhaustive final anonymous `when` returns, alias-based enum coverage, receiver checks, and type-only imports.
- Skipped-default flow joins and safe captured narrowing during body checking and return inference.
- Compact anonymous capture environments preserving shared cells, delayed initialization, and source-free checkpoints.
- Local generic function templates with enclosing arguments, later specialization, and saved capturing functions.
- Shared bounded text scanning for nested strings, triple literals, quoted braces, and interpolation comments.
- Prose paragraph flow preserving expression/triple-string newlines and literal directive prefixes within substitutions.
- Inferred results after early-return null/type guards, including generic and overloaded source-free methods.
- Named-closure capture compaction preserving recursive groups, future declarations, and shared cells during saving.
- Return inference through nested expressions and value blocks, lazy operands, and safe calls, with separate lambda
scopes.
- Shared non-null assertion proofs and retained source locations for anonymous functions inside interpolation.
- Non-consuming conditional lookahead and shared parsing of statement/value branches and executable prose headers.
- Artifact rejection of missing instruction locations and inconsistent named-closure capture contracts.
- Guard-aware return inference for subjectless/payload cases, alternative joins, failed guards, and choice snapshots.
- Rejection of orphan conditional branches and consistent whitespace after executable prose prefixes.
- Shared immutable type arguments with copy-on-write normalization and unchanged source-free artifact bytes.
- Bottom-valued return inference and unary transfer expressions through source-free suspend functions.
- Explicit equality/key capability bounds preserved through projected nominal and sum types.
- Keyword-boundary negation and shared trailing-operator continuation rules retaining complete generic endings.
- Restored nominal field/type/mutability contracts, entry representations, and primitive type-identity checks.
- Loop-exit-aware inferred returns with labeled transfers, post-test condition scopes, and suspended source-free calls.
- Physical-line tracking for nested/continued anonymous functions and opening-level multiline block indentation.
- Closed-bound and built-in projected key capabilities with transitive dependency invalidation.
- Projected collection-family copies from non-null generic bounds, retaining ranking and pre-suspension snapshots.
- Generic bounded case coverage, compatible equality, and safe narrowing across alternatives and guarded remainders.
- Source-language type diagnostics and precise nested locations without repeated source prefixes.
- Shared value-block prefix flow and local callable convergence, including recursive expression bodies.
- Hoisted named closures restricted to block-entry proofs, with anonymous creation-time proofs retained.
- Checkpoint key-graph validation and duplicate rejection, including immutable cycles and signed floating zero.
- Continued-expression scanning without repeated prefix scans or excessively deep constructed expression trees.
- Contextual original-type identity for unchanged narrowed generic bindings through returns, calls, and literals.
- Conservative cast overlap through nullability, bounds, variance, and function shapes, retaining runtime type checks.
- Inferred original generic identities through nested value blocks, returns, escaping lambdas, and suspension.
- Separate body/default capture proofs, with supplied defaults skipped and complete runtime environments retained.
- Declaration-site lexical capture classification that preserves enum shorthand and future-variable initialization
checks.
- Rejection of implicit-member binding collisions, with generated copies available through implicit method receivers.
- Nullable generic upper bounds preserved through function/nominal variance and inferred compatible return joins.
- Common sealed-sum joins for sibling variants through inferred functions, collections, equality, and checkpoints.
- Stable immutable-field null/type proofs through nested paths, inferred generic results, closures, and choice guards.
- Converted `when` subject provenance and stable immutable-field matching across case effects and suspension.
- Contextual non-null assertions retaining unchanged generic identities, expected literal types, and source diagnostics.
- Immutable map-entry key/value proofs across source-map mutation, snapshot traversal, and restored input waits.
- Immutable-field proofs through reassignable roots until assignment or effects, with independent snapshots retained.
- Structural generic inference through scene references, sealed parents, and known bounds, with callee-owned arguments.
- Declaration-consistent callable views and active saved generic arguments matching parameter types and mutability.
- Expected-result retry for narrowed generic call arguments, retaining nullable input identities and literal joins.
- Bound-valid argument preservation under wider result contexts, including proven non-null bindings and fields.
- Intrinsic bound-method type arguments retained through covariant views, reassignment, casts, and saved effects.
- Bound-valid generic function references under nullable, erased, and suspend views, without signature adapters.
- Bound-directed scalar and recursive immutable-container call inference, including constructors and dependent bounds.
- Standard TOML manifests with strict typed fields, equivalent syntax, and source-free module builds.
- Buffered function spooling with logical offsets, preserving append, pending restoration, and canonical output.
- Iterative component discovery, deterministic cyclic groups, and a 100,000-node graph regression on a small thread
stack.
- Class-private permission tied to genuine receivers and declaration identity, including other generic instantiations.
- Unit value registration consistent with lexical no-shadowing and expected-type enum conflict rules.
- Per-function summary and transfer of reusable acyclic bodies, with stale cached bodies discarded before rebuilding.
- Exact binary64 preservation through JSON decoding, source-free modules, defaults, and checkpointed Float keys.
- Per-function artifact decoding with canonical validation, formatted source-free modules, and corrupt-cache recovery.
- Constant-index immutable-list proofs through fields, generic returns, choices, closures, and saved suspension.
- Immutable-map lookup proofs with normalized primitive keys, null presence, nested fields, and saved guards.
- Proven-present generic result joins without spurious nullable returns, including source-free typed references.
- Direct UTF-8 tokenization without complete character/offset arrays, retaining token text and source locations.
- Immediate function/scene references using explicit positional inputs, with receiver capture before suspended
arguments.
- Transitive call-shape capture proofs, skipping supplied defaults through wrappers, scope exits, and saved closures.
- Bounded empty-dependency memoization keyed by declared callable identity and complete argument profiles.
- Shared callback publication checks, including imported state and callbacks nested inside collections.
- Deferred callback reads retained through collection copies, extraction methods, and bound collection methods.
- Flow-sensitive escaped-cell obligations for later captured-variable updates, including branch joins and retargeting.
- Published and cached module bodies decoded into private spools, preserving canonical hashes and the artifact format.
- Cache corruption remains recoverable; private-spool and incremental-deadline failures remain fatal.
- Write-only captures retain existing cells without reading old contents, including escaped and source-free writers.
- Captured compound reads require initialization at invocation rather than at function declaration.
- Compile-time duplicate-key checks include Unit and constant Boolean expressions; Unit/null remain distinct in saves.
- Signed Int range endpoints and large positive steps avoid overflow at traversal completion.
- Checked plain-enum legacy values, nullable forms, source-free transitive aliases, and independent engine restoration.
- Enum-key map proofs retain nominal case identity across qualified/shorthand spellings, callbacks, and checkpoints.
- Map duplicate diagnostics share typed key normalization with immutable lookup proofs.
- Top-level and local enum aliases retain qualified case identity and scope-wide visibility through saved callbacks.
- Shared immutable nominal records across module/program/catalog views, with isolated inferred-method updates.
- Literal call profiles reuse ordinary overload ranking without inheriting captures from unselected declarations.
- Local overload sets retain every physical function cell through returned callbacks, collection, and checkpoints.
- Shared alias graphs retain canonical nullable application, depth checks, key eligibility, and generic substitution.
- Plain alias scopes share names; canonical hashing rejects oversized expansion before replacing completed output.
- Structural type equality compares shared node pairs once; oversized type diagnostics retain bounded source spelling.
- Generic alias instantiations and covariant subtype checks share query-local results without mixing type arguments.
- Projection and closed-type queries visit repeated subgraphs once while retaining hidden-type restrictions.
- Generic alias bounds resolve later aliases in their lexical scope, including source-free exports and local
checkpoints.
- Generic call inference deduplicates repeated constraints while retaining cross-argument joins and distinct parameters.
- Generic aliases share lexical names through parameter overlays, preserving outer types and shadowing diagnostics.
- Named captures retain their declaration scope through calls, references, containers, defaults, and scope retirement.
- Known local helpers establish captured var initialization for primitive and structured values on every normal return.
- Captured-cell writes enforce publication readiness even when a writer was compiled before its reader escaped.
- Proven overwrites retire old deferred dependencies without altering earlier value snapshots.
- Completed helpers discharge entry reads dominated by captured writes, including branches, loops, and saved waits.
- Escaping initializing callbacks retain their cells without requiring the overwritten old value at creation or call.
- Initialization proofs use one bitset for straight-line code and compact basic-block facts for branches and loops.
- Invoked helpers retain publication obligations separately from read requirements, including wrappers and defaults.
- Stored callable values retain their payload; ordinary local reads do not publish their mutable source cells.
- Immutable lexical keys/indexes retain lookup null/type proofs through generic returns, closures, and checkpoints.
- Analysis-only binding identities prevent facts leaking to later declarations that reuse a key's spelling.
- Unchanged reassignable keys/indexes retain proofs until calls or key writes invalidate them, including global aliases.
- Key-use markers keep ordinary assignments from scanning unrelated lookup facts; immutable facts survive invalidation.
- Imported names for one shared cell invalidate each other's null/type/lookup facts after a write through any alias.
- Lowering and return inference share assignment updates; local snapshots and parameter values retain their contents.
- Shared-alias guards and stable paths apply across imported names, including readonly guards at prepared choices.
- Non-null safe fields/indexes establish stable receiver prefixes through when cases, generic returns, and saved
closures.
- Enum-key shorthand resolves during typed path traversal without recursively inferring nested receivers again.
- Pending-result and narrowed-result parameter queries share type subgraphs instead of unfolding repeated arguments.
- Unchanged mutable fields retain guard/assertion proofs through nested safe paths and generic result inference.
- Heap writes invalidate field-dependent facts across aliases; key writes preserve independent mutable-field proofs.
- Supplied argument snapshots retain their values when later arguments mutate fields and suspend.
- Mutable list/map guards retain local null/type proofs through normalized keys, readonly queries, and saved arguments.
- Field writes, container updates, and key reassignment invalidate their dependent selectors across aliases.
- Builtin mutation effects are shared by lowering and return inference; unknown builtins remain conservative.
- Compound address updates retain the read type before RHS mutation, key/root replacement, suspension, or early return.
- Generic-cast graph queries retain completed node pairs, proof kind, and depth without weakening concrete disjointness.

- Removal of unreachable lowered instructions with remapped branches, loop/default targets, and deferred choices.

- Shared source filenames across newly lowered instructions, preserving exact module/program bytes and diagnostics.

- Structural facts retained during artifact decoding, preserving canonical verification and deferred interface checks.

- Bounded canonical-value reuse during package publication, with storage/header checks retained on every use.

- An 81,920-function program ceiling with independently bounded modules and checked larger restored workloads.

- One buffered input spool writer per module, retaining fatal flush failures even after parsing errors.

Typed module interfaces include nominal metadata. Runtime objects use explicit heap/cell/environment references, so
aliases and captured bindings survive supported checkpoints. Saves are taken at prepared input waits and restored
against the same compiled build without replay.

## Maintainability and evidence

The compiler separates its AST, parser grammars, declaration passes, semantic checks, and lowering. Generated field
constructors and copies share one builder. Analysis metadata has a bounded session lifetime. Runtime behavior uses
explicit class layers and imported handlers; duplicate VM implementations and prototype installers have been removed.
The host adapter owns ChoiceScript extension registration.

- [Compiler architecture and maintenance](../bifoil-compiler/ARCHITECTURE.md)

- [Runtime architecture and ownership](../bifoil-runtime/ARCHITECTURE.md)

- [Compiler usage and current coverage](../bifoil-compiler/README.md)

- [Resource measurements and qualification history](../bifoil-compiler/RESOURCES.md)

- [Runtime host responsibilities](../bifoil-runtime/README.md)

- [Instruction boundary](../bifoil-runtime/PROTOCOL.md)

- [Conformance programs](conformance/README.md)

Current qualification passes 570 native compiler tests, 43 release CLI tests, strict all-target Clippy, and formatting
checks. All 1,100 language cases pass after source formatting and idempotence checks in both inline and package modes,
totaling 2,200 case checks. The observer verifies exact case IDs and frozen compiler and execution-source fingerprints.
All 112 runtime tests pass with the pinned engine explicitly supplied, including its 20,000-result fairmath comparison.
Tested input waits save and restore before selection or submission.

Thirteen dedicated source-free comparison cases check exact collection families and type arguments, unordered contents,
nullable contained values, cyclic nominal graphs, independent generic arguments, and reified empty covariant views. They
also check shared pattern-binding widening inside the branch and static rejection of unknown equality capabilities or
unsupported function equality. The [comparison index](conformance/equality.json) supplies targeted partial evidence; the
original 305 steering decisions are unchanged.

Direct captured-val initializer calls now retain separate proofs for selected overloads and exclusive source sites. Each
reached call must find its protected cells unwritten, and every normal return must initialize them. Loop-body calls use
ordinary backedge checks: terminal or labeled exits and post-test false conditions may prove one invocation. While-
condition calls, published writers, actual second assignments, and missing-path writes remain conservative or rejected.
An earlier overload-limit fixture is now a checkpoint/output regression; its failed expectation remains in private
evidence. Three repeated-loop fixtures retain their sources and receive more precise loop diagnostics.

Known nonempty ranges, strings, and collection values can establish initialization after traversal. Construction facts
follow immutable lexical identities through aliases, captures, and safe narrowing. Container copies respect the target
family; readonly mutable aliases do not freeze contents. Referenced elements keep their own mutability. Unknown or empty
inputs retain conservative checks.

An isolated 2,053-function workload retains 1,024 readonly cells after real initializer calls on terminal loop paths.
Its edit measured 1.450 seconds and 26,611,712 bytes peak compiler RSS. Unchanged reuse measured 0.346 seconds and
4,202,496 bytes. Twelve independent executions checked every cell, retained reader, and call count without replay after
restoration. The resource guide retains historical workloads, control comparisons, source-free linkage results, failed
observations, and current enforcement limits. These observations do not establish aggregate cross-platform compliance or
the much larger source-line target.

Original fixtures passed real Chrome acceptance with the unchanged ChoiceScript renderer and stylesheet. Checks covered
disabled options, literal interpolation markers, successive choices, text and numeric input, text/image/chart order, and
full-page reloads at input waits. Restored transcripts and state retained earlier responses without replaying native
preparation. Completion left no game forms or submit buttons, and browser consoles had no errors or warnings. These
results cover the original acceptance host; wider platform and complete-game acceptance remain unfinished.

## Audit corrections

The [audit follow-up](audit-resolution.md) records each finding's repair or remaining limit. Ordered operand and
argument checks now share normal-completion flow; binary lowering validates actual captured operand types. Reusable
artifacts require `bifoil.module.v3`, while the VM instruction profile remains v2. Rebuild older modules from source.
Graph-wide runtime name collisions fail before root publication. Logical/bottom checks, collection search capabilities,
generic bounds, fairmath diagnostics, deterministic discovery, source attribution, bounded cache markers, and indexed
legacy labels have targeted regressions.

Silent child failures cannot pass the conformance gate. The ledger now checks decision text, statuses, and reciprocal
links; unrelated timing tags were removed, leaving S14 pending. The [26-case review map](conformance/review-coverage.md)
separates direct assertions, runtime-owned evidence, and unfulfilled acceptance work. All 112 runtime tests passed with
the explicitly supplied engine and no skips. Five compiler-tool and three ledger-validator Python regression groups
also pass. Earlier resource timings remain historical observations for their stated compiler. Fresh post-audit workloads
contain 15,001 and 81,918 functions, with edits at 6.630 and 9.076 seconds and peak observed compiler RSS of 86,106,112
bytes. Eight original/restored executions check every generated routine and result; actual edited builds reject saved
state from the original builds. These bounded measurements do not establish the accepted source-capacity target or full
aggregate/platform compliance.

## Remaining work

Composite legacy boundary representation and ownership remain unspecified. Further native UI/platform commands and
broader generic projection, bounds, inference, and type-identity rules remain unfinished. Cyclic interfaces now have
targeted execution and artifact
coverage; their wider inference interactions still require acceptance. Projected reads now use known upper bounds and
safe covariant layers; invariant hidden-dependent results remain conservative. Explicitly nullable hidden inputs accept
only null; other present hidden inputs remain unavailable, while defaults and empty variadic groups remain usable.
Unchanged builds can skip linking after byte validation. Changed builds still retain reachable interfaces and one active
component; disk-backed interfaces and lazy runtime code loading remain necessary for the capacity target. Shared
dependency discovery deliberately includes all ordinary targets for unresolved indirect calls and may reject safe
initializers.

Immutable field guards, constant and lexical-binding List indexes/Map keys, assertions, and direct `when` subjects have
targeted proof coverage. Reassignable roots and index/key bindings retain facts until writes or effects invalidate them.
Mutable field/container proofs are local and discarded by relevant writes or calls. Pure primitive and text keys retain
facts through lexical dependencies and immutable selected field paths. Calls, mutable/composite heap-dependent keys, and
larger expressions outside the optional proof budget remain conservative.

Captured delayed `val` writes outside proven direct-call flow remain conservatively rejected; broader callable
read/write and alias proofs remain unfinished. Loop-carried capture checks cover changed dependencies without rejecting
untouched deferred callbacks merely because an unrelated loop runs.

Overloads, variance, aliases, shared initialization, and collection lifetimes have targeted coverage; their wider
interactions still need systematic acceptance. Complete browser/save-host acceptance and the much larger source-capacity
target
remain open. The collector is implemented, while larger allocation and host-lifetime acceptance remains necessary.

The conformance ledger is conservative and does not mark the full steering record complete. Compiler/runtime profile
changes must preserve the selected semantics and add meaningful coverage. Native story executables, self-hosting,
publication, and legal/release decisions are not established by this implementation work.

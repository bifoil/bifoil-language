# Compatibility and producer contract

This contract defines compatibility for the selected extended ChoiceScript target. The current instruction profile is
`bifoil-vm.v3`. Source-language conformance, production-host acceptance, and resource qualification remain separate
obligations. A compatible container does not by itself establish any of those results.

## Version identities and supported combinations

An instruction profile defines execution behavior. A container format defines the required serialized representation. A
producer is the compiler or tool that claims those contracts for its output. These identities are independent of a
producer's executable checksum or package version; version numbers from different format families need not agree.

The following combinations are supported:

- Current reusable modules: `bifoil.module.v6` with `bifoil-vm.v3`.
- Original inline programs: `bifoil.program.v1` with `bifoil-vm.v1`.
- Extended inline programs: `bifoil.program.v2` with `bifoil-vm.v2` or `bifoil-vm.v3`.
- Eager packages: `bifoil.package.v1` with `bifoil-vm.v2` or `bifoil-vm.v3`.
- On-demand packages: `bifoil.package.v2` with `bifoil-vm.v2` or `bifoil-vm.v3`.
- Code chunks for either package layout: `bifoil.code.v1` with the exact v2 or v3 profile of their package root.
- Original checkpoints: `bifoil.checkpoint.v1` with `bifoil-vm.v1`.
- Current checkpoint envelopes: `bifoil.checkpoint.v2` with any supported instruction profile, matching the program.

All other format/profile pairs are rejected. In particular, the runtime cannot select v2 execution for a v1 program
container, select v1 execution for a v2 program container, or restore a v1 checkpoint as v2 execution. The current
checkpoint writer uses a v2 envelope even for an original v1 program, preserving that program's v1 execution profile.
This is a container upgrade, without a source-language or execution-profile migration.

A checkpoint must additionally match its program's profile and build identity exactly. Merely appearing in the supported
combination list is insufficient. The original profile remains available for original regression inputs; its presence
does not imply that an old compiler or runtime implements the full Bifoil language.

## Declared comparison views in profile v3

V3 requires exact_compare instructions with both declared operand types and a Boolean negate flag. The runtime reifies
those types in the active call frame and recursively compares exposed fields and container positions. It does not
replace retained construction types. V1/v2 exact comparisons retain their construction-type behavior; an older body
cannot adopt v3 semantics merely by relabeling its profile. V3 rejects binary exact-equality instructions without
comparison views, and v1/v2 reject the new instruction.

The module, program, package, code, and checkpoint container envelopes keep their existing structures. The required
instruction change is identified by profile v3. Current compiler module readers require that profile and regenerate
previous-profile modules from source; old runtime fixture support is a separate contract. Unknown or mixed profiles
remain errors, including a correctly hashed code chunk whose profile differs from its package root.

## Retained generic inference in module v6

Module v6 requires the selected supplied-argument inference rule. An already inferred, bound-valid argument remains
selected when its substituted result satisfies the expected type by genuine subtyping. Expected types may fill missing
parameters without replacing already sufficient arguments. Invariant positions and value conversions retain the
existing contextual inference rules. An older lowered body may have embedded Any where Int is now required, even if
its public signature is unchanged. Relabeling its format or recomputing its checksum cannot repair that identity.

Regenerate module v5 and earlier artifacts from source. Current readers reject those older formats in both ordinary
and streamed paths, including correctly digested inputs. This changes reusable producer compatibility, not the VM
instruction schema: program v2, profile v3, package v1/v2, code v1, and checkpoint v2 remain unchanged.
Their build hashes
still bind the selected module identities and prevent cross-build restoration.

## Producer obligations and trust

A module producer claiming format v6 must perform the selected static checks and emit their required runtime checks.
This includes preserving the chosen operand evaluation order and checked operand types. Earlier module bodies cannot
establish that contract by changing their format field; regenerate them from source. The current compiler rejects
earlier, later, and unknown module formats and profiles, including when their ordinary checksums are otherwise valid.

A compatible independent producer need not have the same executable bytes as the consuming compiler. Its output must
meet the same format, profile, declaration, dependency, and semantic obligations. A producer name or package version
alone grants no compatibility. No public module field currently requires an exact compiler-binary identity.

Compiled inputs are trusted producer output. Consumers validate structure, identities, dependencies, and required
relationships; they do not prove that arbitrary supplied code implements its claimed source semantics. SHA-256 digests
establish integrity under the specified representation and are not publisher authentication. Distribution and host
applications must preserve their trust in the selected compiled roots and artifacts.

Unknown object members do not negotiate new behavior. Readers may ignore them where their schemas permit it; such
members cannot be required for correct execution under a claimed supported format/profile. Unknown operation/type
discriminators, required representation versions, and instruction profiles are errors. A producer requiring an
unsupported operation or meaning must declare a corresponding new version rather than hide it in an ignored member.

## Reusable module validation

The `.bfm.json` interface retains declaration identities, exported signatures and overloads, nominal definitions,
generic parameters and bounds, aliases, default behavior, captures, effects, initialization dependencies, and source
locations. [Instruction interfaces](../bifoil-runtime/PROTOCOL.md) define their representation. Imported private helpers
may remain necessary to execute an exported default or body; their presence does not make them source-visible exports.

Before publication into the linker's pending code store, readers must enforce bounded decoding and validate the
supported format/profile, module name, canonical digest, function ownership and bodies, parameters, exports, nominal
metadata, checked instructions, and source locations. The ordinary and streamed readers use the same structural
validator. A streamed decoder's private spool is not a successfully linked or published module.

After dependencies are available, graph validation must check imported declarations and dependency identities before the
build succeeds. Dependency values must match the selected artifacts. A cyclic component additionally requires its
complete, sorted membership and matching group fingerprint; individually well-formed members from different component
revisions cannot be mixed. A successful local checksum alone is insufficient.

Canonical module hashing uses the recognized typed representation with an empty digest field. Maps have deterministic
ordering; declared field order and source metadata retain their defined representation. Whitespace or member ordering in
an input JSON file does not change its typed module identity. Consumers must preserve exact binary64 values while
decoding and re-encoding. Unknown ignored members are not part of this recognized typed digest representation.

A rejected published artifact cannot supply a trusted partial interface. If required source is unavailable, report
failure with a regeneration diagnostic where applicable. Source availability may permit recompilation through the
ordinary loader, but does not authorize bypassing validation or relabeling an older artifact.

## Disposable caches

A disposable module cache has a stricter producer key than the public module interface: it records the compiler
executable's SHA-256 and exact source-byte hash. Completed-build records also check their context, module/input
identities, legacy inputs, and actual output files. Changed executable bytes, changed inputs, a bad checksum, malformed
records, or mismatched dependencies invalidate reuse. A cache miss permits an ordinary rebuild from available source.

A cache is not a replacement for an independently published source-free module. `--clean` bypasses disposable reuse; it
does not make an incompatible published artifact valid. Timestamps and a producer's unchanged display version do not
establish a cache hit. [Compiler architecture](../bifoil-compiler/ARCHITECTURE.md) defines cache ownership and
verification.

## Programs, packages, and build identity

The compiler derives an inline build identity from its canonical linked program with an empty build field. Package build
identities use their complete root manifest, including code references and, for on-demand packages, function headers.
Changing canonical lowered data, metadata, profiles, entry selection, or the selected code inventory changes that
identity. A source edit producing identical canonical output need not change the build identity.

Consumers require a well-formed build identifier and compare it exactly when restoring. The identifier is a trusted
producer claim; the VM does not authenticate the producer or reconstruct a source build from that identifier. Retain the
selected root rather than assembling a new identity from directory contents or unrelated chunks.

Each package reference must agree with its root's module identity and use its distinct content-addressed scene name. A
chunk's identity is SHA-256 of the original UTF-8 JSON payload bytes. Consumers must hash those bytes, without parsing
and reserializing first: rewriting a Float spelling or JSON layout can change the byte identity.

Eager packages verify every referenced chunk before VM startup. On-demand packages validate the complete declared header
inventory first, then verify each fetched chunk's hash, ownership, signatures, capture/continuation metadata, and
instructions before executing that code. Evicted code is verified again when fetched. Unused chunks need not be read.
Both layouts retain their normal module and aggregate admission limits.

Changing between inline, eager-package, and on-demand-package roots changes the build representation. Their saves are
not interchangeable. Old chunk files may coexist for older roots or concurrent builds; the selected root determines the
inventory. A missing or corrupt required chunk is an execution/loading error rather than permission to select a
different body or replay prior work. [On-demand code](../bifoil-runtime/LAZY_PACKAGES.md) defines loader lifetimes and
verification order.

## Checkpoints and rejection order

A supported save point is a fully prepared player-input wait. Instruction quanta, asynchronous code-fetch waits,
startup, completed execution, and failed execution are not save points. V2 checkpoints preserve active calls, locals,
captured aliases, expression temporaries, reified types, choice snapshots, option history, traversals, prose state, and
required native continuation state. Code-cache contents are excluded; resumed code loading follows the same checks.

Restore must reject unsupported checkpoint versions, profile/build mismatches, invalid references, invalid callable
views, invalid stored types/keys, inconsistent frame positions, and unprepared input states. Validation finishes before
restoring native host state or releasing the previous owned continuation. A rejected restore leaves an existing prepared
adapter session usable. Loading must not replay initializers, completed expressions, option preparation, or prior
output.

The adapter rejects an incompatible program header before constructing a host factory. It checks a package's version and
root inventory before retiring a prior session or consuming its staged code. Once a compatible package load starts, its
existing asynchronous session-lifetime rules apply; a later missing body or integrity failure does not roll back
external effects or restore an abandoned session. Cross-build save migration is outside the first milestone.

## Version changes and host requirements

A changed required container representation requires a new container version. A changed required execution meaning or
unsupported required operation requires a new instruction profile. A compiler-only format change may retain the same VM
profile, as with module v5's ordered-check requirement. Backward readers must explicitly implement each accepted
combination. No consumer silently downgrades an unknown version.

Optional representation additions may retain an existing version only when an older conforming consumer's defined
fallback preserves the claimed execution behavior. Adding a required field or relying on a previously ignored field's
new meaning is not such an addition. Development status does not waive these compatibility rules.

Extended ChoiceScript output requires the Bifoil runtime and explicit command installation. It is not executable by an
unextended ChoiceScript engine alone. The tested upstream baseline remains the unmodified pinned interpreter recorded in
the [runtime guide](../bifoil-runtime/README.md#test-independently). Custom hosts must supply the documented
choice/input, code-loading, hashing, and legacy hooks that their selected programs require. Node and browser host
requirements remain in the runtime guide; a supported wire version does not certify an untested host or engine.

## Direct acceptance evidence

[Runtime compatibility tests](../bifoil-runtime/test/compatibility.test.mjs) exercise matching program versions,
mixed/future/missing versions, original checkpoint reads, current envelopes retaining v1 execution, rejection before
restore callbacks, both package layouts, code chunk versions, host-factory ordering, and a prepared session surviving an
incompatible package command.

[Module reader tests](../bifoil-compiler/src/module_input/tests.rs) cover the producer matrix through ordinary and
streamed readers with otherwise matching digests. Existing module/cache/CLI tests cover dependency and cyclic-group
identities, corrupt-cache recovery, source removal, and atomic publication. Existing runtime package, checkpoint, and
adapter tests retain hash, inventory, continuation, and no-replay controls. Full source conformance and target-scale
resource acceptance retain their separate checklist gates.

## Progression-view producer requirement

Module format v4 requires integer query checking and lowering that preserves the checked IntProgression receiver view,
including when its retained value is IntRange. Rebuild v1/v2/v3 modules from source. Program v2 and VM profile v3 remain
unchanged: the compiler uses existing instructions on a temporary operand instead of adding an ignored optional field.


## Namespace and nested-storage producer requirement

Module v5 adds ordinary value-prefix priority over same-named type aliases, including capture and initialization checks.
Rebuild v1/v2/v3/v4 modules: older bodies can contain an incorrect enum constant with a valid public signature. Earlier
ordered-operand and checked progression-view requirements remain mandatory.

Nested shared cells are private shared definitions using ordinary initializer/dependency metadata. Their lexical sites
refer to persistent identities without declaring local copies. The compiler checks independence from enclosing
call/instance state and type parameters. Existing VM v3 loads, stores, and shared-cell checkpoint validation implement
these rules; program/package/code/checkpoint versions remain unchanged.

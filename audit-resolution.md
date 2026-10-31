# Implementation audit follow-up

Updated: 2026-10-31

The audit's reproduced compiler defects and acceptance-gate failure have targeted repairs. This is a disposition of
those findings, rather than a claim of complete language conformance. The original steering text and all 305 decision
IDs remain unchanged.

Current verification passes 570 native compiler tests, 43 release CLI tests, strict all-target Clippy, and formatting.
All 1,100 original conformance cases pass in both inline and package modes after source formatting and idempotence
checks. The runtime suite passes all 112 tests with the explicitly supplied pinned ChoiceScript engine, with no skips.
The runner has five Python regression groups; the evidence validator has three. The review corpus includes 36 new cases.
The final hardened gate passes a complete 1,100-case sweep in each output
mode with exact case IDs and frozen compiler/execution inputs. Earlier scoped controls and injected failure records
remain in private development evidence.

## Compiler artifact compatibility

Reusable modules now use `bifoil.module.v3`. Regenerate older modules from their original sources before linking them
with this compiler. A newly compiled client cannot recheck a lowered body produced by the old compiler. The VM
instruction profile remains `bifoil-vm.v2`; linked programs retain `bifoil.program.v2` and packages retain
`bifoil.package.v1`.

A separate check used the actual earlier compiler to produce the invalid typed body from the revoked-operand example.
The repaired compiler refused that genuine v2 artifact in both output modes while preserving completed roots. Current
source-free v3 compilation and package reuse remain exercised. Existing linked programs are not retroactively retyped
by the runtime.

## Finding disposition

| Finding | Current disposition | Concrete change or remaining limit |
| --- | --- | --- |
| LIA-001 | Repaired composition gate | Loaded graphs reject callable/shared/legacy-storage identity overlaps, naming both owners. Independent modules can still compile separately; ambiguous graphs cannot publish a root. |
| LIA-002 | Repaired | Reached logical left operands must be Boolean before right-side Nothing propagation. Both logical operators retain valid short circuiting. |
| LIA-003 | Repaired | Equality-based collection search/removal interfaces require Equatable elements or keys. Function storage, extraction, clear, and removeAt remain available. |
| LIA-004 | Repaired definition paths | Installed bounds are checked after the complete nominal environment exists, including unused function/class/method/alias declarations. Recursive nominal bounds retain positive controls. |
| LIA-005 | Repaired | Dependency discovery is canonical across source, cache, and artifacts. Both output modes compare cold, lost/corrupt receipt, clean, and source-free roots byte for byte. |
| LIA-006 | Repaired targeted ordered flow | Applicability, generic argument inference, and binary inference share normal-completion flow transfer. Actual lowering still checks arguments and emits each source evaluation once. |
| LIA-007 | Repaired | A known invalid fairmath base fails independently of a dynamic modifier. Modifier signs/magnitudes and endpoint behavior retain their selected rules. |
| LIA-008 | Repaired header/interpolation attribution; finer precision partial | Opening option lines, separate condition starts, and physical interpolation starts survive lowering and artifact serialization. Inner operations in a continued expression still generally inherit that expression's start line. |
| LIA-009 | Repaired targeted loop flow | Return inference shares captured-iterable nonempty evidence and joins real body/break/continue exits. An unknown iterable still includes the zero-iteration path. |
| LIA-010 | Open milestone | Admission guards remain unchanged. Paged interfaces, larger source admission, lazy runtime code loading, and target-scale incremental acceptance are still required. |
| LIA-011 | Repaired bounded marker/reuse policy; portability open | Marker comparison reads at most 65 bytes. Actual validated module reuse enables deadline checks even without a marker. Portable enforcement and the full aggregate measurement protocol remain unqualified. |
| LIA-012 | Repaired | Legacy labels are indexed once per referenced scene; indexing and reference traversal check the job budget. Matching retains the existing whitespace and ASCII case rules. |
| LIA-013 | Repaired acceptance gate | None is the only success result. Silent nonzero exits and signals fail formatting, precompilation, compilation, and execution with explicit phase/status diagnostics. A matching expected diagnostic cannot hide a terminated compiler. |
| LIA-014 | Repaired traceability | Unrelated S14 tags were removed and S14 remains pending. Reciprocal omissions were repaired; invalid statuses, stale decision text, and missing reciprocal links reject. Validation remains an integrity check. |
| LIA-015 | Partial acceptance expansion | Dynamic numeric/range/fairmath pairs now execute directly. The incompatible-save runtime test is identified and freshly exercised; actual original/edited compiler outputs also reject mismatched restores. The review map retains narrower remaining gaps. |
| LIA-016 | Repaired ordered checking and producer gate | Operators use each operand's checked type at its actual evaluation point, retaining the captured left type. Revoked nullable/Any/field/generic proofs reject. Older module formats require regeneration. |
| LIA-017 | Repaired documentation | Sole-source-site restrictions now describe compact expansion only; framed exclusive calls retain at-most-once executed initialization checks. |

[The review-obligation map](conformance/review-coverage.md) traces all 26 predetermined review cases to targeted
assertions or explicit remaining gaps. [Current implementation status](implementation-status.md) retains broader
unfinished language and acceptance work.

## Unselected profile details

The repairs do not select nominal Map-key copy broadening (LIA-C01), exact equality across differing covariant views
(LIA-D01), the complete resource measurement/reference protocol (LIA-D02), once-history evaluation timing (LIA-D03),
embedded function/continuation modes (LIA-D04), or the large-progression reference/cost refinement (LIA-D06). The v3
gate
addresses the concrete old-producer issue in LIA-D05; wider producer compatibility remains a versioned profile concern.
Composite legacy bridge ownership also remains undecided. These choices are separate from the reproduced defects.

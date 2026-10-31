# Runtime build compatibility evidence

The runtime repository owns the executable incompatible-save assertion in
[its checkpoint validation test](../../../bifoil-runtime/test/runtime.test.mjs). The test creates a valid checkpoint,
changes the program build identity, and requires restoration to fail with the different-build diagnostic. Matching
scene names do not bypass that check. It also rejects malformed saved references.

On 2026-10-31, the complete runtime suite passed 112 tests with zero skips, using an explicitly supplied, unchanged
ChoiceScript engine. The compiler and language conformance runner use explicit paths to the separate runtime checkout;
this evidence does not introduce an implicit build dependency.

This is a runtime fixture assertion, rather than a two-release browser migration test. It establishes the identity
rejection exercised by that test. Full browser, deployment, cross-device, and cross-update acceptance remain separate.

Two additional checks use actual original and edited compiler outputs from the 15,001-function code workload and the
81,918-function graph workload. Each original reaches a prepared input wait. Its checkpoint restores against that same
program and rejects against the edited program, whose real build identity differs. This exercises real compiler output
without replacing its build field manually. Separate original/restored executions verify every routine/result and
absence of replay. These are Node host assertions, not browser deployment or update-migration acceptance.

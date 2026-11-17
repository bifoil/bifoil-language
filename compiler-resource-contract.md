# Compiler resident-memory and timing contract

The user selected resident process memory on 2026-11-05. The strict budget is below 250,000,000 bytes for the compiler
and its helpers at every moment. This contract completes the quantity selection; it does not certify every workload,
host platform, or implementation gate. [Narrative measurements](../bifoil-compiler/NARRATIVE_CAPACITY.md) and the
[resource history](../bifoil-compiler/RESOURCES.md) retain their exact conditions and failed observations.

## Quantity and process scope

The relevant quantity is the maximum simultaneous sum of resident bytes over all compiler/helper processes. Include
native allocation, thread stacks, and resident library/file mappings. Exclude unmapped operating-system filesystem
caches. Count shared resident pages per process when using summed RSS; that is a conservative process accounting
quantity, not a managed-heap limit or a physical-page union.

A compiler helper is a process required for discovery, compilation, linking, publication, or owned cleanup. Optional
benchmark controllers, workload generation, compiler construction, and post-build runtime tests are separate work.
Their exclusion does not permit required work to be moved outside the measured job. A helper introduced later must
be included from its startup through exit, including overlap with the compiler and other helpers.

Independent per-process maxima cannot replace a simultaneous aggregate when multiple processes overlap. Periodic
sampling alone cannot establish the strict peak. Kernel high-water accounting and conservative continuous enforcement
must cover the actual process scope. [Linux accounting](https://man7.org/linux/man-pages/man2/getrusage.2.html) states
the distinction between a largest child and a process-tree peak.

## Current Linux mechanism and reference

The current x86-64 Linux compiler is one native process and starts no compiler helpers. Its threads share that process
address space. The native observer records the kernel process peak through GNU Time, including startup and exit,
so the observed process peak is the aggregate for this verified single-process scope. Adding a helper invalidates
that shortcut until its simultaneous accounting and enforcement are qualified.

Before parsing arguments or opening the project, the compiler applies a virtual-address-space limit of at most
240,000,000 bytes and preserves a stricter inherited limit. Native allocation and mappings are covered; allocator arenas
are bounded before worker creation. The stricter address-space quantity leaves at least ten million bytes below the
selected resident-memory budget. Startup is included in kernel peak observations; this is a fixed executable/reference
qualification, not authorization for injected startup code or an unmeasured helper tree. [Linux limit
semantics](https://man7.org/linux/man-pages/man2/getrlimit.2.html) describe the mechanism and its allocation failures.

The reference machine is an AMD Ryzen 7 6800H, eight physical cores and sixteen logical CPUs, x86-64 WSL2 Linux
6.18.54.1-microsoft-standard-WSL2. Source/cache/output storage conditions distinguish the Windows 9p mount from Linux
ext4. The measured compiler is a native release build. Input prefetch uses at most four threads; completed-build
verification uses at most sixteen. No helper-process budget is assumed merely because those threads run concurrently.

Other compiler platforms require corresponding qualified enforcement/accounting before a compliance claim. Passing
Windows Node runtime tests does not qualify a Windows native compiler. The source/workload envelope and timing
conditions remain explicit in their measurement records.

## Timing and success

Incremental end-to-end compilation using precompiled modules must finish in less than ten seconds within the published
supported workload/reference conditions. Include startup, discovery, required compilation/linking, artifact writes,
and compiler-owned cleanup. Use a monotonic wall clock. Warmed native work still checks its 9.5-second internal
deadline. Clean work scales with total input and is measured separately.

Keep successful compilation, budget enforcement, and observed peaks distinct. An allocation failure, deadline error,
signal, or rejected workload is a failed build. A low memory peak on a failed build does not demonstrate successful
capacity. Retain raw failures and worst observations rather than only medians. Full workload coverage, broader
platforms, failure-boundary testing, and the remaining checklist gates are not waived by the selected metric.

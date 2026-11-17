# Complete language implementation checklist

## Language requirements ([steering](language-steering.md))

### Scope and compatibility

- [ ] **S01** Provide a strongly statically typed, feature-complete language compatible with ChoiceScript.

- [x] **S02** New syntax takes primary inspiration from Kotlin and Python.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [ ] **S03** Bifoil has its own syntax. Projects may include unchanged legacy ChoiceScript files through a
      compatibility front end.

- [ ] **S04** Legacy files retain ChoiceScript's original semantics, including its scope and case rules. New Bifoil
      rules apply to new Bifoil source.

- [x] **S05** Narrative-block syntax and unquoted prose follow T01. ([tests](conformance/expressions.json))

- [x] **S06** Use a native compiler written in C++, Rust, or Go. ([source](../bifoil-compiler/Cargo.toml))

- [x] **S07** The language must support pre-compilation. Ahead-of-time generation and reusable, independently compiled
      modules are required under S10. Native story executables remain unselected.
      ([tests](../bifoil-compiler/tests/cli/packages.rs))

- [ ] **S08** Keep peak aggregate compiler-and-helper memory strictly below 250,000,000 bytes, using the measurement and
      enforcement protocol required by S13.

- [ ] **S09** Complete incremental end-to-end builds in less than ten seconds within the supported workload and
      reference environment under S14. Diagnose unsupported inputs and resource-budget failures under S15.

- [x] **S10** The first compiler milestone requires ahead-of-time Bifoil-to-ChoiceScript compilation and reusable,
      independently compiled module artifacts. Native story executables have not been selected as an initial
      requirement. ([tests](../bifoil-compiler/tests/cli/packages.rs))

- [x] **S11** Bifoil runtime extensions are permitted. A required runtime layer or engine extensions may provide
      features; compatibility requirements must be stated explicitly and Bifoil semantics preserved. Unmodified-engine
      compatibility is not an initial requirement. ([interface](../bifoil-runtime/PROTOCOL.md))

- [ ] **S12** Typed Bifoil and unchanged legacy ChoiceScript interact through explicit typed bridges. Cross-language
      calls and shared-state access require declared interfaces and checked conversions; unknown legacy values are never
      trusted implicitly. Legacy source retains its original semantics.

- [ ] **S13** Peak aggregate compiler-and-helper memory must remain below 250,000,000 bytes at every moment. This is not
      an average or compiler-heap-only allowance. Specify and validate the exact measurement and enforcement protocol.

- [ ] **S14** Complete incremental end-to-end compilation using precompiled modules in less than ten seconds for a
      published maximum-size/complexity workload on reference hardware. Specify and test the workload, hardware, cache
      conditions, and full-pipeline measurements. Allow clean-build time to scale with total input.

- [x] **S15** Inputs beyond the supported compilation envelope receive an explicit diagnostic. Compilation errors and
      resource-budget failures report failure rather than claiming a successful build.
      ([tests](../bifoil-compiler/tests/cli/module_capacity.rs))

### Layout, spelling, and names

- [x] **L01** Ordinary code blocks use indentation and a colon to open the body.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L02** On ordinary code lines, each tab and each complete group of four spaces adds one structural indentation
      level. Leftover spaces count as alignment. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L03** One tab followed by four spaces means two structural levels. Six spaces mean one level plus two alignment
      spaces. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L04** Tabs and spaces may be mixed for alignment under the preceding counting rule.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L05** Ordinary expressions may continue inside parentheses or after an unfinished operator, such as `+` or `=`.
      Continuation indentation serves as alignment. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L06** Block expressions such as `if` retain their structural indentation rules within expressions.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L07** Corresponding conditional branch headers align, and corresponding branch bodies use the same indentation
      level. Standard formatting normalizes this structure. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L08** Names and keywords are case-sensitive in new Bifoil source. Legacy source keeps its original rules.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L09** Conditional branch spellings and their formatting follow E08.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L10** The function-declaration keyword follows F01. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **L11** Logical NOT uses `!`; AND/OR spelling and behavior follow E02. Equality operators follow E03 and E28-E30.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

### Bindings, scope, and nullability

- [x] **B01** Infer variable types when possible. Allow optional annotations and require them when inference cannot
      establish a type. Static checking remains mandatory.
      ([evidence](conformance/cases/binding-inference-source-free-checkpoint/main.bfl))

- [x] **B02** `val` declares a binding that cannot be reassigned; `var` declares a reassignable binding. Reassignment
      retains the binding's static type. ([tests](conformance/generics.json))

- [x] **B03** Keep binding mutability separate from the mutability of referenced contents. Collection-container
      mutability and aliasing follow D02/D05; data-instance sharing and field mutability follow U03/U05. Binding
      reassignment does not freeze or implicitly deep-copy referenced objects.
      ([evidence](conformance/cases/nominal-contracts-source-free-checkpoint/main.bfl))

- [x] **B04** Names have block scope: they are visible only within their declaring block and nested blocks, with
      declaration order governed by B10. Captured bindings may remain alive under F21.
      ([tests](conformance/generics.json))

- [x] **B05** Reject shadowing: a declaration cannot reuse a currently visible binding name. This includes implicit loop
      bindings. Same-scope function overload sets follow F23; nested shadowing remains prohibited.
      ([evidence](conformance/foundations.json))

- [x] **B06** Local `val` and `var` declarations may omit their initializer when they have an explicit type. Every read
      requires proven initialization.
      ([evidence](binding-flow-semantics.md#reads-and-writes))

- [x] **B07** Each delayed-initialization `val` binding must be initialized at most once. Control-flow checks must
      enforce this per binding.
      ([evidence](binding-flow-semantics.md#reachability-and-branch-joins))

- [x] **B08** Types are non-null by default. `T?` permits `null`, which must be handled before the value can be used as
      `T`. ([tests](conformance/generics.json))

- [x] **B09** Null checks automatically narrow a value's type where control flow proves that the value remains
      unchanged. Explicit handling is required when that proof is unavailable.
      ([evidence](binding-flow-semantics.md#refinement-invalidation))

- [x] **B10** A local variable name is visible from its declaration through the rest of its block and nested blocks.
      Local variable names are not visible before their declarations; function names retain F14's scope-wide visibility.
      ([tests](conformance/generics.json))

- [x] **B11** Safe member access and method calls use `?.`. Evaluate the receiver once; when it is null, yield null and
      skip method arguments and the call. Calls retain the ordinary suspension-effect checks.
      ([tests](conformance/generics.json))

- [x] **B12** Use `?:` for lazy null fallback. Evaluate the left operand once; evaluate the fallback only when that
      value is null. Precedence follows E12; compatible joins and explicit result contexts determine its type.
      ([evidence](equality-and-nullability.md))

- [x] **B13** Postfix `!!` converts `T?` to `T` with a runtime null check. Evaluate its operand once; a null value
      reports a runtime error, otherwise produce the non-null value. ([tests](conformance/generics.json))

- [x] **B14** Lift approved conversions through nullable types: convert a present value and preserve null. This includes
      `Int?` to `Float?`, `Char?` to `String?`, and nullable forms of approved collection copying and widening.
      ([evidence](conformance/cases/nullable-conversions-source-free-checkpoint/main.bfl))

- [x] **B15** Safe indexing of a nullable `String`, list, or map uses `?[index]`: for example, `items?[i]` or
      `mapping?[key]`. Evaluate the receiver once; null yields null and skips the index/key expression. A non-null
      receiver follows ordinary indexing, bounds, and missing-map-key rules. ([tests](conformance/generics.json))

- [x] **B16** Safely invoke a nullable function value with `?.(arguments)`, for example `callback?.(value)`. Evaluate
      the callable once; null yields null and skips arguments and the call. Function-value argument rules and
      suspension-effect checks still apply. ([tests](conformance/generics.json))

- [x] **B17** Nullable application flattens to one layer. For example, lookup in `Map<String, Int?>` returns `Int?`;
      absence and a stored null remain indistinguishable through lookup alone. Explicitly repeated nullable markers such
      as `Int??` are errors. ([tests](conformance/generics.json))

- [x] **B18** A variable declaration initialized only with `null` requires an expected type: `val name: String? = null`
      is valid, while `val name = null` is an error. Empty and all-null collection literals retain D11's expected-type
      requirement. ([tests](conformance/generics.json))

- [x] **B19** Subject-based `when` cases contribute to automatic null narrowing. Infer non-null values in branches that
      exclude null; narrow an original binding only while flow analysis proves it still matches the captured subject.
      Writes, calls, and suspension must not invalidate that proof.
      ([evidence](binding-flow-semantics.md#refinement-invalidation))

- [x] **B20** Expose Any as the universal non-null value type and Any? as its nullable form. Operations require
      appropriate static type information. Universal types do not introduce automatic Any fallback in common-type
      inference. ([tests](conformance/generics.json))

- [x] **B21** Test types in ordinary expressions with is and !is, for example value is Character or value !is Character.
      Existing case is Variant patterns remain available. ([tests](conformance/generics.json))

- [x] **B22** Use as for checked casts and as? for nullable casts, such as value as Character and value as? Character. A
      dynamic mismatch reports a runtime error for as and yields null for as?, subject to B24.
      ([tests](conformance/generics.json))

- [x] **B23** Casts check runtime type compatibility without scalar conversions or container copies. Use explicit
      conversion operations for value conversions; ordinary assignment and argument conversions remain available.
      ([tests](conformance/generics.json))

- [x] **B24** Reject a cast between concrete types when it is provably impossible at compile time, rather than
      generating an inevitable runtime error or null result. ([tests](conformance/generics.json))

- [x] **B25** Successful general type tests automatically narrow bindings in if branches and when cases where safe.
      Reuse the existing proof rules for writes, calls, aliases, and suspension; existing null narrowing remains
      available.
      ([evidence](binding-flow-semantics.md#refinement-invalidation))

### Boolean and text types

- [x] **P01** Use Boolean as the boolean type, with lowercase true and false literals.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P02** Provide immutable String values and a distinct Char type. String indexing produces Char. Immutability
      concerns the contents; a var binding may still be reassigned. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P03** Use Unicode scalar values as the element model for string length, indexing, and Char: a Unicode code point
      excluding surrogates. A supplementary character such as U+1F600 occupies one element; combining sequences may
      occupy multiple elements. Legacy ChoiceScript retains S04. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P04** String indexing uses s[i] with zero-based, nonnegative Int indexes. Provably invalid constant indexes are
      compile errors; other out-of-bounds indexes are runtime errors. Negative indexes are invalid.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P05** Ordinary String literals use double quotes and Char literals use single quotes. Escape forms follow P09.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P06** Ordinary String literals support ${expression} interpolation. Evaluate substitutions left to right under
      the enclosing expression's suspension permissions, preserving completed evaluation across suspension. Prose and
      option-label interpolation retain their non-suspending restrictions.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P07** Multiline String literals use triple double quotes with ordinary escape rules and interpolation.
      Common-indent stripping, delimiter lines, tabs, blank content, and retained newlines follow the text contract.
      ([evidence](text-semantics.md))

- [x] **P08** Prose and option-label interpolation directly render non-null String, Char, Int, Float, and Boolean
      values. Nullable values, Unit, collections, function values, scene references, and other types require explicit
      conversion to a renderable value. Exact boolean and numeric formatting follows the text contract.
      ([evidence](conformance/cases/primitive-text-contracts-source-free-checkpoint/main.bfl))

- [x] **P09** Quoted String and Char literals, including triple-quoted strings, accept both braced Unicode scalar
      escapes (`\u{41}`, `\u{1F600}`; one to six hexadecimal digits) and fixed-width escapes (`\u0041`, `\U0001F600`;
      four or eight hexadecimal digits). Also support `\\`, `\"`, `\'`, `\n`, `\r`, `\t`, and `\${`. Unknown escapes and
      invalid scalar values are errors. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P10** Triple-quoted strings strip common leading indentation from nonblank lines, while retaining newlines and
      other content. Tabs, blank lines, delimiter placement, and source newline normalization follow the text contract.
      ([evidence](text-semantics.md))

- [x] **P11** Obtain String length with the length property, for example text.length. The result is Int and counts
      Unicode scalar elements. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P12** When either operand of + is String, accept directly renderable non-null primitive operands and format them
      as interpolation would. Ordinary left-to-right evaluation still applies; this rule does not introduce general
      implicit conversion of numbers or booleans to String in assignments or calls.
      ([evidence](conformance/cases/primitive-string-assignment-error/main.bfl))

- [x] **P13** Automatically widen Char to a one-element String in assignments, function arguments, and string
      operations. The conversion preserves the scalar; exact Char parameter matches remain preferable in overload
      resolution. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P14** String values preserve their scalar sequences without implicit Unicode normalization. String equality
      compares exact scalar sequences; canonically equivalent spellings may compare unequal.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P15** String supports <, <=, >, and >= using case-sensitive scalar lexicographic order: compare scalar numeric
      values left to right, with a matching shorter prefix sorting first. Locale-aware sorting is a separate topic.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **P16** Extract a substring with text.substring(start, endExclusive). Both Int bounds are required and use scalar
      positions, with 0 <= start <= endExclusive <= text.length. The end is excluded and equal bounds produce an empty
      String. Provably invalid constant bounds are compile errors; other invalid bounds are runtime errors.
      ([tests](../bifoil-runtime/test/text.test.mjs))

### Numeric types and conversions

- [x] **N01** `Int` and `Float` are distinct static types. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N02** `Int` is signed 32-bit: −2,147,483,648 through +2,147,483,647. Out-of-range constants are compile errors;
      arithmetic overflow is checked at runtime. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N03** `Float` uses finite binary64 with ordinary floating-point rounding. Division by zero, overflow to
      infinity, and invalid non-finite results are errors. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N04** Automatically widen `Int` to `Float` in assignments, function arguments, and mixed arithmetic. Every
      signed 32-bit integer is exactly representable in binary64. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N05** `Float` to `Int` requires an explicit conversion. It truncates toward zero, then rejects a converted
      result outside the signed 32-bit range. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N06** `Int / Int` returns an `Int` truncated toward zero. A `Float` operand makes division produce a `Float`.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N07** Integer `%` is truncation remainder: mathematically, `a % b = a − (a / b) × b`. Its sign follows the
      dividend when the remainder is nonzero. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N08** Support binary fairmath `%+` and `%-`; numeric rules follow N10-N12 and the [pinned ChoiceScript
      baseline](language-steering.md#fairmath-numeric-contract-and-source-baseline), compounds follow N09, and grouping
      follows N13. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N09** Add fairmath compound statements `%+=` and `%-=` alongside the value-producing binary `%+` and `%-`
      operators. Compound forms follow E11's target-once capture and read order.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N10** Both fairmath operands may be `Int` or `Float`; the rounded result is `Int`. Use binary64 intermediates
      and directional integer rounding, including when both operands are `Int`, rather than N06's ordinary integer
      division. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N11** Preserve the pinned ChoiceScript interpreter's directional rounding and clamps. The base must be in
      `0..100` inclusive; provably invalid constants are compile errors and invalid dynamic bases are runtime errors.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N12** The fairmath change operand may be any finite numeric value, including negatives and magnitudes above 100.
      There is no separate percentage-range restriction; the operator and modifier sign determine direction.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **N13** Require explicit parentheses when binary `%+` or `%-` combines with another binary operation or a fairmath
      chain. Standalone `a %+ b` and `a %- b` remain valid. Ordinary arithmetic retains E04's conventional precedence;
      fairmath combinations have no implicit chain associativity. ([tests](../bifoil-runtime/test/runtime.test.mjs))

### Type declarations and aliases

- [x] **U01** Support transparent `typealias` declarations, for example `typealias Transform = (Int) -> Int`. An alias
      denotes its existing type without another runtime identity; generic aliases follow G01. Placement, scope-wide
      resolution, and cycle rules follow U25-U27; visibility follows explicit module interfaces.
      ([evidence](modules-and-names.md))

- [x] **U02** Support user-defined data types with named, statically typed fields. ([tests](conformance/nominals.json))

- [x] **U03** Declare fields in an indented `data class` block: `data class Character:` with declarations such as `val
      name: String` and `var health: Int`. Field types are explicit; `val` fields cannot be reassigned, while `var`
      fields can. ([tests](conformance/nominals.json))

- [x] **U04** Generate a field constructor called with the data-type name, for example `Character(name = "Ada", health =
      100)`. Parameters follow field declaration order and the existing positional/named/default-argument rules. Field
      initializers supply defaults evaluated per construction when omitted. ([tests](conformance/nominals.json))

- [x] **U05** Assigning or passing a data instance shares that instance. Reassignable-field updates are visible through
      aliases; copying requires an explicit operation. Referenced field values retain their own semantics, and a `val`
      instance binding does not freeze its `var` fields. ([tests](conformance/nominals.json))

- [x] **U06** Data-instance `==` and `!=` use structural equality over corresponding fields of compatible types.
      Equality is available only when every field supports it. Nominal compatibility follows U07; exact equality follows
      E28-E30.
      ([evidence](equality-and-nullability.md))

- [x] **U07** Data types are nominal: distinct declarations define distinct types even when their fields match.
      Conversion between such types requires an explicit operation. Transparent aliases under U01 do not create another
      type. ([tests](conformance/nominals.json))

- [x] **U08** Support enum types as closed sets of typed, named constants with stable equality and exhaustive `when`
      coverage. Declaration and case-reference syntax follow U12-U13. Data-bearing variants belong to the separately
      selected closed sum types under U14. ([tests](conformance/nominals.json))

- [x] **U09** Data types support member `fun` and `suspend fun` declarations, called through an instance. Existing
      parameter, return, overload, and suspension rules apply. ([tests](conformance/nominals.json))

- [x] **U10** Methods have an implicit receiver named `this`: write `this.health` inside a method, while
      `instance.heal(amount)` supplies the receiver without a declared parameter. Bare member access follows U23 and
      bound references follow F43-F44; remaining receiver and lookup details are open.
      ([evidence](conformance/cases/nominal-contracts-source-free-checkpoint/helpers.bfl))

- [x] **U11** Data fields and methods are public by default, with explicit `public`/`private` modifiers. Private members
      are inaccessible from outside the data type. File-level visibility follows M08/M16.
      ([tests](conformance/nominals.json))

- [x] **U12** Declare a plain enum with `enum`, not `enum class`: `enum Mood:` followed by named cases such as `Happy`
      and `Sad` on separate indented lines. ([tests](conformance/nominals.json))

- [x] **U13** Enum cases may use expected-type shorthand: when an expected enum type uniquely resolves a case, a bare
      name such as `Happy` is permitted; otherwise use `Mood.Happy`. Conflicts with ordinary bindings follow U24; exact
      import rules remain open.
      ([evidence](modules-and-names.md))

- [x] **U14** Support closed sum types with typed payload variants, separate from plain enums. Their declaration,
      construction, matching, and equality follow U15-U22. ([tests](conformance/nominals.json))

- [x] **U15** Declare a closed sum type with `sealed class`, for example `sealed class Outcome:`. This does not select
      general class inheritance. ([tests](conformance/nominals.json))

- [x] **U16** Declare variants inside the sum-type block with `case`, such as `case Success(value: String)` and `case
      Pending`. Payload types are explicit; payload-free variants are allowed. ([tests](conformance/nominals.json))

- [x] **U17** Variant payload field bindings are immutable. Referenced values retain their existing mutability; fixed
      bindings do not recursively freeze their contents. ([tests](conformance/nominals.json))

- [x] **U18** Each variant has a distinct, nameable nominal subtype, such as `Outcome.Success`, which may widen to its
      enclosing sum type. Unrelated variants remain distinct. ([tests](conformance/nominals.json))

- [x] **U19** Construct payload variants with qualified names, such as `Outcome.Success("Ada")`; payload-free constants
      use `Outcome.Pending`. Payload constructors follow existing positional/named/default-argument rules.
      ([tests](conformance/nominals.json))

- [x] **U20** `when` supports explicit `is` variant tests and payload destructuring: `case is Outcome.Success:` and
      `case is Outcome.Success(value):`. The marker distinguishes patterns from ordinary value expressions.
      ([tests](conformance/nominals.json))

- [x] **U21** Destructured payload names create inferred immutable bindings scoped to the matched branch. For example,
      `case is Outcome.Success(value):` binds `value` without an explicit `val`; no-shadowing and capture rules apply.
      ([tests](conformance/nominals.json))

- [x] **U22** Through a compatible sum type, different variants compare unequal; matching variants compare payloads
      structurally when all payload types support equality. Exact comparison retains E28-E30's type and recursive
      equality rules.
      ([evidence](equality-and-nullability.md))

- [x] **U23** Inside a method, allow bare instance-member names such as health and heal(...) when lookup resolves them
      unambiguously. Explicit this.health and this.heal(...) remain available; detailed lookup interactions must respect
      the existing no-shadowing rules.
      ([evidence](../bifoil-compiler/src/tests/members.rs))

- [x] **U24** If an ordinary visible binding and an expected-type enum case are both interpretations of a bare name,
      report a name conflict and require qualification. Do not silently prefer either interpretation.
      ([tests](conformance/nominals.json))

- [x] **U25** Permit transparent typealias declarations at file scope and inside ordinary lexical blocks. They introduce
      no new runtime type; generic aliases remain supported under G01. ([tests](conformance/nominals.json))

- [x] **U26** A type-alias name is visible throughout its enclosing scope, including before its declaration, subject to
      alias-cycle checks. Local variable visibility remains unchanged. ([tests](conformance/nominals.json))

- [x] **U27** Reject cycles through transparent alias expansion, such as typealias Nested = List<Nested>. Recursive
      structures must pass through nominal data or sum types; nominal recursion is not prohibited.
      ([tests](conformance/nominals.json))

- [x] **U28** Separate private field access from generated constructor inputs. If a data class is externally
      constructible, outside callers may supply a private field constructor parameter but cannot read or update the
      private field afterward. ([tests](conformance/nominals.json))

- [x] **U29** Generate explicit shallow data-instance copying with instance.copy(...): supplied fields replace values,
      and omitted fields retain their current values. The new instance shares referenced field values according to their
      ordinary semantics. Private inputs follow U28. Reserve the generated member name copy: a user-defined field or
      method with that name is a compile error. Copy evaluation follows receiver-first calls and post-argument field
      reads.
      ([evidence](collection-operations.md#generated-data-copy))

- [x] **U30** After narrowing a sum value to a payload-bearing variant, allow named payload-field access, such as
      result.value. Payload bindings remain immutable; the existing destructuring patterns remain available.
      ([tests](conformance/nominals.json))

- [x] **U31** Use _ as an ignored payload-pattern position, for example case is Outcome.Success(_):. It creates no
      binding and is exempt from the no-shadowing rule. ([tests](conformance/nominals.json))

- [x] **U32** Initially limit payload patterns to one level. Bind payload values and use another when to inspect nested
      variants; recursive nested-pattern syntax has not been selected. ([tests](conformance/nominals.json))

- [x] **U33** Comma-separated case alternatives introducing payload bindings must all bind the same names with
      compatible types. Infer each shared branch binding using the existing compatible-type join rules; no-shadowing and
      capture rules still apply. ([tests](conformance/nominals.json))

### User-defined generics

- [x] **G01** Support type parameters on named functions, data classes, sealed sum types, and transparent type aliases.
      Built-in collection type parameters remain supported. ([tests](conformance/generics.json))

- [x] **G02** Function type parameters precede the name: `fun <T> identity(value: T) -> T = value`. Generic data and sum
      types use name-following parameters, such as `Box<T>`. ([tests](conformance/generics.json))

- [x] **G03** Infer generic call and constructor type arguments from supplied arguments and expected types when
      unambiguous. Allow explicit arguments, such as `identity<Int>(3)`, and require them when inference cannot resolve
      the types. Function parameter annotations remain mandatory.
      ([evidence](function-contracts.md))

- [x] **G04** Unconstrained type parameters are nullable-capable: `T` may stand for `String?`. An unmarked type
      parameter alone does not prove non-nullness; applying `T?` follows B17's nullable flattening.
      ([tests](conformance/generics.json))

- [x] **G05** Support static nominal bounds and operation-capability requirements on type parameters, such as supported
      equality and stable map-key eligibility. Automatic qualification, capability names, and constraint syntax follow
      G09-G13; enforce the complete constraint rules.
      ([evidence](type-constraints.md))

- [x] **G06** User-defined generic type parameters are invariant by default, with optional checked `in`/`out`
      declaration-site variance. Reject field or method usage that violates the declared variance. Variance uses
      subtyping and does not introduce value-conversion or copying adapters.
      ([evidence](../bifoil-compiler/src/declarations/variance.rs))

- [x] **G07** Support existential/star projections, such as `Box<*>`, that hide a type argument. Permit only operations
      the type checker proves safe from the projected argument's bounds.
      ([evidence](projection-semantics.md))

- [x] **G08** Check generic bodies at their definition against their declared constraints; invalid bodies are errors
      even when unused. Every instantiation must satisfy the constraints. This does not choose a code-generation
      strategy. ([tests](conformance/generics.json))

- [x] **G09** Automatically derive built-in generic capability qualification from the type and its fields or payloads,
      without a separate author opt-in. Existing structural equality remains available under the previously selected
      rules.
      ([evidence](capability-semantics.md))

- [x] **G10** Name the equality capabilities Equatable and StableKey. Equatable permits supported equality operations;
      StableKey additionally permits set-element and map-key storage with equality that cannot change while stored.
      ([tests](conformance/generics.json))

- [x] **G11** Support inline generic bounds, such as fun <T: Equatable> same(...), and trailing where clauses for
      additional nominal bounds or capabilities. Complete declaration grammar remains to be specified.
      ([evidence](development-source-grammar.md#files-and-declarations))

- [x] **G12** Combine requirements conjunctively with repeated comma-separated constraints, for example where T:
      Outcome, T: Equatable. This does not introduce general intersection types. ([tests](conformance/generics.json))

- [x] **G13** A bound T: Any excludes nullable type arguments. Unconstrained T remains nullable-capable under G04.
      ([tests](conformance/generics.json))

- [x] **G14** Generic inference uses existing compatible-type joins for arguments constraining the same parameter: Int
      and Float arguments may infer Float and convert the Int argument. Do not infer container-family copies or fall
      back to arbitrary Any.
      ([evidence](conformance/type-interactions.md))

- [x] **G15** Retain runtime generic type arguments for type tests, including empty collections: value is List<Int> is
      permitted. Tests follow the chosen subtype rules without scalar conversions or container copying. This does not
      select a code-generation strategy. ([tests](conformance/generics.json))

### Expressions and conditionals

- [x] **E01** Conditions require boolean values. Numbers, strings, and nullable values require explicit tests; they have
      no implicit truthiness conversion. ([tests](conformance/expressions.json))

- [x] **E02** Logical operands must be booleans. `&&` and `||` short-circuit: the right operand is skipped when the left
      already determines the result. ([tests](conformance/expressions.json))

- [x] **E03** `==` and `!=` require compatible types. Unrelated types are compile errors; Int/Float comparisons use the
      agreed widening, and nullable values may be compared with `null`. Function-value comparisons follow F39; the
      separately requested `===` and `!==` operators follow E28.
      ([evidence](equality-and-nullability.md))

- [x] **E04** Use conventional precedence: multiplication/division before addition/subtraction, comparisons before `&&`,
      and `&&` before `||`. Parentheses override grouping. ([tests](conformance/expressions.json))

- [x] **E05** Explicit comparisons remain valid. Encourage integer range membership using `in` for suitable bounds
      checks. ([tests](conformance/expressions.json))

- [x] **E06** `if` may be a statement or an expression. A value-producing form must cover every path and yield
      compatible branch types. ([tests](conformance/expressions.json))

- [x] **E07** A value-producing `if` requires an `else`. Each branch's final expression supplies its value; earlier
      statements may prepare the result. ([tests](conformance/expressions.json))

- [x] **E08** Both `elif` and `else if` introduce additional conditional branches with identical meaning. Formatting
      preserves the author's spelling; alignment follows L07. ([tests](conformance/expressions.json))

- [x] **E09** Ordinary binary operators fully evaluate the left operand before the right; precedence determines
      grouping. The selected short-circuit rules still apply. ([tests](conformance/expressions.json))

- [x] **E10** For plain `=` assignments, evaluate and capture target receivers and indexes/keys once, from left to
      right, before evaluating and converting the right-hand side; then write. Dynamic bounds checks follow the
      operation contract. ([tests](conformance/expressions.json))

- [x] **E11** Support compound assignment statements `+=`, `-=`, `*=`, `/=`, and `%=` where their operators and target
      types permit them. Capture and read the target once before evaluating the right-hand side; apply the existing
      operator, overflow, conversion, and assignment rules. Fairmath `%+=` and `%-=` follow the same target order with
      N09-N12's numeric rules. ([tests](conformance/expressions.json))

- [x] **E12** Use Kotlin's precedence for `?:`: arithmetic, ranges, and infix range forms/modifiers bind more tightly;
      `in`/`!in`, comparisons, equality, `&&`, and `||` bind less tightly. Repeated fallbacks group right-to-left:
      `a ?: (b ?: c)`. Fairmath's relative grouping remains subject to N13.
      ([tests](conformance/expressions.json))

- [x] **E13** Common-type inference for value-producing branches and function returns may use approved scalar/nullable
      widening and widening through immutable collection layers. Do not infer a common type by copying between mutable
      and immutable container families; a suitable explicit expected type may request approved copies.
      ([tests](conformance/expressions.json))

- [x] **E14** Support `when` as a multi-branch statement or expression. Value-producing branches require compatible
      result types under E13/E25; coverage follows E21.
      ([evidence](conformance/cases/when-contracts-source-free-checkpoint/helpers.bfl))

- [x] **E15** Support subject-based `when value:` and subjectless `when:`, each with indented branches. Subject-based
      cases compare against one evaluated value; subjectless cases test Boolean conditions.
      ([tests](conformance/expressions.json))

- [x] **E16** Use `case` with colon branch headers, such as `case 1:` or `case condition:`, followed by an indented
      body. The fallback header is `else:`. Branch results follow E22; fallback placement follows E33.
      ([tests](conformance/expressions.json))

- [x] **E17** Subject-based cases support compatible-type value equality, null for nullable subjects, and `in`/`!in`
      range or collection tests. Sum-type variant patterns follow U20-U21.
      ([evidence](conformance/cases/when-values/main.bfl))

- [x] **E18** Allow comma-separated alternatives in one `when` branch, including multiple value cases or multiple
      Boolean conditions in a subjectless form. Test alternatives left to right and stop at the first match.
      ([tests](conformance/expressions.json))

- [x] **E19** Evaluate a `when` subject once, then test branches in source order until a match and execute only that
      branch. Subjects and case-test expressions follow the enclosing context's suspension permissions; preserve
      completed evaluation when resuming. Ordinary non-suspending state changes remain allowed.
      ([tests](conformance/expressions.json))

- [x] **E20** Allow overlapping `when` matches; selection follows E19. Provably unreachable later branches may receive
      warnings. ([tests](conformance/expressions.json))

- [x] **E21** A value-producing `when` may omit its fallback when coverage of every possible subject is proven, such as
      true and false for Boolean; otherwise require a fallback. Statement forms need not produce a value and follow E23
      when unmatched. Exact coverage analysis remains to be specified.
      ([evidence](conformance/cases/when-generic-constant-coverage-source-free/helpers.bfl))

- [x] **E22** A value-producing `when` branch supplies its result through its final expression, matching value-producing
      `if` branches. Earlier statements may prepare the result; early control transfers follow their own rules.
      ([tests](conformance/expressions.json))

- [x] **E23** If a statement-form `when` has no matching branch or `else`, execute no branch and continue normally.
      ([tests](conformance/expressions.json))

- [x] **E24** A subject-based `when` may declare an immutable subject binding: `when val value = expression:`. The
      binding is visible in case tests and branch bodies but unavailable after the `when`. Existing no-shadowing and
      capture-lifetime rules apply. ([tests](conformance/expressions.json))

- [x] **E25** Expose the bottom type `Nothing`, which has no values and is compatible with every result type. Paths that
      never produce a value do not force incompatible branch-result types. This does not introduce exceptions or
      additional control-transfer operations. ([tests](conformance/expressions.json))

- [x] **E26** Existing `return`, `break`, `continue`, and `goto` transfers may appear in expression positions, such as
      `val name = maybeName ?: return`. Each transfer must remain valid in its function, loop, or story context; a
      transferring path produces no value and has type `Nothing`. ([tests](conformance/expressions.json))

- [x] **E27** Plain `=` assignment is a statement, not a value-producing expression. It changes a binding or container
      element under E10's target-first evaluation order. Compound updates retain E11's statement forms.
      ([tests](conformance/expressions.json))

- [x] **E28** Support `===` and `!==` as exact type-and-value equality operators alongside `==` and `!=`. Compare
      without widening: different non-null value types are unequal, so `3 === 3.0` is false. Comparable values of the
      same type use value equality; `!==` negates that comparison. Nullable and composite comparison follow E29-E30.
      ([evidence](equality-and-nullability.md))

- [x] **E29** Exact equality compares contained values or null. Two nulls are equal regardless of their nullable
      annotations; one null is unequal to a present value. A present `Int?` containing 3 is exactly equal to `Int` 3.
      Conversions performed before comparison determine its values; composite comparison views follow E30.
      ([tests](conformance/expressions.json))

- [x] **E30** Collections, data instances, and eligible sum values support typed structural exact equality using their
      declared comparison views. Collection families/type arguments or nominal comparison types must match; recursively
      compare supported contents without widening or copying. A covariant view can therefore compare exactly equal to an
      independently constructed value with that same view, while retained construction types remain available to type
      tests and casts. Sum-specific eligibility follows U22.
      ([evidence](comparison-view-equality.md#distinguishing-examples))

- [x] **E31** If an operand has static type Any or Any? and its concrete equality capability is unknown, require
      narrowing or other static proof of equality eligibility before comparison. Existing null comparisons remain
      available; this does not introduce runtime failure-based equality dispatch.
      ([tests](conformance/expressions.json))

- [x] **E32** Support Boolean when pattern guards, such as case is Outcome.Success(value) if value != "":. Payload names
      are available to the guard. Evaluate it once after the pattern matches, under the enclosing suspension
      permissions; a false guard continues to later cases. ([tests](conformance/expressions.json))

- [x] **E33** A when may have at most one else: fallback, which must follow all case branches. Choice-fallback placement
      remains a separate matter. ([tests](conformance/expressions.json))

- [x] **E34** Ordinary and exact structural equality handle eligible cyclic data or collection graphs without infinite
      recursion. Track pairs being compared so revisiting a pair terminates that recursive step. Shared-reference layout
      does not determine equality; the ordinary and exact type rules remain distinct.
      ([tests](conformance/expressions.json))

- [x] **E35** Initially fail fast on checked runtime failures, including overflow, invalid indexes, and failed checked
      casts: stop the story and report the original Bifoil source location. Catchable language-level exceptions are
      deferred. Compilation and budget errors follow S15. ([tests](conformance/expressions.json))

### Collections

- [x] **D01** Provide `List<T>`, `Set<T>`, and `Map<K, V>` as the initial collection families.
      ([tests](conformance/foundations.json))

- [x] **D02** Use separate immutable and mutable container families: List<T>, Set<T>, and Map<K, V> cannot have their
      contents changed through any alias; MutableList<T>, MutableSet<T>, and MutableMap<K, V> permit container changes.
      Element values retain their own mutability rules. ([tests](conformance/foundations.json))

- [x] **D03** Support collection literals: `[a, b]` for lists, `{a, b}` for sets, and `{key: value}` for maps.
      Contextual typing and inference follow D10-D11; empty literals follow D17. Factory APIs remain separate.
      ([tests](conformance/foundations.json))

- [x] **D04** When no expected type supplies context, collection construction infers the immutable List/Set/Map family
      by default. Mutable construction uses the explicit prefix in D09 or expected-type guidance in D10.
      ([tests](conformance/foundations.json))

- [x] **D05** Same-family assignment and argument passing of mutable collection values share the same container, so
      mutations are visible through aliases. Cross-family copying follows D21. These rules concern container contents
      rather than `val`/`var` binding reassignment. ([tests](conformance/foundations.json))

- [x] **D06** List indexing uses zero-based, nonnegative indexes, matching String indexing. Provably invalid constant
      indexes are compile errors; other invalid indexes are runtime errors. Negative indexes are invalid.
      ([tests](conformance/foundations.json))

- [x] **D07** Map lookup with `map[key]` returns `V?`. A missing key yields null, and a stored null also yields null.
      Map key presence is tested with `in` or `!in` under D19. ([tests](conformance/foundations.json))

- [x] **D08** Equality and inequality for compatible collection values are structural. Lists compare elements in order;
      sets compare members and maps compare entries independent of iteration order. Element, key, and value equality
      must be supported. Compatible argument joins determine ordinary comparison; cyclic comparison follows E34.
      ([evidence](equality-and-nullability.md))

- [x] **D09** Explicit mutable collection construction uses the mutable literal prefix, for example mutable [1, 2],
      mutable {"a", "b"}, and mutable {"gold": 3}. ([tests](conformance/foundations.json))

- [x] **D10** Expected types guide collection literal element/key/value types and mutability. An annotation or parameter
      type may request mutable construction without a mutable prefix, for example val items: MutableList<Int> = [1, 2].
      The no-context default remains immutable under D04. ([tests](conformance/foundations.json))

- [x] **D11** Collection literals infer compatible-type joins using existing scalar widening: `[1, 2.5]` yields
      `List<Float>`, and `['a', "b"]` yields `List<String>`. Mixing `T` with null yields `T?`. Unrelated types require a
      suitable explicit expected type or are errors. Empty or all-null collections require an expected type; empty
      set/map forms follow D17. ([tests](conformance/foundations.json))

- [x] **D12** Set elements and map keys must have statically stable equality that cannot change while stored. Accept
      known-stable types; immutable containers qualify only when their contained values also qualify. Reject mutable
      composites. Exact eligibility analysis and hashing machinery remain open.
      ([evidence](conformance/cases/projected-capability-compositions-source-free-checkpoint/main.bfl))

- [x] **D13** Sets and maps preserve first-insertion order for iteration. Replacing a map value retains its key's
      position; removing and reinserting moves it to the end. Lists retain positional order.
      ([tests](conformance/foundations.json))

- [x] **D14** Set construction coalesces equal duplicate members. Map construction rejects duplicate keys: compile
      errors when provable and runtime errors otherwise. Literal evaluation and dynamic key-check timing follow D29.
      ([tests](conformance/foundations.json))

- [x] **D15** For loops over lists and sets yield elements; loops over maps yield entry values with .key and .value. The
      existing fresh immutable iteration-binding rule applies. Entry<K,V> has fixed key/value snapshot fields; general
      tuple unpacking is not selected. ([tests](conformance/foundations.json))

- [x] **D16** For loops snapshot elements or map entries when traversal starts, including traversal of mutable
      collections. Mutating the original container does not change that traversal. Referenced element values retain
      their own semantics; the snapshot is not a recursive freeze or deep copy. ([tests](conformance/foundations.json))

- [x] **D17** Empty literals use context: `[]` is a list; `{}` is a set or map according to its expected type. Empty
      collections require sufficient expected element/key/value types; insufficient context is a compile error.
      ([tests](conformance/foundations.json))

- [x] **D18** Use the `size` property for collection element or entry counts, with an `Int` result. `String` retains its
      `length` property. ([tests](conformance/foundations.json))

- [x] **D19** Use `in` and `!in` for collection membership. Lists and sets test elements; maps test keys, including keys
      whose stored value is null. `!in` negates the test. ([tests](conformance/foundations.json))

- [x] **D20** Mutable collections support indexed assignment plus methods: `items[i] = value` replaces a list element,
      and `mapping[key] = value` inserts or replaces a map entry. Add/remove operations use methods with the selected
      signatures and results.
      ([evidence](collection-operations.md))

- [x] **D21** Assignments and arguments may implicitly convert between corresponding immutable and mutable collection
      families by copying container contents into the requested family. The resulting container is independent;
      referenced element values retain their own semantics rather than being recursively frozen or copied.
      ([tests](conformance/foundations.json))

- [x] **D22** Lift approved lossless scalar widening through immutable `List`/`Set`/`Map` element, key, or value types,
      converting contents as needed. Also allow implicit nominal Map-key subtype conversion by rebuilding the map and
      checking duplicate keys. Map keys remain invariant for subtyping under D30. Same-family mutable collection type
      arguments must match exactly; family copying and recursive immutable lifting follow D25/D28.
      ([tests](conformance/foundations.json))
      ([evidence](clarification-conformance.md#nominal-map-keys))

- [x] **D23** A variadic parameter exposes a fresh immutable `List<T>` of its declared element type on each call, for
      example `vararg values: Int` yields `List<Int>`. Referenced elements retain their own semantics.
      ([tests](conformance/foundations.json))

- [x] **D24** Use the star prefix to spread `List<T>` or `MutableList<T>` elements into typed variadic arguments, for
      example `total(1, *numbers)`. Multiple groups and source-position expansion follow A07; other iterable families
      remain separate. ([tests](conformance/foundations.json))

- [x] **D25** A container-family copy may combine with approved scalar widening: `MutableList<Int>` to `List<Float>` and
      `List<Int>` to `MutableList<Float>` produce independent containers. Same-family `MutableList<Int>` to
      `MutableList<Float>` remains forbidden; implicit copy chains must not bypass that invariance.
      ([tests](conformance/foundations.json))

- [x] **D26** Argument conversion and snapshot timing follow A04. An earlier requested snapshot completes before a later
      argument expression can mutate its source. ([tests](conformance/foundations.json))

- [x] **D27** Rank overload argument conversions as exact, widening, container-family copying, then copying plus
      widening. These are semantic categories, not allocation counts. Candidate dominance and tie-breakers follow
      F28-F29. ([tests](conformance/foundations.json))

- [x] **D28** Approved widening recurses through nested immutable containers, for example `List<List<Int>>` to
      `List<List<Float>>`. Stop at mutable contained types, whose type arguments require exact matching. This does not
      authorize recursively copying or freezing mutable element objects. ([tests](conformance/foundations.json))

- [x] **D29** Collection literals evaluate elements or entries from left to right. For each map entry, evaluate its key,
      reject a dynamically duplicated key before evaluating its value, then proceed to the next entry. Provable
      duplicate map keys remain compile errors. ([tests](conformance/foundations.json))

- [x] **D30** Immutable List and Set element types and Map value types are covariant through genuine subtype
      relationships, without copying; Map keys remain invariant. For example, List<Outcome.Success> may satisfy
      List<Outcome>. Scalar conversions remain separate, and mutable collection type arguments remain invariant.
      ([tests](conformance/foundations.json))

### Integer ranges and membership

- [x] **R01** `a..b` is an ascending inclusive integer range. ([tests](conformance/foundations.json))

- [x] **R02** `a..<b` is an ascending half-open integer range: include `a`, exclude `b`.
      ([tests](conformance/foundations.json))

- [x] **R03** Ranges are immutable first-class values. They can be stored in bindings, passed to functions, and reused
      in membership tests. A `var` may be rebound to another range value. ([tests](conformance/foundations.json))

- [x] **R04** Invalid or empty ascending ranges are errors. Reject constant cases at compile time and dynamically
      computed cases at runtime. Examples include `5..1` and `5..<5`. ([tests](conformance/foundations.json))

- [x] **R05** `a downTo b` explicitly creates an inclusive descending range. The ascending forms retain their direction.
      ([tests](conformance/foundations.json))

- [x] **R06** `step n` selects every nth value. The step must be a positive `Int`; direction comes from the range form.
      ([tests](conformance/foundations.json))

- [x] **R07** Use Kotlin's implementation as the reference for stepped integer progression membership. Membership
      follows the values produced by the progression.
      ([evidence](progression-membership.md))

### Loops and jumps

- [x] **C01** `for i in range:` creates a fresh, inferred immutable binding each iteration, scoped to the loop body.
      ([tests](conformance/foundations.json))

- [x] **C02** `break` exits the innermost loop; `continue` skips to its next iteration.
      ([tests](conformance/foundations.json))

- [x] **C03** Loops may have optional labels. A targeted jump must name an enclosing loop in the same function; invalid
      targets are compile errors. ([tests](conformance/foundations.json))

- [x] **C04** Label a loop using `outer@ for ...:`; target it with `break@outer` or `continue@outer`.
      ([tests](conformance/foundations.json))

- [x] **C05** Support both `while` and `do/while`. A `while` tests before the body; a `do/while` tests after it and runs
      the body at least once. ([tests](conformance/foundations.json))

- [x] **C06** Write `do:` with an indented body, followed by `while condition` aligned with `do`. The closing `while`
      has no colon. ([tests](conformance/foundations.json))

- [x] **C07** Declarations directly in a `do` body are visible to its closing condition, but unavailable after the loop.
      Declarations inside nested blocks retain those narrower scopes. ([tests](conformance/foundations.json))

- [x] **C08** Every variable read by the closing condition must be initialized on every path reaching it, including
      paths through `continue`. ([tests](conformance/foundations.json))

### Functions, parameters, and calls

- [x] **F01** Declare functions using `fun` exclusively. ([tests](conformance/overloads.json))

- [x] **F02** Parameters require type annotations. Infer return types when unambiguous; require annotations when
      inference cannot resolve them.
      ([evidence](function-contracts.md))

- [x] **F03** Explicit return annotations use `->`: `fun double(value: Int) -> Int:`. The final colon opens a block
      body. ([tests](conformance/overloads.json))

- [x] **F04** Named function block bodies use explicit return value. Value-returning named functions must return on
      every reachable path. Anonymous function bodies follow F27. ([tests](conformance/overloads.json))

- [x] **F05** Support expression bodies: `fun double(value: Int) = value * 2`. The expression supplies the returned
      value; return annotations may still use `->`. ([tests](conformance/overloads.json))

- [x] **F06** `Unit` is a regular type with one value. Infer it for functions that return no value. Such functions may
      end naturally or use bare `return`. An explicit annotation is `-> Unit`. ([tests](conformance/overloads.json))

- [x] **F07** Parameters are immutable by default. An optional `var` modifier permits reassignment of a parameter
      binding inside the function. ([tests](conformance/overloads.json))

- [x] **F08** Each parameter has its own local binding. Reassigning a `var` parameter does not update the caller's
      binding. Ordinary argument expressions are allowed. ([tests](conformance/overloads.json))

- [x] **F09** Parameters may declare default argument values using `=`, while retaining required type annotations. Calls
      omitting an argument use its default. ([tests](conformance/overloads.json))

- [x] **F10** For parameters permitted to have defaults, evaluate an omitted default at each call only when that
      argument is omitted. Variadic parameters follow F33 instead. ([tests](conformance/overloads.json))

- [x] **F11** Defaults may reference already-resolved earlier parameters and bindings visible where the function is
      declared. Later parameters are unavailable. ([tests](conformance/overloads.json))

- [x] **F12** Defaulted parameters may appear anywhere, including before required ones. Positionals bind in declaration
      order; named arguments can omit earlier defaults. ([tests](conformance/overloads.json))

- [x] **F13** Support self-recursion and mutual recursion, with fresh parameter and local bindings for every call.
      Return typing follows F02. ([tests](conformance/overloads.json))

- [x] **F14** Function names are visible throughout their enclosing scope. Calls may precede declarations in that scope,
      so declaration order does not restrict ordinary calls or mutual recursion. ([tests](conformance/overloads.json))

- [x] **F15** Allow fun declarations at file scope and inside functions or ordinary code blocks. Local function names
      follow the scope of their enclosing block and the scope-wide visibility rule in F14.
      ([tests](conformance/overloads.json))

- [x] **F16** Local function bodies may read bindings from enclosing lexical scopes that are visible where the function
      is declared. Reads of enclosing var bindings follow F17, and reassignment follows F18.
      ([tests](conformance/overloads.json))

- [x] **F17** Each read of an enclosing var observes that lexical binding's current value at the time of the read,
      including reassignments since the local function was declared. ([tests](conformance/overloads.json))

- [x] **F18** Local functions may reassign visible enclosing var bindings. Assignment updates that same enclosing
      binding, subject to its type and ordinary assignment rules. ([tests](conformance/overloads.json))

- [x] **F19** A local function may be declared before an enclosing binding it reads has been initialized. Every call
      that could read the binding requires compile-time proof of initialization; unprovable cases are compile errors.
      ([evidence](binding-flow-semantics.md#captured-reads-call-profiles-and-recursion))

- [x] **F20** Functions are first-class, statically typed values. They may be stored in variables, passed as arguments,
      and returned, including references to local functions. ([tests](conformance/overloads.json))

- [x] **F21** Escaping functions retain their captured lexical bindings as long as needed. Functions capturing the same
      var binding share its current state; separate enclosing invocations still have their own bindings.
      ([evidence](../bifoil-runtime/test/compact-captures.test.mjs))

- [x] **F22** Function types use arrow notation, such as (Int, Int) -> Int, with an explicit return type. Unit-returning
      function types spell (Int) -> Unit or () -> Unit. Omission of -> Unit applies to function declarations.
      ([tests](conformance/overloads.json))

- [x] **F23** Functions in the same scope may form overload sets distinguished by parameter types or counts. Ambiguous
      calls are compile errors, and return types alone cannot distinguish overloads. Nested shadowing remains
      prohibited.
      ([evidence](function-contracts.md))

- [x] **F24** Support typed variadic parameters accepting zero or more arguments of one declared element type. Spelling
      follows F30 and placement follows F31; the fresh immutable `List<T>` representation follows D23.
      ([tests](conformance/overloads.json))

- [x] **F25** Support anonymous function expressions without a declared name, with mandatory parameter annotations.
      Arrow syntax follows F26/F40, final-expression returns follow F27/F34, and variadic parameters follow F41.
      ([tests](conformance/overloads.json))

- [x] **F26** Anonymous functions use `(x: Int) => x + 1`, or `(x: Int) =>:` with an indented block. Optional return
      annotations follow F40. ([tests](conformance/overloads.json))

- [x] **F27** Anonymous expression bodies and block bodies return their final expression, with contextual Unit-result
      discarding under F34. An early return exits the anonymous function itself. Named function block bodies retain
      F04's explicit-return rule. ([tests](conformance/overloads.json))

- [x] **F28** Overload resolution compares each supplied argument's conversion rank under D27. A candidate wins on
      argument types only if it is no worse on every supplied argument and better on at least one. The selected scalar
      widenings and collection conversions participate in these ranks. ([tests](conformance/overloads.json))

- [x] **F29** For overloads otherwise equally good on supplied arguments, prefer nonvariadic candidates, then candidates
      requiring fewer omitted defaults. Remaining generic/nongeneric ties follow F42; other ties are compile errors.
      ([tests](conformance/overloads.json))

- [x] **F30** Declare a typed variadic parameter with the vararg modifier, such as vararg values: Int. The annotation
      denotes the element type. ([tests](conformance/overloads.json))

- [x] **F31** Allow at most one variadic parameter per function signature, always as the last parameter.
      ([tests](conformance/overloads.json))

- [x] **F32** Retain variadic function-value types, such as `(vararg Int) -> Unit`, with zero-or-more individual or
      spread arguments. Other function-value call rules follow A05. ([tests](conformance/overloads.json))

- [x] **F33** Variadic parameters have no explicit default expressions; omission supplies an empty group under D23. Use
      an ordinary `List` parameter for a custom default. ([tests](conformance/overloads.json))

- [x] **F34** When constructing an anonymous function with an expected return type of `Unit`, evaluate and discard
      non-Unit values from both its final expression and value-bearing early return statements, then return `Unit`. An
      early return still exits that anonymous function. Ordinary named functions retain their existing return rules.
      This is contextual anonymous-function construction, not a conversion of existing function values.
      ([tests](conformance/overloads.json))
      ([evidence](clarification-conformance.md#anonymous-unit-returns))

- [x] **F35** Take a named function reference with `::`, for example `val transform = ::double`. Its calling interface
      follows A05/F32. ([tests](conformance/overloads.json))

- [x] **F36** Resolve an overloaded function reference using an expected function type from an annotation or parameter
      context. Select a unique compatible overload; unresolved or ambiguous references are compile errors.
      ([evidence](conformance/cases/unresolved-overload-reference-matrix-error/main.bfl))

- [x] **F37** For function types with the same parameter count and variadic shape, allow safe variance through subtype
      relationships: broader parameter types and narrower return types may satisfy the expected type. For example,
      `(Int?) -> String` may satisfy `(Int) -> String?`. Numeric widening and container copying are separate
      conversions; T21's ordinary-to-suspend widening remains available.
      ([evidence](conformance/cases/type-interactions-source-free-checkpoint/main.bfl))

- [x] **F38** Do not automatically create function adapters when signature compatibility would require scalar value
      conversions or container copies. Write an anonymous function to perform those conversions explicitly. Ordinary
      argument conversions when calling a function remain available. ([tests](conformance/overloads.json))

- [x] **F39** Function values do not support `==` or `!=` comparisons except nullable comparisons with `null`; other
      such comparisons are compile errors. Eligibility for the newly requested exact-equality operators remains subject
      to E28. ([tests](conformance/overloads.json))

- [x] **F40** Anonymous functions may declare an explicit return type with `->` between their parameters and `=>`: `(x:
      Int) -> Float => x * 2`, or `(x: Int) -> Float =>:` followed by an indented block. Parameter annotations remain
      mandatory. ([tests](conformance/overloads.json))

- [x] **F41** Anonymous functions may declare a variadic parameter, such as `(vararg values: Int) => values.size`, and
      infer a variadic function type. Existing last-parameter, fresh immutable `List<T>`, and variadic function-value
      call rules apply. ([tests](conformance/overloads.json))

- [x] **F42** After the existing conversion, variadic, and default-argument tie-breakers, prefer a nongeneric overload
      over an otherwise tied generic overload. Other unresolved ties are compile errors.
      ([tests](conformance/overloads.json))

- [x] **F43** Take a bound instance-method reference with receiver::method, for example val heal = character::heal. Its
      resulting function value already has the receiver bound and follows the existing function-value calling interface.
      ([tests](conformance/overloads.json))

- [x] **F44** Evaluate and capture a method-reference receiver once when the reference is created. Later reassignment of
      the original receiver binding does not retarget that reference. Anonymous functions reading captured bindings
      retain F17. ([tests](conformance/overloads.json))

- [x] **A01** Calls support both positional arguments and named arguments written `name = value`.
      ([tests](conformance/overloads.json))

- [x] **A02** Unknown parameter names and duplicate argument bindings are compile errors. Arguments retain static type
      checking. ([tests](conformance/overloads.json))

- [x] **A03** In mixed calls, positional arguments precede named arguments. Named arguments may appear in any order.
      ([tests](conformance/overloads.json))

- [x] **A04** Evaluate supplied arguments left to right, completing each implicit conversion before evaluating the next
      argument. Then evaluate omitted defaults in parameter declaration order. ([tests](conformance/overloads.json))

- [x] **A05** Calls through function values require explicit positional arguments for fixed parameters and expose no
      parameter names or defaults. Variadic function types retain F32's zero-or-more argument interface. Declared
      function-name calls retain their named/default interfaces. ([tests](conformance/overloads.json))

- [x] **A06** Evaluate and capture a call's callable expression or method receiver before supplied arguments. Then
      process arguments and omitted defaults under A04 and D26. ([tests](conformance/overloads.json))

- [x] **A07** Allow multiple spread groups interleaved with individual variadic arguments, for example `gather(1,
      *first, 2, *second)`. Expand groups at their source position under the selected argument order; spreads supply the
      variadic portion and preserve that element order. ([tests](conformance/overloads.json))

- [x] **A08** A declared function name accepts a named variadic group as a list value, for example `gather(values =
      numbers)`, with applicable copying/widening rules and a fresh immutable `List<T>` for the callee. The same
      variadic parameter cannot be supplied both positionally and by name. ([tests](conformance/overloads.json))

### Narrative and story control

- [x] **T01** Introduce explicit unquoted narrative blocks with prose: followed by indented narrative.
      ([tests](conformance/expressions.json))

- [x] **T02** Prose interpolation uses ${expression}, such as Your score is ${score}. Literal-delimiter escaping follows
      T11. ([tests](conformance/expressions.json))

- [x] **T03** Prose interpolation permits non-suspending value expressions, including arithmetic and ordinary function
      calls, that produce a renderable value. Directly renderable types follow P08; exact formatting remains open.
      ([evidence](conformance/cases/interpolation-blocks-source-free-checkpoint/main.bfl))

- [x] **T04** After removing structural block indentation, single source newlines join text within a paragraph and blank
      lines separate paragraphs. Support explicit line breaks within paragraphs.
      ([evidence](prose-semantics.md))

- [x] **T05** Support executable directives inside prose. Their prefix and nested-body rules follow T09-T10.
      ([tests](conformance/expressions.json))

- [x] **T06** A choice uses an outer choice: block containing explicit option headers, such as option "Open the door":,
      each followed by its indented body. ([tests](conformance/expressions.json))

- [x] **T07** After the selected option body finishes normally, execution continues after the choice. Existing return,
      break, and other control transfers still apply. ([tests](conformance/expressions.json))

- [x] **T08** Functions that may wait for player interaction carry an explicit suspension effect in their types; calls
      require a suspension-capable context. ([tests](conformance/expressions.json))

- [x] **T09** A line-leading @ after indentation introduces an executable directive inside prose. The text after the
      prefix uses Bifoil syntax, such as @if hasKey: or @score = score + 1. ([tests](conformance/expressions.json))

- [x] **T10** Conditional and loop directive bodies remain in prose mode by default. Further executable statements and
      branch headers use the @ prefix. ([tests](conformance/expressions.json))

- [x] **T11** Prose uses backslash escapes: `\${` produces literal `${`, `\@` makes a directive introducer literal, and
      `\\` produces one backslash. Other escape forms remain open. ([tests](conformance/expressions.json))

- [x] **T12** Quoted option labels support ${expression} interpolation under the same non-suspending, renderable-value
      rules as prose. ([tests](conformance/expressions.json))

- [x] **T13** Conditional option headers may use if for visibility and enabledIf for selection availability, as in
      option "Open" if visible enabledIf allowed:. False if hides the option; false enabledIf displays it disabled.
      Conditions require booleans. ([tests](conformance/expressions.json))

- [x] **T14** Prepare each choice once, processing options in source order. Filter a consumed once option before
      evaluating its visibility, enabling, or label expressions. For an unconsumed option, evaluate visibility first,
      then the enabled condition and label when visible. Hidden options skip enabled-condition and label evaluation.
      Retain these results until selection.
      ([evidence](clarification-conformance.md#choice-preparation))

- [x] **T15** The suspend modifier marks suspension-capable named functions, anonymous functions, and function types:
      suspend fun ask() -> Int:, suspend () -> Int, and a suspend-prefixed lambda.
      ([tests](conformance/expressions.json))

- [x] **T16** Call suspending functions with ordinary syntax, such as `val answer = ask()`, in a context permitted by
      T08. No `await` marker is required. ([tests](conformance/expressions.json))

- [x] **T17** A choice may contain an else: fallback for when no option is selectable. Without a fallback, provably
      empty choices are compile errors and dynamically empty choices are runtime errors.
      ([tests](conformance/expressions.json))

- [x] **T18** Options are reusable by default. An option with the once modifier, such as option "Ask about the map"
      once:, is consumed on selection and hidden on subsequent visits. ([tests](conformance/expressions.json))

- [x] **T19** Once-option history is story-wide per source option site for the playthrough. Later scene visits and
      function calls share that site's consumed state. ([tests](conformance/expressions.json))

- [x] **T20** New Bifoil scene bodies are automatically allowed to suspend: they may present choices and call suspend
      functions directly. Ordinary function bodies still require the suspend modifier.
      ([tests](conformance/expressions.json))

- [x] **T21** An ordinary function value may satisfy a suspend function type with otherwise identical parameter and
      return types. A suspend function value cannot satisfy an ordinary function type.
      ([tests](conformance/expressions.json))

- [x] **T22** Suspending calls may appear inside larger expressions and function arguments. Preserve the selected
      evaluation order and retain completed operands, arguments, and partial evaluation across suspension without
      repeating completed work. Prose and option-label interpolation remain non-suspending.
      ([tests](conformance/expressions.json))

- [x] **T23** Choice-preparation expressions for visibility, enabling, and label interpolation must not suspend.
      Ordinary state changes and other non-suspending effects are permitted under the selected preparation order.
      ([tests](conformance/expressions.json))

- [x] **T24** At supported save points, retain full suspended state: active calls, locals, captures, computed
      temporaries, active traversal state, choice snapshots, and option history. Resume without replay. Initial
      checkpoint and build-compatibility policies follow T25-T26; save-format details remain open.
      ([tests](conformance/expressions.json))

- [x] **T25** Initially support saving at fully prepared player-input waits. Every supported save point preserves the
      full suspended-state, no-replay contract under T24. ([tests](conformance/expressions.json))

- [x] **T26** Initial saves restore only against the same compiled build. Reject incompatible saves clearly.
      Compatibility across game updates and migrations are outside the initial save contract.
      ([tests](conformance/expressions.json))

### Scenes, modules, and shared state

- [x] **M01** Organize new source into scene files and library modules. A scene file has one executable story body plus
      declarations. Ordinary file/module-level val/var values require shared; library initialization happens through
      non-suspending shared initializers. Scene-body bindings retain their per-visit behavior under M06.
      ([evidence](clarification-conformance.md#generated-members-and-module-values))

- [x] **M02** Scene destinations are typed first-class references that can be stored, passed, and selected with checked
      input signatures. Ordinary strings are not scene destinations. ([tests](conformance/shared.json))

- [x] **M03** Scene entries may declare typed input parameters local to that visit. Scene entry and calls reuse the
      existing argument and default-argument rules. ([tests](conformance/shared.json))

- [x] **M04** Support returning scene calls and one-way scene transfers. A call runs a fresh visit and returns control
      with Unit; a transfer replaces the current story position. Value-returning routines use suspend functions.
      Operation syntax and transfer unwinding follow M12-M13. ([tests](conformance/shared.json))

- [x] **M05** A scene body may finish naturally. Return to its scene caller if one exists; otherwise finish the story.
      ([tests](conformance/shared.json))

- [x] **M06** Ordinary scene-body `val`/`var` declarations are local to that visit. Persistent shared storage follows
      M14. ([tests](conformance/shared.json))

- [x] **M07** Initialize shared story state once before the first scene of a new playthrough, using non-suspending
      initializers. Loading restores saved state without replaying initializers. Dependency ordering and cycle policy
      follow M15. ([tests](conformance/shared.json))

- [x] **M08** Top-level symbols are private by default. Export intended interfaces and explicitly import the symbols a
      file uses. Import/export spelling follows M16; explicit module interfaces determine visibility.
      ([evidence](modules-and-names.md))

- [x] **M09** A scene file declares its entry with a named header such as scene forest(danger: Int = 0): and an indented
      body. The header supplies the logical scene name; helpers and shared declarations remain outside that body.
      ([tests](conformance/shared.json))

- [x] **M10** Scene references use input types: `Scene<Int, Float>`, or bare `Scene` for zero inputs. Reference-valued
      targets require every input explicitly and positionally; named targets retain named/default arguments.
      ([tests](conformance/shared.json))

- [x] **M11** Obtain a named scene reference with the explicit `::` prefix, for example `val destination = ::forest`.
      Named function references use the same prefix under F35. ([tests](conformance/shared.json))

- [x] **M12** Use `goto` for a transfer and `visit` for a returning scene call, such as `goto forest(danger = 3)` or
      `visit forest(danger = 3)`. Input and return rules follow M03-M04/M10. ([tests](conformance/shared.json))

- [x] **M13** Transfers are permitted only in scene bodies or suspend functions. A transfer replaces the current scene
      visit and abandons its active function calls, while retaining earlier scene-call callers. If A visits B and B
      transfers to C, C's natural completion returns to A. ([tests](conformance/shared.json))

- [x] **M14** At file/module scope, declare persistent story values with shared val or shared var, for example shared
      var gold: Int = 0. Allowing shared declarations inside functions or scene bodies requires a separate placement
      decision. ([tests](conformance/shared.json))

- [x] **M15** Shared names resolve throughout their module, including forward references. Initialize dependencies first,
      use stable module/source order for independent values, and reject cycles requiring uninitialized values.
      Local-variable visibility retains B10. ([tests](conformance/shared.json))

- [x] **M16** Use dotted explicit imports with optional `as` aliases, such as `import story.stats.gold as coins`; prefix
      exported declarations with `export`. ([tests](conformance/shared.json))

- [x] **M17** Place new Bifoil sources under src/ and derive dotted module names from directory and file paths. Existing
      explicit import and export rules remain in force. ([tests](conformance/shared.json))

- [x] **M18** Use bifoil.toml as the project manifest and name the entry scene there. Specify and validate its exact
      keys and schema.
      ([evidence](../bifoil-compiler/README.md#compile-a-project))

- [x] **M19** Use .bfl as the source-file extension and account for its documented file-association conflicts.
      ([tests](conformance/shared.json))

## Engineering and acceptance ([specification](language-specification-draft.md))

### Contract closure and formal specification

- [ ] **CON-01** Publish a coherent language-version/profile contract and a complete lexer, grammar, and static
      semantics.

- [x] **CON-02** Reconcile stale provisional prose with dated user clarifications without deleting decision history.
      ([evidence](specification-contracts.md))

- [x] **CON-03** Specify identifiers, reserved/contextual keywords, comments, literal forms, and source text encoding.
      ([evidence](development-source-grammar.md#notation-and-lexical-input))

- [x] **CON-04** Publish one complete precedence/associativity table, including fairmath grouping, ranges, casts, and
      Elvis.
      ([evidence](development-source-grammar.md#expressions-and-precedence))

- [x] **CON-05** Resolve chained-comparison syntax explicitly; do not infer Python behavior from syntax inspiration.
      ([evidence](text-semantics.md))

- [x] **CON-06** Specify triple-string dedent, tabs, delimiter lines, blank lines, newlines, and interpolation timing.
      ([evidence](text-semantics.md))

- [x] **CON-07** Specify primitive rendering, numeric/text conversion APIs, negative zero, and malformed external text.
      ([evidence](text-semantics.md))

- [x] **CON-08** Resolve exact equality across covariant views and preserved generic identities, including empty
      containers.
      ([evidence](accepted-clarifications.md#exact-equality-and-comparison-views))

- [x] **CON-09** Resolve nominal Map-key conversion behavior without silently broadening the selected scalar-copy rules.
      ([evidence](accepted-clarifications.md#nominal-map-key-conversion))

- [x] **CON-10** Define capability derivation, recursive constraints, subtype relations, joins, and inference
      termination.
      ([evidence](type-constraints.md))

- [x] **CON-11** Resolve namespace/member lookup, no-shadowing, alias conflicts, and generated member/copy-name
      collisions.
      ([evidence](modules-and-names.md))

- [x] **CON-12** Specify collection operation signatures/results, entry types, contextual literals, and bounds-check
      timing.
      ([evidence](collection-operations.md))

- [x] **CON-13** Resolve the pinned Kotlin progression reference, terminal overflow, membership cost, and failure
      behavior.
      ([evidence](progression-membership.md))

- [x] **CON-14** Resolve once-history filtering relative to effectful visibility, enabling, and label preparation.
      ([evidence](accepted-clarifications.md#consumed-once-options))

- [x] **CON-15** Complete embedded-directive grammar, including functions, continued expressions, and prose/code
      boundaries.
      ([evidence](prose-semantics.md))

- [x] **CON-16** Specify shared-storage placement, library ordinary bindings/initialization, re-exports, and modifier
      order.
      ([evidence](modules-and-names.md))

- [ ] **CON-17** Specify composite legacy bridge representation, copying/sharing, aliasing, cycles, mutation, and
      ownership.

- [x] **CON-18** Complete runtime-profile, module-producer, artifact, package, and checkpoint compatibility/rejection
      rules.
      ([evidence](compatibility-contract.md))

- [ ] **CON-19** Select the full-job resource metric, process scope, accounting/enforcement method, and reference
      environment.

- [x] **CON-20** Specify guarded-pattern coverage, Unit-context early returns, and combined overload/conversion
      inference.
      ([evidence](function-contracts.md))

- [x] **CON-21** Formalize conservative definite assignment, effect invalidation, escaping captures, and recursive
      calls.
      ([evidence](binding-flow-semantics.md))

- [x] **CON-22** Review Turing completeness at the language-semantics level separately from finite implementation
      guards.
      ([evidence](computability.md))

- [ ] **CON-23** Give every unresolved observable contract a distinguishing example and a documented resolution/status.

- [ ] **CON-24** Complete whole-design review without treating working implementation choices as approved language
      rules.

### Lexing, layout, parsing, and formatting

- [x] **LEX-01** Implement all selected tokens and longest-match boundaries, including overlapping operators and
      delimiters. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-02** Distinguish identifiers from keyword prefixes, member names, generic arguments, and keyword operators.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-03** Parse every approved numeric literal form, minimum Int, range dots, exponent, and separator boundary.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-04** Parse ordinary/triple strings, Char literals, every Unicode escape form, and invalid scalar rejection.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-05** Balance recursive interpolation, nested quoted text, braces, and comments without consuming following
      code. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-06** Count tabs and complete four-space groups structurally; retain leftover alignment and mixed whitespace.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-07** Handle blank/comment-only lines, indentation jumps, dedents, end-of-file, and source newline encodings.
      ([evidence](../bifoil-compiler/src/parser/grammar_contracts.rs))

- [x] **LEX-08** Preserve block-expression structure inside parenthesized and trailing-operator continuations.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-09** Parse every declaration, modifier, import, generic bound, type, reference, and scene header production.
      ([evidence](modules-and-names.md))

- [x] **LEX-10** Parse statements, expressions, assignments, labels, loop transfers, patterns, guards, and fallbacks.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-11** Distinguish anonymous arrow bodies, function types, return annotations, and expression-body
      declarations. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-12** Parse all nullable access/call/index forms and distinguish nullable header endings from Elvis
      continuation. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-13** Preserve the explicit fairmath grouping rule while ordinary arithmetic retains conventional precedence.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-14** Parse prose directives and nested prose without reclassifying literal branch-looking text as executable
      code. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-15** Parse choice labels, visibility/enabling/once modifiers, bodies, and fallback combinations coherently.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-16** Share import discovery with real lexical/parser rules; ignore import-looking strings and prose.
      ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-17** Retain physical source locations through multiline strings, interpolations, headers, and embedded
      directives. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-18** Reject malformed or unsupported syntax with bounded, original-source diagnostics and no successful
      output. ([tests](../bifoil-compiler/src/tests/syntax.rs))

- [x] **LEX-19** Keep AST nodes explicit and maintainable for all grammar forms; preserve source identity through
      lowering.
      ([evidence](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **LEX-20** Format structural indentation while preserving alignment, comments, newline style, prose, and literal
      bytes. ([tests](../bifoil-compiler/tests/cli/source_format.rs))

- [x] **LEX-21** Preserve authored elif/else-if spelling; never introduce def or superseded return-annotation syntax.
      ([tests](../bifoil-compiler/tests/cli/source_format.rs))

- [x] **LEX-22** Verify formatter idempotence, format-check failure status, atomic output, and semantic equivalence.
      ([tests](../bifoil-compiler/tests/cli/source_format.rs))

- [x] **LEX-23** Detect Bifoil through manifests or explicit selection where file handling is provided; respect .bfl
      collisions.
      ([evidence](file-selection.md))

### Names, scopes, modules, imports, and visibility

- [x] **NAM-01** Implement case-sensitive names/keywords without importing legacy ChoiceScript case rules into Bifoil.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-02** Enforce lexical block scope, variable declaration-order visibility, and scope-wide function visibility.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-03** Resolve forward local/type-alias declarations without making future local variable names visible.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-04** Reject nested shadowing consistently for parameters, implicit bindings, captures, patterns, and labels.
      ([evidence](conformance/foundations.json))

- [x] **NAM-05** Keep legitimate same-scope overload sets distinct from duplicate declarations or prohibited shadowing.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-06** Resolve implicit this, bare members, private access, and nested methods/functions by declaration
      identity.
      ([evidence](../bifoil-compiler/src/tests/private_members.rs))

- [x] **NAM-07** Reject enum-shorthand conflicts with ordinary bindings; support qualified and expected-type references.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-08** Resolve transparent aliases across files and lexical blocks while rejecting alias-expansion cycles.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-09** Preserve nominal identities through aliases, variants, generics, source-free modules, and
      case-sensitive names. ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-10** Implement path-derived dotted modules under src and explicit import/export/alias visibility.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-11** Check the selected manifest schema, entry scene, module/legacy paths, duplicate keys, and unknown
      options. ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-12** Resolve module/name conflicts, private-by-default top-level symbols, and selected re-export rules.
      ([evidence](modules-and-names.md))

- [x] **NAM-13** Handle cyclic imports with checked interfaces, anchored inference, reproducible artifacts, and cycle
      diagnostics. ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-14** Detect cross-kind callable/shared/legacy-storage identity collisions before publishing a linked root.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-15** Preserve language names resembling host object properties without prototype-dependent lookup behavior.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

- [x] **NAM-16** Test namespace and visibility rules with independent compilation and removed dependency source.
      ([tests](../bifoil-compiler/src/tests/modules.rs))

### Types, nullability, generics, and capabilities

- [x] **TYP-01** Represent all primitive, universal, nullable, bottom, nominal, variant, collection, callable, and scene
      types. ([tests](conformance/generics.json))

- [x] **TYP-02** Keep static subtyping distinct from numeric widening, Char widening, family copies, and explicit
      adapters. ([tests](conformance/generics.json))

- [x] **TYP-03** Implement inference and expected-type checking without an arbitrary Any fallback or inferred family
      copies.
      ([evidence](../bifoil-compiler/src/types/joins.rs))

- [x] **TYP-04** Require expected types for bare null and empty/all-null collections; flatten inferred nullability
      correctly. ([tests](conformance/generics.json))

- [x] **TYP-05** Reject repeated nullable markers and invalid/undefined types in used and unused declarations.
      ([tests](conformance/generics.json))

- [x] **TYP-06** Implement Any/Any? operations and static equality eligibility without trusting unknown concrete
      capabilities. ([tests](conformance/generics.json))

- [x] **TYP-07** Implement reified type tests/casts for empty and populated generic values; never convert or copy in a
      cast. ([tests](conformance/generics.json))

- [x] **TYP-08** Reject provably impossible concrete casts; retain checked failure/null outcomes for dynamic mismatches.
      ([tests](conformance/generics.json))

- [x] **TYP-09** Implement nullable lifting, lazy access/calls/indexing, assertion unwrapping, and compatible Elvis
      result typing.
      ([evidence](equality-and-nullability.md))

- [x] **TYP-10** Support generic functions, data/sum declarations, aliases, explicit arguments, and unambiguous
      inference.
      ([evidence](function-contracts.md))

- [x] **TYP-11** Keep unconstrained generic parameters nullable-capable and enforce explicit non-null Any bounds.
      ([tests](conformance/generics.json))

- [x] **TYP-12** Check every generic body at definition time under its constraints, even when never instantiated.
      ([tests](conformance/generics.json))

- [x] **TYP-13** Validate nominal and capability bounds after complete interface resolution, including unused
      declarations. ([tests](conformance/generics.json))

- [x] **TYP-14** Infer generic arguments from compatible joins and expected types without accidental owner-parameter
      capture.
      ([evidence](function-contracts.md))

- [x] **TYP-15** Implement invariant defaults, checked declaration-site in/out variance, and function
      contravariance/covariance.
      ([evidence](conformance/type-interactions.md))

- [x] **TYP-16** Implement immutable List/Set element and Map-value covariance while preserving invariant Map keys.
      ([tests](conformance/generics.json))

- [x] **TYP-17** Keep mutable collection arguments invariant; do not invent mutable-to-mutable scalar widening.
      ([tests](conformance/generics.json))

- [x] **TYP-18** Implement star-projection upper/lower views, including safe reads, callbacks, bounds, nulls, and empty
      varargs.
      ([evidence](projection-semantics.md))

- [x] **TYP-19** Reject hidden-dependent unsafe operations without rejecting safe operations proved by selected bounds.
      ([evidence](projection-semantics.md))

- [x] **TYP-20** Automatically derive Equatable and StableKey from complete field/payload/container graphs.
      ([evidence](../bifoil-compiler/src/declarations/capabilities/query.rs))

- [x] **TYP-21** Reject unstable mutable/transitively mutable keys; terminate capability proofs over recursive
      declarations. ([tests](conformance/generics.json))

- [x] **TYP-22** Require equality capabilities on search/removal operations while permitting non-comparing collection
      operations. ([tests](conformance/generics.json))

- [x] **TYP-23** Preserve runtime generic identity through covariance, projections, copies, aliases, casts, and
      checkpoints.
      ([evidence](conformance/generics.json))

- [x] **TYP-24** Handle recursive nominal bounds, generic aliases, cyclic module interfaces, and dependent-bound
      termination.
      ([evidence](type-constraints.md))

- [x] **TYP-25** Apply Nothing only after validating reached operands; prevent bottom propagation from hiding type
      errors. ([tests](conformance/generics.json))

- [x] **TYP-26** Verify combined subtype, conversion, generic-inference, overload, and Unit-context behavior
      systematically.
      ([evidence](function-contracts.md))

### Control flow, initialization, narrowing, and captures

- [x] **FLW-01** Track definite and possible initialization separately at every reachable program point.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-02** Enforce read-before-write rejection and at-most-once delayed val assignment across all control
      transfers. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-03** Join real normal-completion branch states; ignore unreachable exits without executing their effects.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-04** Model short-circuit, safe-call, Elvis, and constant branches without counting skipped writes as
      executed. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-05** Analyze do/while body declarations at the closing condition, including continue-before-initialization
      paths. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-06** Analyze loop bodies, zero-iteration paths, known nonempty traversal, breaks, continues, and labeled
      targets. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-07** Preserve immutable nonempty facts through aliases/captures; do not freeze mutable container aliases.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-08** Validate repeated conditions/backedges and reject a second possible write to the same delayed val.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-09** Infer returns from actual loop/branch exits, with Nothing paths and ordinary Unit completion
      distinguished. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-10** Invalidate narrowing when writes, aliases, calls, defaults, method bodies, or suspension may change the
      proof.
      ([evidence](binding-flow-semantics.md#refinement-invalidation))

- [x] **FLW-11** Narrow captured when subjects independently from original mutable bindings that may have changed.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-12** Track selected field/index/key facts through receiver replacement and relevant collection mutations.
      ([evidence](../bifoil-compiler/src/compiler/field_proofs.rs))

- [x] **FLW-13** Keep legacy global proxies volatile; only a copied local snapshot can retain a stable narrowing proof.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-14** Discover lexical capture reads/writes without extending declaration-time name visibility.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-15** Prove captured initialization at every possible reading call, including mutual recursion and forwarded
      calls.
      ([evidence](binding-flow-semantics.md#captured-reads-call-profiles-and-recursion))

- [x] **FLW-16** Handle selected overload/default/callback dependencies conservatively without borrowing unselected
      effects. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-17** Support proven direct helpers initializing delayed captured vals, including exclusive and terminal loop
      paths. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-18** Distinguish one executed initializer call from multiple syntactic sites; enforce protected-state checks
      per call. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-19** Reject unproved indirect or escaping captured writers; extend proofs only where soundly justified.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-20** Check closure publication through returns, arguments, fields, collections, shared storage, and nested
      captures.
      ([evidence](binding-flow-semantics.md#escaping-values-and-lexical-lifetime))

- [x] **FLW-21** Preserve shared mutable cells across sibling closures and fresh bindings across separate enclosing
      calls. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-22** Preserve original operand types/snapshots during later effects; inference and lowering must share
      ordered flow. ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-23** Model return/break/continue/goto expressions without allowing statement-only assignment expressions.
      ([tests](../bifoil-compiler/src/tests/flow.rs))

- [x] **FLW-24** Verify safe/unsafe paired cases across aliases, generics, defaults, recursion, suspension, and
      source-free modules.
      ([evidence](binding-flow-semantics.md#implementation-and-evidence))

### Calls, overloads, function values, defaults, and variadics

- [x] **CAL-01** Implement fun-only declarations, mandatory parameter types, inferred/explicit returns, and expression
      bodies. ([tests](conformance/overloads.json))

- [x] **CAL-02** Enforce explicit value returns in named block functions and natural/bare-return Unit completion.
      ([tests](conformance/overloads.json))

- [x] **CAL-03** Implement immutable parameters and local-only var rebinding without changing caller bindings.
      ([tests](conformance/overloads.json))

- [x] **CAL-04** Give self/mutual recursive calls fresh activation frames, locals, and correctly shared captures.
      ([tests](conformance/overloads.json))

- [x] **CAL-05** Support positional/named arguments with positional-first ordering, duplicate/unknown-name diagnostics.
      ([tests](conformance/overloads.json))

- [x] **CAL-06** Evaluate callable/receiver first, then each supplied argument and conversion in written order.
      ([tests](conformance/overloads.json))

- [x] **CAL-07** Evaluate only omitted defaults per call, in parameter order, using earlier parameters and definition
      scope. ([tests](conformance/overloads.json))

- [x] **CAL-08** Allow defaults before required parameters without changing positional binding or named omission
      semantics. ([tests](conformance/overloads.json))

- [x] **CAL-09** Preserve evaluation exactly once across suspension in callable expressions, arguments, and defaults.
      ([tests](conformance/overloads.json))

- [x] **CAL-10** Implement typed first-class references and anonymous expression/block bodies with lambda-local early
      returns. ([tests](conformance/overloads.json))

- [x] **CAL-11** Limit contextual Unit result discarding to anonymous construction; do not silently adapt existing
      functions. ([tests](conformance/overloads.json))

- [x] **CAL-12** Resolve overloaded references against a unique expected function type with no default/name metadata
      leakage.
      ([evidence](conformance/type-interactions.md))

- [x] **CAL-13** Rank argument conversions by dominance: exact, widening, copying, then copying plus widening.
      ([tests](conformance/overloads.json))

- [x] **CAL-14** Apply nonvariadic, fewer-default, and nongeneric tie-breakers in order; report remaining ambiguity.
      ([tests](conformance/overloads.json))

- [x] **CAL-15** Enforce function subtype variance and ordinary-to-suspend widening without creating conversion
      adapters.
      ([evidence](conformance/type-interactions.md))

- [x] **CAL-16** Capture bound receivers once; preserve private method eligibility and selected generic receiver
      arguments. ([tests](conformance/overloads.json))

- [x] **CAL-17** Implement final-only typed vararg parameters in named and anonymous functions and function-value
      signatures. ([tests](conformance/overloads.json))

- [x] **CAL-18** Give every invocation a fresh immutable List for zero, individual, interleaved spread, or named-list
      groups. ([tests](conformance/overloads.json))

- [x] **CAL-19** Expand spread groups at their source position and snapshot/convert before later argument effects.
      ([tests](conformance/overloads.json))

- [x] **CAL-20** Reject explicit vararg defaults, duplicate named/positional groups, and incompatible spread element
      types. ([tests](conformance/overloads.json))

- [x] **CAL-21** Verify function-value positional/explicit calling rules and the selected restrictions on function
      equality. ([tests](conformance/overloads.json))

### Numeric operations, fairmath, ranges, and progression behavior

- [x] **NUM-01** Check signed 32-bit constants and dynamic arithmetic without host-language overflow or silent wrapping.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-02** Handle minimum Int negation/division overflow and mathematically zero remainder by minus one
      distinctly. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-03** Implement truncating Int division/remainder, zero checks, signs, and mixed Float arithmetic.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-04** Enforce finite binary64 inputs/results and distinguish zero division, nonfinite overflow, and invalid
      results. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-05** Implement lossless Int-to-Float widening and explicit truncating, range-checked Float-to-Int
      conversion. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-06** Keep compile-time evaluation and runtime checks aligned, including dynamic controls that cannot
      constant-fold. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-07** Preserve pinned ChoiceScript fairmath calculation order, effective modifier signs, rounding, and
      directional clamps. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-08** Check fairmath base independently of modifier constancy; permit all finite signed modifier magnitudes.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-09** Support both fairmath binaries and compounds, Int/Float inputs, Int results, and minimum-Int modifiers.
      ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-10** Preserve fairmath endpoint/zero-modifier anomalies and explicit mixed-operation grouping with direct
      assertions. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-11** Define first-class inclusive/half-open ascending and inclusive downTo forms with immutable reusable
      values. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-12** Reject empty/reversed selected ranges statically when provable and dynamically otherwise; include zero
      counts. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-13** Check positive Int step, direction, aligned endpoints, terminal-step overflow, and endpoint extremes.
      ([evidence](conformance/cases/range-terminal-boundaries-source-free-checkpoint/main.bfl))

- [x] **NUM-14** Match the selected Kotlin stepped-membership contract, including large-progression cost and failure
      boundaries.
      ([evidence](progression-membership.md))

- [x] **NUM-15** Evaluate traversal bounds/iterables once and retain fresh immutable per-iteration bindings through
      captures. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **NUM-16** Test while/do-while, labeled break/continue, iteration transfers, and suspension at boundary values.
      ([evidence](conformance/cases/range-terminal-boundaries-source-free-checkpoint/main.bfl))

### Text, Unicode, interpolation, and rendering

- [x] **TXT-01** Represent immutable String and one-scalar Char values without accepting lone surrogates as characters.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-02** Implement scalar length/indexing/substrings, nonnegative indexes, empty slices, and checked bounds.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-03** Preserve exact scalar sequences without implicit normalization; compare scalar lexicographic order.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-04** Handle supplementary scalars, combining sequences, escaped delimiters, and mixed source newline
      encodings. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-05** Implement approved triple-string common-indent stripping without accidentally trimming semantic
      content.
      ([evidence](text-semantics.md))

- [x] **TXT-06** Evaluate ordinary String substitutions left to right with enclosing suspension permissions and no
      replay. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-07** Restrict prose/option substitutions to non-suspending directly renderable non-null primitive values.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-08** Support primitive formatting in String concatenation without adding general implicit
      primitive-to-String casts. ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-09** Widen Char to String losslessly and preserve exact-match overload preference.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-10** Define explicit conversions/rendering for nullable and composite values, including supported cycles and
      aliases.
      ([evidence](text-semantics.md))

- [x] **TXT-11** Keep immutable source text distinct from presentation escaping and native variable interpolation.
      ([tests](../bifoil-runtime/test/text.test.mjs))

- [x] **TXT-12** Bound processing of malformed external text and large strings; report scalar/source positions
      coherently.
      ([evidence](text-semantics.md#scalar-validation-and-limits))

- [x] **TXT-13** Avoid host recursion and argument-count limits in large rendering/interpolation operations.
      ([tests](../bifoil-runtime/test/text.test.mjs))

### Collections, conversion copies, equality, and keys

- [x] **COL-01** Implement immutable/mutable List, Set, and Map families with the selected alias and mutation contracts.
      ([tests](conformance/foundations.json))

- [x] **COL-02** Support list/set/map literals, explicit mutable prefixes, contextual mutability, and expected-type
      empty forms. ([tests](conformance/foundations.json))

- [x] **COL-03** Infer compatible scalar/nullable element joins without arbitrary heterogeneous fallback or accidental
      copies. ([tests](conformance/foundations.json))

- [x] **COL-04** Evaluate elements left to right; check duplicate map keys before evaluating the duplicate entry's
      value. ([tests](conformance/foundations.json))

- [x] **COL-05** Coalesce equal set elements and preserve first-insertion order; retain map position on replacement.
      ([tests](conformance/foundations.json))

- [x] **COL-06** Move removed/reinserted members to the end and verify duplicate behavior after approved conversions.
      ([tests](conformance/foundations.json))

- [x] **COL-07** Implement size, zero-based indexing, nullable map lookup, and independent key-presence membership.
      ([tests](conformance/foundations.json))

- [x] **COL-08** Implement mutable indexed assignment and all selected add/remove/clear/copy operation signatures and
      results.
      ([evidence](collection-operations.md))

- [x] **COL-09** Share same-family mutable containers; copy between immutable/mutable families at assignment/argument
      time. ([tests](conformance/foundations.json))

- [x] **COL-10** Combine family copies with approved scalar widening while preserving independent container storage.
      ([tests](conformance/foundations.json))

- [x] **COL-11** Lift widening recursively through immutable layers and stop at mutable contained arguments.
      ([tests](conformance/foundations.json))

- [x] **COL-12** Preserve shallow referenced-element sharing through copies, snapshots, map entries, and checkpoints.
      ([tests](conformance/foundations.json))

- [x] **COL-13** Snapshot collection traversal once; preserve referenced element semantics while original containers
      mutate. ([tests](conformance/foundations.json))

- [x] **COL-14** Expose checked map entry key/value fields and the selected entry/destructuring interface.
      ([evidence](collection-operations.md))

- [x] **COL-15** Compare ordered lists and unordered sets/maps structurally under compatible ordinary-equality rules.
      ([evidence](equality-and-nullability.md))

- [x] **COL-16** Implement exact equality with matching declared comparison types/families/arguments and recursive
      exact contents; preserve construction identities for type tests and casts.
      ([evidence](comparison-view-equality.md#execution-and-persistence))

- [x] **COL-17** Compare nulls and present nullable values correctly; preserve types established by prior conversions.
      ([tests](conformance/foundations.json))

- [x] **COL-18** Compare cyclic graphs safely without making shared-reference layout determine value equality.
      ([tests](conformance/foundations.json))

- [x] **COL-19** Roll back failed unordered candidate comparisons so cyclic pair tracking cannot manufacture equality.
      ([tests](conformance/foundations.json))

- [x] **COL-20** Require static equality eligibility, including through Any, generic bounds, variants, and composite
      fields.
      ([evidence](conformance/type-interactions.md))

- [x] **COL-21** Keep stable-key qualification, hashing/indexing, ordinary equality, widening, and insertion coalescing
      coherent.
      ([evidence](conformance/collection-graph-interactions.md#paired-failures-and-indexes))

- [x] **COL-22** Rebuild transient indexes safely after mutation, collection, and restore without retaining dead
      containers. ([tests](conformance/foundations.json))

- [x] **COL-23** Test nested nullable/mutable/immutable/generic cyclic structures in source and source-free execution.
      ([evidence](conformance/collection-graph-interactions.md))

### Data classes, enums, sealed sums, and pattern matching

- [x] **DAT-01** Implement nominal typed field blocks, val/var field restrictions, shared instance assignment, and alias
      updates. ([tests](conformance/nominals.json))

- [x] **DAT-02** Generate field constructors with declaration-order positional/named/default inputs evaluated per
      construction. ([tests](conformance/nominals.json))

- [x] **DAT-03** Separate private field access from externally supplied constructor/copy inputs as selected.
      ([tests](conformance/nominals.json))

- [x] **DAT-04** Implement public-by-default members, explicit visibility, implicit receiver, and unambiguous bare
      lookup. ([tests](conformance/nominals.json))

- [x] **DAT-05** Support ordinary/suspend methods, overloads, recursion, generics, defaults, and saved bound references.
      ([tests](conformance/nominals.json))

- [x] **DAT-06** Generate shallow copy with retained current omitted fields and selected receiver/input evaluation
      order.
      ([evidence](collection-operations.md))

- [x] **DAT-07** Prevent user-defined member collisions with generated construction/copy behavior according to the final
      rule.
      ([evidence](clarification-conformance.md#generated-members-and-module-values))

- [x] **DAT-08** Derive structural equality/capabilities over fields and payloads, preserving nominal identity and
      mutation rules.
      ([evidence](equality-and-nullability.md))

- [x] **DAT-09** Implement plain enum syntax, qualified/shorthand cases, stable equality, aliases, and exhaustive
      coverage. ([tests](conformance/nominals.json))

- [x] **DAT-10** Implement sealed case declarations, payload defaults, payload-free constants, and distinct variant
      subtypes. ([tests](conformance/nominals.json))

- [x] **DAT-11** Widen variants to sealed parents without losing payload, generic, or exact-equality identity.
      ([evidence](comparison-view-equality.md#regression-evidence))

- [x] **DAT-12** Implement one-level variant tests/destructuring, immutable branch bindings, ignored fields, and named
      payload access. ([tests](conformance/nominals.json))

- [x] **DAT-13** Implement subject-based/subjectless when, subject capture, local val headers, and source-order first
      matching. ([tests](conformance/nominals.json))

- [x] **DAT-14** Test value/null/membership cases, comma alternatives, and matching binding names with compatible joined
      types. ([tests](conformance/nominals.json))

- [x] **DAT-15** Evaluate guards once after matching; preserve false-guard effects and continue to later alternatives.
      ([tests](conformance/nominals.json))

- [x] **DAT-16** Restrict fallback placement, distinguish statement no-match behavior, and prove expression
      exhaustiveness.
      ([evidence](conformance/cases/when-contracts-source-free-checkpoint/main.bfl))

- [x] **DAT-17** Handle Boolean/enum/sealed/nullable coverage, guards, generics, Nothing, and compatible final branch
      results.
      ([evidence](conformance/cases/when-contracts-source-free-checkpoint/helpers.bfl))

- [x] **DAT-18** Verify private/defaulted/generic nominal behavior through imports, artifacts, copies, suspension, and
      restore.
      ([evidence](conformance/cases/nominal-contracts-source-free-checkpoint/main.bfl))

### Prose, choices, story flow, and suspension

- [x] **STY-01** Implement explicit unquoted prose blocks, structural indent removal, paragraph flow, and explicit line
      breaks.
      ([evidence](prose-semantics.md))

- [x] **STY-02** Preserve prose/code mode across nested directives, branches, loops, functions, and continued
      interpolations.
      ([evidence](prose-semantics.md))

- [x] **STY-03** Implement literal interpolation/directive/backslash escapes without native re-interpolation at
      presentation time. ([tests](conformance/expressions.json))

- [x] **STY-04** Implement option headers with interpolated labels, visibility, enabled state, once history, and
      selected bodies. ([tests](conformance/expressions.json))

- [x] **STY-05** Snapshot prepared options in source order, with visibility first and enabling/label only when
      applicable.
      ([evidence](clarification-conformance.md#choice-preparation))

- [x] **STY-06** Preserve permitted non-suspending preparation effects and skip hidden/consumed work under the resolved
      contract.
      ([evidence](clarification-conformance.md#choice-preparation))

- [x] **STY-07** Reject suspension in prose/label/preparation contexts even through function values, defaults, or
      indirect calls. ([tests](conformance/expressions.json))

- [x] **STY-08** Continue after normal option completion while honoring return/break/continue/goto from option bodies.
      ([tests](conformance/expressions.json))

- [x] **STY-09** Handle no selectable options with explicit fallback or required static/dynamic failure.
      ([tests](conformance/expressions.json))

- [x] **STY-10** Persist story-wide per-option-site once consumption across visits, recursive calls, and same-build
      restores. ([tests](conformance/expressions.json))

- [x] **STY-11** Mark named/anonymous functions and function types suspend; allow scene bodies to suspend automatically.
      ([tests](conformance/expressions.json))

- [x] **STY-12** Check ordinary-to-suspend widening and reject effect hiding through references, generic values, or
      adapters. ([tests](conformance/expressions.json))

- [x] **STY-13** Permit suspension in enclosing-allowed expressions while preserving operands, addresses, arguments, and
      branch state. ([tests](conformance/expressions.json))

- [x] **STY-14** Resume without repeating completed side effects, conversions, defaults, text rendering, or option
      preparation. ([tests](conformance/expressions.json))

- [x] **STY-15** Clean abandoned expression/loop state on transfers while preserving surrounding live expression
      progress. ([tests](conformance/expressions.json))

- [x] **STY-16** Test nested choices, recursive suspension, labeled loop transfers, and effects in ordinary/value block
      expressions.
      ([evidence](conformance/cases/nested-recursive-story-expression-source-free/main.bfl))

### Scenes, shared state, initialization, and module startup

- [x] **SCN-01** Implement named scene bodies, declaration separation, entry selection, and library initialization
      constraints.
      ([evidence](clarification-conformance.md#generated-members-and-module-values))

- [x] **SCN-02** Implement typed scene input signatures and defaults, visit-local bindings, and checked scene reference
      values. ([tests](conformance/shared.json))

- [x] **SCN-03** Resolve named scene targets with named/default arguments and reference-valued targets with explicit
      positions. ([tests](conformance/shared.json))

- [x] **SCN-04** Evaluate/capture targets, supplied inputs, conversions, and omitted defaults in the selected order.
      ([tests](conformance/shared.json))

- [x] **SCN-05** Implement returning visit and one-way goto with the required current-visit/function-frame abandonment.
      ([tests](conformance/shared.json))

- [x] **SCN-06** Retain earlier scene callers across replacement; natural completion returns Unit or finishes the story.
      ([tests](conformance/shared.json))

- [x] **SCN-07** Implement shared val/var storage distinct from ordinary per-visit values and selected library bindings.
      ([evidence](modules-and-names.md))

- [x] **SCN-08** Resolve shared names module-wide and initialize dependencies fully before starting a dependent
      initializer. ([tests](conformance/shared.json))

- [x] **SCN-09** Include dependencies reached through defaults, methods, recursion, callbacks, and cross-module
      artifacts. ([tests](conformance/shared.json))

- [x] **SCN-10** Reject conservative dependency cycles and unresolved unsafe initialization without reading
      uninitialized state. ([tests](conformance/shared.json))

- [x] **SCN-11** Use deterministic module/source order for independent initializers; preserve ordinary effect order
      inside each. ([tests](conformance/shared.json))

- [x] **SCN-12** Restore initialized shared state without rerunning startup or triggering initializers on reads/writes.
      ([tests](conformance/shared.json))

- [x] **SCN-13** Test scene references/call stacks/shared initialization through cyclic modules and source-free linkage.
      ([tests](conformance/shared.json))

### Typed legacy ChoiceScript interoperability

- [x] **LEG-01** Define and validate the supported unchanged-engine/runtime profile and required extension installation.
      ([tests](conformance/legacy.json))

- [x] **LEG-02** Preserve unchanged legacy source bytes, case rules, scopes, expressions, labels, and native control
      behavior. ([tests](conformance/legacy.json))

- [x] **LEG-03** Implement declared typed global proxies and subroutine interfaces with checked inbound and outbound
      values. ([tests](conformance/legacy.json))

- [x] **LEG-04** Validate Int/Float/Boolean/String/Char, plain enum case names, nullability, and result bindings
      strictly. ([tests](conformance/legacy.json))

- [x] **LEG-05** Reject implicit trust of unknown values and numeric-string coercion; preserve real native
      failures/source context. ([tests](conformance/legacy.json))

- [x] **LEG-06** Require ordinary bridges to return; reject unexpected native transfers or game termination.
      ([tests](conformance/legacy.json))

- [x] **LEG-07** Implement explicit transfer bridges that abandon Bifoil callers and may transfer or terminate natively.
      ([tests](conformance/legacy.json))

- [x] **LEG-08** Preserve native call/temp/stat/navigation state, aliases, cycles, and prepared inputs across same-build
      restore. ([tests](conformance/legacy.json))

- [x] **LEG-09** Validate bridge effects, defaults, variadics, source-free interfaces, and live-proxy narrowing
      restrictions. ([tests](conformance/legacy.json))

- [ ] **LEG-10** Implement the approved composite bridge contract for collections/data/generics only after CON-17 is
      resolved.

- [x] **LEG-11** Enumerate supported native UI/platform commands; implement required coverage or document explicit
      profile limits.
      ([evidence](legacy-compatibility.md))

- [x] **LEG-12** Verify native choice/page/text/number waits, output/image/chart ordering, validation feedback, and no
      replay. ([tests](conformance/legacy.json))

- [x] **LEG-13** Index labels and validate references with bounded work; preserve native whitespace/case matching.
      ([tests](conformance/legacy.json))

- [x] **LEG-14** Differential-test relevant behavior against the explicitly supplied pinned unmodified interpreter.
      ([tests](conformance/legacy.json))

- [x] **LEG-15** Verify bridge snapshots never execute native reads/calls or replay completed preparation while saving.
      ([tests](conformance/legacy.json))

- [x] **LEG-16** Keep original fixtures, engine licensing/provenance, and standalone builds independent of private story
      sources. ([tests](conformance/legacy.json))

### Lowering, execution representation, heap, and collection

- [x] **VM-01** Define typed instruction contracts for every accepted operation, effect, transfer, declaration, and
      source span.
      ([evidence](../bifoil-runtime/INSTRUCTIONS.md))

- [x] **VM-02** Preserve case-sensitive declaration identities and detect composition conflicts across independent
      modules. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-03** Lower each source evaluation exactly once in the selected order; keep checked and captured operand types
      aligned. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-04** Preserve block scopes, activation frames, shared cells, generic arguments, bound receivers, and
      temporary values. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-05** Encode nominal/variant/generic identities consistently across tests, casts, conversions, equality, and
      saves. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-06** Check program, module, package, callable, heap, and instruction shapes before using malformed metadata.
      ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-07** Treat checksums as integrity checks rather than publisher authentication; define trusted artifact
      inputs. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-08** Execute already compiled code; do not defer Bifoil parsing/type checking or source compilation to player
      startup. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-09** Reclaim unreachable cells/environments/objects while preserving live closures, forward cells, aliases,
      and cycles. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-10** Trace frames, expression operands, traversal snapshots, assignment addresses, bound receivers, and
      native state. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-11** Avoid host recursion/argument-array limits for deep equality, rendering, conversions, and large argument
      groups.
      ([evidence](../bifoil-runtime/VALUE_OPERATIONS.md))

- [x] **VM-12** Make execution slicing resumable and cancel obsolete scheduled continuations after replacement/failure.
      ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-13** Keep active runtime allocation/work guards distinct from static source admission and compiler memory
      budgets. ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-14** Validate growth/failure behavior at active call/heap/checkpoint limits with meaningful diagnostics.
      ([tests](../bifoil-runtime/test/collector.test.mjs))

- [x] **VM-15** Implement lazy/on-demand compiled code loading for the capacity architecture, with checked identity and
      lifetime.
      ([evidence](../bifoil-runtime/LAZY_PACKAGES.md))

- [x] **VM-16** Preserve independent host/VM responsibilities and one maintainable implementation of each runtime
      behavior. ([tests](../bifoil-runtime/test/collector.test.mjs))

### Persistence, checkpoints, and host lifecycle

- [x] **SAV-01** Save only supported fully prepared player-input checkpoints and reject unsupported save positions
      explicitly. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-02** Preserve active function/scene calls, locals, captured cells, current generic arguments, and shared
      state. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-03** Preserve completed operands/arguments/conversions, assignment targets, traversal cursors/snapshots, and
      prose. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-04** Preserve prepared labels/enabled states, native waits, consumed option history, and retained caller
      frames. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-05** Serialize graph aliasing/cycles without duplicating shared mutable bindings or losing distinct
      invocation cells. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-06** Validate build/profile/schema/type/references/frames/choice targets before attaching restored
      execution. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-07** Accept matching-build checkpoints and reject genuinely different edited builds before any story side
      effects. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-08** Retain intrinsic callable/receiver types through exposed views, projected values, collection, and
      restoration. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-09** Restore into a fresh host/runtime instance and prove completed effects/preparation/defaults do not
      replay. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-10** Preserve a working session if proposed restored data is invalid; release owned old continuations only
      when safe. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-11** Remove consumed forms/buttons and reject stale selection/submission callbacks without losing live
      waits. ([tests](../bifoil-runtime/test/runtime.test.mjs))

- [x] **SAV-12** Separate transcript/presentation persistence from VM state and test the complete host save/load
      lifecycle.
      ([evidence](../bifoil-runtime/BROWSER_ACCEPTANCE.md#host-save-contract))

- [x] **SAV-13** Verify repeated save/restore, large live graphs, collection after restore, and replacement/detachment
      cleanup.
      ([evidence](../bifoil-runtime/VALUE_OPERATIONS.md#large-checkpoint-graphs))

- [x] **SAV-14** Document same-build-only compatibility; do not imply cross-update migration or checkpoint
      authentication. ([tests](../bifoil-runtime/test/runtime.test.mjs))

### Ahead-of-time modules, artifacts, cache, and atomic publication

- [x] **AOT-01** Produce valid extended ChoiceScript and reusable compiled modules with explicit runtime compatibility
      metadata. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-02** Compile clients against independently produced interfaces after dependency sources are removed.
      ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-03** Include visibility, signatures, defaults, varargs, constraints, nominal identity, and effects in
      interfaces. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-04** Validate structural/schema/digest/dependency/producer compatibility before trusting stored lowered
      bodies. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-05** Reject older unchecked module producers explicitly; regenerate affected artifacts from source.
      ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-06** Preserve cyclic-group fingerprints and reject mixed versions or partially replaced strongly connected
      groups. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-07** Keep disposable cache invalidation separate from public module compatibility and trust policy.
      ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-08** Invalidate on source bytes, compiler identity, interface/dependency changes, native inputs, and
      relevant options. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-09** Detect same-size/same-timestamp edits, changed discovery inputs, damaged chunks, and missing/corrupt
      receipts. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-10** Canonicalize source/cache/artifact discovery so equivalent builds produce identical output and
      identities. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-11** Verify cold, warm, receipt-loss, clean, source-free, cyclic, inline, and package determinism.
      ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-12** Stream hashing/serialization/body input with bounded buffers and avoid duplicate complete decoded
      programs. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-13** Publish completed code chunks before their root and preserve the last completed build on every failure.
      ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-14** Validate completed-output reuse against all required inputs and referenced outputs rather than
      timestamps alone. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-15** Handle interrupted/concurrent publication and owned temporary-file cleanup without corrupting reusable
      outputs. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-16** Define safe retention/cleanup of reusable immutable chunks without deleting outputs needed by other
      builds.
      ([evidence](../bifoil-compiler/README.md#compiled-code-packages))

- [x] **AOT-17** Verify canonical hashes cover the intended bytes and distinguish inline/package/checkpoint build
      identities. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

- [x] **AOT-18** Keep compiler/module/runtime use independent of adjacent checkouts through explicit paths/versioned
      contracts. ([tests](../bifoil-compiler/tests/cli/encoded_modules.rs))

### Capacity architecture and the resource contract

- [ ] **CAP-01** Select target-scale workload families reaching tens to hundreds of millions of source lines
      meaningfully.

- [ ] **CAP-02** Publish source bytes, module/dependency shapes, declaration/type complexity, code volume, and
      diagnostic loads.

- [x] **CAP-03** Specify reference hardware, operating system, storage, concurrency, and cold/warm/precompiled cache
      conditions.
      ([evidence](../bifoil-compiler/NARRATIVE_CAPACITY.md#reference-conditions-and-retained-observations))

- [ ] **CAP-04** Measure strict aggregate simultaneous compiler-plus-helper memory, including native allocations and
      mappings.

- [ ] **CAP-05** Use justified peak accounting that cannot silently miss short spikes; document metric and enforcement
      headroom.

- [x] **CAP-06** Include process startup, discovery, required compilation/linking, artifact writes, and owned cleanup in
      timing.
      ([evidence](../bifoil-compiler/NARRATIVE_CAPACITY.md#measurement-validation-and-implementation-boundary))

- [ ] **CAP-07** Keep incremental builds strictly below ten seconds under the published supported workload/reference
      conditions.

- [x] **CAP-08** Let clean-build work scale with input; document its measured throughput without claiming the
      incremental bound.
      ([evidence](../bifoil-compiler/NARRATIVE_CAPACITY.md#reference-conditions-and-retained-observations))

- [ ] **CAP-09** Page declaration interfaces, symbol/type/dependency indexes, and large cyclic components instead of
      retaining all.

- [ ] **CAP-10** Bound active AST, parsing, semantic-analysis, diagnostic, and lowered-body memory at target-scale
      inputs.

- [ ] **CAP-11** Avoid rescanning/decoding/relinking every unchanged reachable module after a bounded incremental edit.

- [ ] **CAP-12** Implement scalable artifact lookup and dependency invalidation without quadratic graph or metadata
      growth.

- [ ] **CAP-13** Bound source/native discovery, marker reads, label indexing, hashing, output verification, and failure
      work.

- [x] **CAP-14** Coordinate package layout and lazy runtime loading so source capacity does not require all code
      resident in play.
      ([evidence](../bifoil-compiler/NARRATIVE_CAPACITY.md))

- [ ] **CAP-15** Replace small development admission guards only when measured architecture supports larger inputs
      safely.

- [ ] **CAP-16** Measure unchanged builds, leaf edits, interface edits, fan-out invalidation, cyclic edits, and
      source-free linking.

- [ ] **CAP-17** Measure heavy generics, broad scopes, many paths, long imports, large literals, and large generated
      code.

- [ ] **CAP-18** Exercise missing/corrupt caches, budget failures, allocation failures, cancellations, and prior-root
      preservation.

- [ ] **CAP-19** Establish appropriate memory/deadline enforcement on every claimed host platform, including
      Windows/macOS.

- [x] **CAP-20** Preserve failure status and explicit diagnostics instead of treating killed/rejected jobs as successful
      compliance. ([tests](../bifoil-compiler/tools/test_run_conformance.py))

- [ ] **CAP-21** Retain all raw results, failures, identities, worst observations, and exact workload generators/inputs.

- [x] **CAP-22** Separate instrumented coverage/test execution from isolated production resource measurements.
      ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **CAP-23** Test active runtime allocation, call depth, long execution, collector pressure, and checkpoint size
      independently. ([evidence](../bifoil-runtime/CAPACITY_TESTS.md))

- [ ] **CAP-24** Demonstrate the accepted capacity and strict budgets together; raising configured limits alone is
      insufficient.

### Diagnostics, failure handling, and operational correctness

- [x] **ERR-01** Distinguish provable compile-time rejection from checked dynamic failure for every selected operation.
      ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-02** Report original Bifoil file/physical line and useful operation context through artifacts and runtime
      adapters. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-03** Improve continued-expression operation attribution beyond the current expression-start precision where
      needed. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-04** Keep legacy execution locations and Bifoil bridge call locations attributable without rewriting native
      sources. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-05** Fail fast on checked runtime failures and preserve the original terminal diagnostic on later API
      requests. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-06** Drain previously completed output once before reporting failure without replaying output or continuing
      execution. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [x] **ERR-07** Keep invalid player input/host selection recoverable at the prepared wait as distinct from checked
      story failure. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [ ] **ERR-08** Clean owned files/processes/callbacks/continuations on success, errors, signals, interruption, and
      replacement.

- [ ] **ERR-09** Reject malformed manifests, paths, interfaces, programs, packages, and saves with bounded processing.

- [x] **ERR-10** Preserve previously completed outputs and working sessions across rejected
      builds/restores/publications. ([tests](../bifoil-compiler/src/tests/source_locations.rs))

- [ ] **ERR-11** Keep errors actionable without exposing credentials, private source material, or machine-specific
      public paths.

### Conformance, interaction coverage, and final verification

- [ ] **QA-01** Map every accepted decision to meaningful direct assertions, expected rejections, or justified
      architecture evidence.

- [x] **QA-02** Keep the 305-ID ledger synchronized with exact steering text, statuses, reciprocal links, and real
      source inputs. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [ ] **QA-03** Close all 26 determined review obligations below with direct evidence and explicit remaining-scope
      accounting.

- [x] **QA-04** Run every applicable case through formatted/idempotent source, inline output, and compiled package
      output. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **QA-05** Exercise independently compiled interfaces and remove dependency sources before client
      compilation/execution. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **QA-06** Save/restore at every supported input wait and assert values, transcripts, effects, snapshots, and no
      replay. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [ ] **QA-07** Pair valid/invalid and constant/dynamic controls; do not let constant folding substitute for runtime
      checking.

- [x] **QA-08** Build a systematic interaction matrix for nullability, generics, variance, aliases, effects, overloads,
      and captures.
      ([evidence](conformance/type-interactions.md))

- [x] **QA-09** Cover collections/data cycles, stable keys, copies, exact equality, projections, and runtime identity
      together.
      ([evidence](conformance/collection-graph-interactions.md))

- [ ] **QA-10** Cover scenes/defaults/shared initialization/legacy boundaries with recursion, cyclic imports, and
      checkpoints.

- [x] **QA-11** Test compiler/executor/formatter/precompiler silent failures, nonzero statuses, signals, timeouts, and
      empty runs.
      ([evidence](../bifoil-compiler/tools/test_run_conformance.py))

- [x] **QA-12** Ensure an expected diagnostic cannot conceal a crashed/terminated compiler or a failed execution phase.
      ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **QA-13** Validate case selection, duplicate/unknown IDs, malformed metadata, deterministic ordering, and bounded
      workers. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **QA-14** Retain original minimal cases, portable commands, exact revisions/fingerprints, failures, and
      reproducible reports. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [x] **QA-15** Run native unit/CLI tests, strict linting, formatting, tool regressions, and metadata validation without
      skips concealed. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [ ] **QA-16** Preserve current Sonar rules/gate, meaningful production coverage, and duplication limits without
      weakening scope.

- [x] **QA-17** Test real browsers/unchanged engine rendering, native waits, literal text, output order, and full-page
      reloads.
      ([evidence](../bifoil-runtime/BROWSER_ACCEPTANCE.md))

- [ ] **QA-18** Validate a complete original game using production-intended host persistence and generated deployable
      packages.

- [ ] **QA-19** Validate all claimed compiler/runtime host platforms and document support boundaries before declaring
      conformance.

- [ ] **QA-20** Conduct final independent source/behavior review only when separately authorized; record resulting gaps
      honestly.

- [ ] **QA-21** Update user/contributor/protocol/resource documentation to the final contract and remove obsolete
      completion claims.

- [x] **QA-22** Keep private reports and external game sources out of public fixtures/docs; preserve upstream licenses
      and provenance. ([checks](../bifoil-compiler/tools/collect-coverage.sh))

- [ ] **QA-23** Remove owned unneeded outputs and temporary files while preserving evidence, caches in use, and
      unrelated changes.

## Review obligations

- [x] **REVIEW-01** Verify Integer boundaries using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-02** Verify Finite Float using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-03** Verify Fairmath using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-04** Verify Safe-call laziness using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-05** Verify Evaluation order using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-06** Verify Duplicate keys using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-07** Verify Nullable map lookup using direct assertions and the required boundary cases.
      ([evidence](conformance/cases/collection-contracts-source-free-checkpoint/main.bfl))

- [x] **REVIEW-08** Verify Family copies/invariance using direct assertions and the required boundary cases.
      ([evidence](conformance/cases/collection-copies/main.bfl))

- [x] **REVIEW-09** Verify Shallow sharing using direct assertions and the required boundary cases.
      ([evidence](conformance/cases/collection-contracts-source-free-checkpoint/main.bfl))

- [x] **REVIEW-10** Verify Stable keys using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-11** Verify Empty traversals/ranges using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-12** Verify Do-condition assignment using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-13** Verify Numeric equality using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-14** Verify Generic reification using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-15** Verify Definition checking using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-16** Verify Overload ordering using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-17** Verify Enum conflicts using direct assertions and the required boundary cases.
      ([evidence](conformance/cases/generic-enum-shorthand-conflict-error/main.bfl))

- [x] **REVIEW-18** Verify Guard continuation using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-19** Verify Captured state using direct assertions and the required boundary cases.
      ([evidence](../bifoil-runtime/test/compact-captures.test.mjs))

- [x] **REVIEW-20** Verify Suspension effects using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-21** Verify Scene transfer using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-22** Verify Saved snapshots using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-23** Verify Build compatibility using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [x] **REVIEW-24** Verify Legacy validation using direct assertions and the required boundary cases.
      ([evidence](legacy-compatibility.md#checked-value-boundary))

- [x] **REVIEW-25** Verify Independent artifacts using direct assertions and the required boundary cases.
      ([assertions](conformance/review-coverage.md))

- [ ] **REVIEW-26** Verify Resource failure using direct assertions and the required boundary cases.

## Completion criteria

- [ ] **DONE-01** All 305 accepted decisions have complete, reviewed evidence or an explicitly approved scope amendment.

- [ ] **DONE-02** No material observable contract is silently chosen or still contradicted across
      steering/spec/code/runtime.

- [ ] **DONE-03** Native AOT compilation and independently compiled modules satisfy the complete selected source
      language.

- [ ] **DONE-04** Both output modes preserve semantics, runtime requirements, source locations, and compatibility
      rejection.

- [ ] **DONE-05** Whole-language conformance and interaction suites pass, including negative, source-free, and restored
      execution.

- [ ] **DONE-06** Same-build input-checkpoint persistence preserves every required live relationship without replay.

- [ ] **DONE-07** The supported legacy surface and all selected typed boundary contracts pass unchanged-engine
      acceptance.

- [ ] **DONE-08** Target-scale capacity, strict aggregate memory, and incremental timing pass the published acceptance
      protocol.

- [ ] **DONE-09** Every claimed compiler/runtime platform and production-intended host has matching acceptance evidence.

- [ ] **DONE-10** Source is human-readable and maintainable, with clear module ownership and no redundant semantic
      implementation.

- [ ] **DONE-11** Required checks pass; known defects/restrictions and evidence limitations are reconciled before
      completion claims.

- [ ] **DONE-12** Documentation, provenance, reproducibility, and cleanup are complete; release/publication remain
      separate actions.

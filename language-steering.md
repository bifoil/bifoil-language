# Bifoil language steering

Updated: 2026-10-25

## Status and use

This document records the provisional language decisions from the design discussion. It is a steering record for
continued discussion and eventual specification work, rather than a finalized grammar or conformance specification. The
latest direct user instruction takes precedence over this record.

Read this alongside [AGENTS.md](AGENTS.md) and [README.md](README.md). Examples illustrate the selected direction;
unspecified details in an example do not establish additional language rules.

The initial compiler/runtime slice was subsequently authorized on 2026-10-25. See [implementation
status](implementation-status.md) for the restricted profile and verified results. The full language design remains
provisional; this record does not imply implementation of every accepted feature.

The Bifoil Language repository is the default working directory until the user explicitly changes it.

**Discussion status:** The planned steering questionnaire is complete. The record contains 305 decision IDs, including
the final six answers and the preferred .bfl extension. The initial implementation slice is now underway.

**Discussion checkpoint:** Continue from the [specification draft](language-specification-draft.md), with incomplete
details marked explicitly. Stable decision IDs preserve traceability to the accepted choices.

**Specification review:** The draft now contains a concrete completion sequence and 26 review cases. The initial review
expands the resource protocol, module interface obligations, saved alias relationships, and legacy effects. Unresolved
type-identity and flow-analysis cases remain explicit; no accepted decisions were changed.

The broader question rounds are finished. Raise further steering only for a material conflict or a user-requested scope
change; routine grammar and implementation details belong in the draft and feasibility review.

Capacity clarification, 2026-10-25: the user expects projects in the tens to hundreds of millions of source lines before
reaching extreme capacity limits. The existing small compiler/runtime guards are development constraints and do not
establish the required capacity. Source capacity, compiler working memory, and the running story's live memory and
executed work must be measured separately; source length alone cannot bound a runaway loop or allocation.

Resource clarification, 2026-10-25: the under-ten-second target applies to incremental builds using precompiled modules.
This supersedes the earlier clean-build timing wording in S09/S14 below. Clean builds scale with total source input. The
compiler memory budget remains below 250,000,000 bytes; large-project capacity still requires implementation and
measurement rather than a larger configured limit.

Legacy control clarification, 2026-10-25: ordinary typed legacy bridges must return. Legacy scene transfers and game
termination require an explicit transfer bridge, rather than silently abandoning an ordinary Bifoil caller.

## Scope and compatibility

| ID  | Current direction                                                                                                                                 |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------|
| S01 | Bifoil is a strongly statically typed language. The current design focus is a more feature-complete, typed language compatible with ChoiceScript. |
| S02 | New syntax takes primary inspiration from Kotlin and Python.                                                                                      |
| S03 | Bifoil has its own syntax. Projects may include unchanged legacy ChoiceScript files through a compatibility front end.                            |
| S04 | Legacy files retain ChoiceScript's original semantics, including its scope and case rules. New Bifoil rules apply to new Bifoil source.           |
| S05 | Narrative-block syntax and unquoted prose follow T01.                                                                                             |
| S06 | The compiler must be a native implementation written in C++, Rust, or Go. The exact language has not been selected. This implementation constraint does not select native machine-code output for Bifoil programs. |
| S07 | The language must support pre-compilation. Ahead-of-time generation and reusable, independently compiled modules are required under S10. Native story executables remain unselected. |
| S08 | Compiler memory must remain below one quarter of a gigabyte at every moment. The strict numeric budget and process scope follow S13; exact measurement and enforcement remain to be specified. Compliance is unverified. |
| S09 | Compilation must take less than ten seconds within the supported maximum workload and reference environment under S14. Out-of-envelope and resource-budget failures follow S15; compliance is unverified. |
| S10 | The first compiler milestone requires ahead-of-time Bifoil-to-ChoiceScript compilation and reusable, independently compiled module artifacts. Native story executables have not been selected as an initial requirement. |
| S11 | Bifoil runtime extensions are permitted. A required runtime layer or engine extensions may provide features; compatibility requirements must be stated explicitly and Bifoil semantics preserved. Unmodified-engine compatibility is not an initial requirement. |
| S12 | Typed Bifoil and unchanged legacy ChoiceScript interact through explicit typed bridges. Cross-language calls and shared-state access require declared interfaces and checked conversions; unknown legacy values are never trusted implicitly. Legacy source retains its original semantics. |
| S13 | Peak aggregate compiler-and-helper memory must remain below 250,000,000 bytes at every moment. This is not an average or compiler-heap-only allowance. The exact measurement and enforcement protocol remains to be specified and validated. |
| S14 | Require a clean end-to-end compilation in under ten seconds for a published maximum-size/complexity workload on reference hardware. Workload, hardware, cache conditions, and full-pipeline measurements must be specified and tested before claiming compliance. |
| S15 | Inputs beyond the supported compilation envelope receive an explicit diagnostic. Compilation errors and resource-budget failures report failure rather than claiming a successful build. |

The initial ambition included Turing completeness, a compiler built around formal grammars, lexers and ASTs, both
machine-code and ChoiceScript output, and eventual self-hosting. The discussion subsequently narrowed its immediate
focus to the typed ChoiceScript-compatible language. Native output and self-hosting have not been finalized as current
deliverables or permanently abandoned. Turing completeness and the compiler architecture still need a whole-design
review.

This repository defines language behavior and eventual conformance examples. Compiler implementation belongs in Bifoil
Compiler; execution components belong in Bifoil Runtime. Compiler implementation is restricted by S06. The exact
language allowance remains unchanged. Rust and a versioned instruction interface are selected for the initial slice;
release commitments remain unselected.

Resource feasibility under S08-S09/S13-S15 has not been demonstrated. The accepted contract sets a strict aggregate
memory budget and an incremental-build time limit within a published workload and reference environment. Concrete
workload limits, hardware, and the measurement protocol remain to be specified and tested. Inputs outside that envelope
must receive an explicit failure diagnostic.

### Preferred extension and conflict check

Checked: 2026-10-25. The user prefers .bfl over the earlier .bifoil default. The provisional design uses .bfl as the
preferred candidate; this is a known shared extension.

- Betaflight uses BFL for blackbox flight logs. Its [file-association change][ext1] explicitly handles .bfl files; this
  is an active application-association collision.
- IBM's Bus Functional Language compiler accepts .bfl source files, documented in its [toolkit manual][ext2], section
  4.3. This is an existing domain-specific language use.
- The checked [GitHub Linguist language registry][ext3] contains no .bfl or .BFL entry. This does not prove that no
  other language or editor plugin uses the extension.

As integration guidance, identify Bifoil sources through the project manifest or explicit language selection in addition
to the extension. This check is not an exhaustive global registry or legal-clearance search.

## Layout, spelling, and names

| ID  | Current decision                                                                                                                                               |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| L01 | Ordinary code blocks use indentation and a colon to open the body.                                                                                             |
| L02 | On ordinary code lines, each tab and each complete group of four spaces adds one structural indentation level. Leftover spaces count as alignment.             |
| L03 | One tab followed by four spaces means two structural levels. Six spaces mean one level plus two alignment spaces.                                              |
| L04 | Tabs and spaces may be mixed for alignment under the preceding counting rule.                                                                                  |
| L05 | Ordinary expressions may continue inside parentheses or after an unfinished operator, such as `+` or `=`. Continuation indentation serves as alignment.        |
| L06 | Block expressions such as `if` retain their structural indentation rules within expressions.                                                                   |
| L07 | Corresponding conditional branch headers align, and corresponding branch bodies use the same indentation level. Standard formatting normalizes this structure. |
| L08 | Names and keywords are case-sensitive in new Bifoil source. Legacy source keeps its original rules.                                                            |
| L09 | Conditional branch spellings and their formatting follow E08.                                                                                                  |
| L10 | The function-declaration keyword follows F01.                                                                                                                  |
| L11 | Logical NOT uses `!`; AND/OR spelling and behavior follow E02. Equality operators follow E03 and E28-E30.                                                      |

## Bindings, scope, and nullability

| ID  | Current decision                                                                                                                                                                                                                                                                        |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| B01 | Infer variable types when possible. Allow optional annotations and require them when inference cannot establish a type. Static checking remains mandatory.                                                                                                                              |
| B02 | `val` declares a binding that cannot be reassigned; `var` declares a reassignable binding. Reassignment retains the binding's static type.                                                                                                                                              |
| B03 | Binding mutability and the mutability of referenced contents are separate. Collection-container mutability and aliasing follow D02/D05; data-instance sharing and field mutability follow U03/U05. Remaining object ownership rules are open.                                           |
| B04 | Names have block scope: they are visible only within their declaring block and nested blocks, with declaration order governed by B10. Captured bindings may remain alive under F21.                                                                                                     |
| B05 | Reject shadowing: a declaration cannot reuse a currently visible binding name. This includes implicit loop bindings. Same-scope function overload sets follow F23; nested shadowing remains prohibited.                                                                                 |
| B06 | Local `val` and `var` declarations may omit their initializer when they have an explicit type. Every read requires proven initialization.                                                                                                                                               |
| B07 | Each delayed-initialization `val` binding must be initialized at most once. Control-flow checks must enforce this per binding.                                                                                                                                                          |
| B08 | Types are non-null by default. `T?` permits `null`, which must be handled before the value can be used as `T`.                                                                                                                                                                          |
| B09 | Null checks automatically narrow a value's type where control flow proves that the value remains unchanged. Explicit handling is required when that proof is unavailable.                                                                                                               |
| B10 | A local variable name is visible from its declaration through the rest of its block and nested blocks. Local variable names are not visible before their declarations; function names retain F14's scope-wide visibility.                                                               |
| B11 | Safe member access and method calls use `?.`. Evaluate the receiver once; when it is null, yield null and skip method arguments and the call. Calls retain the ordinary suspension-effect checks.                                                                                       |
| B12 | Use `?:` for lazy null fallback. Evaluate the left operand once; evaluate the fallback only when that value is null. Precedence follows E12; detailed result typing remains to be specified.                                                                                            |
| B13 | Postfix `!!` converts `T?` to `T` with a runtime null check. Evaluate its operand once; a null value reports a runtime error, otherwise produce the non-null value.                                                                                                                     |
| B14 | Lift approved conversions through nullable types: convert a present value and preserve null. This includes `Int?` to `Float?`, `Char?` to `String?`, and nullable forms of approved collection copying and widening.                                                                    |
| B15 | Safe indexing of a nullable `String`, list, or map uses `?[index]`: for example, `items?[i]` or `mapping?[key]`. Evaluate the receiver once; null yields null and skips the index/key expression. A non-null receiver follows ordinary indexing, bounds, and missing-map-key rules.     |
| B16 | Safely invoke a nullable function value with `?.(arguments)`, for example `callback?.(value)`. Evaluate the callable once; null yields null and skips arguments and the call. Function-value argument rules and suspension-effect checks still apply.                                   |
| B17 | Nullable application flattens to one layer. For example, lookup in `Map<String, Int?>` returns `Int?`; absence and a stored null remain indistinguishable through lookup alone. Explicitly repeated nullable markers such as `Int??` are errors.                                        |
| B18 | A variable declaration initialized only with `null` requires an expected type: `val name: String? = null` is valid, while `val name = null` is an error. Empty and all-null collection literals retain D11's expected-type requirement.                                                 |
| B19 | Subject-based `when` cases contribute to automatic null narrowing. Infer non-null values in branches that exclude null; narrow an original binding only while flow analysis proves it still matches the captured subject. Writes, calls, and suspension must not invalidate that proof. |
| B20 | Expose Any as the universal non-null value type and Any? as its nullable form. Operations require appropriate static type information. Universal types do not introduce automatic Any fallback in common-type inference. |
| B21 | Test types in ordinary expressions with is and !is, for example value is Character or value !is Character. Existing case is Variant patterns remain available. |
| B22 | Use as for checked casts and as? for nullable casts, such as value as Character and value as? Character. A dynamic mismatch reports a runtime error for as and yields null for as?, subject to B24. |
| B23 | Casts check runtime type compatibility without scalar conversions or container copies. Use explicit conversion operations for value conversions; ordinary assignment and argument conversions remain available. |
| B24 | Reject a cast between concrete types when it is provably impossible at compile time, rather than generating an inevitable runtime error or null result. |
| B25 | Successful general type tests automatically narrow bindings in if branches and when cases where safe. Reuse the existing proof rules for writes, calls, aliases, and suspension; existing null narrowing remains available. |

## Boolean and text types

| ID  | Current decision                                                                                                                                                                                                                                                                                                                                                         |
|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P01 | Use Boolean as the boolean type, with lowercase true and false literals.                                                                                                                                                                                                                                                                                                 |
| P02 | Provide immutable String values and a distinct Char type. String indexing produces Char. Immutability concerns the contents; a var binding may still be reassigned.                                                                                                                                                                                                      |
| P03 | Use Unicode scalar values as the element model for string length, indexing, and Char: a Unicode code point excluding surrogates. A supplementary character such as U+1F600 occupies one element; combining sequences may occupy multiple elements. Legacy ChoiceScript retains S04.                                                                                      |
| P04 | String indexing uses s[i] with zero-based, nonnegative Int indexes. Provably invalid constant indexes are compile errors; other out-of-bounds indexes are runtime errors. Negative indexes are invalid.                                                                                                                                                                  |
| P05 | Ordinary String literals use double quotes and Char literals use single quotes. Escape forms follow P09.                                                                                                                                                                                                                                                                 |
| P06 | Ordinary String literals support ${expression} interpolation. Evaluate substitutions left to right under the enclosing expression's suspension permissions, preserving completed evaluation across suspension. Prose and option-label interpolation retain their non-suspending restrictions.                                                                            |
| P07 | Multiline String literals use triple double quotes with ordinary escape rules and interpolation. Common-indent stripping and retained newlines follow P10; detailed whitespace rules remain open.                                                                                                                                                                        |
| P08 | Prose and option-label interpolation directly render non-null String, Char, Int, Float, and Boolean values. Nullable values, Unit, collections, function values, scene references, and other types require explicit conversion to a renderable value. Exact boolean and numeric formatting remains open.                                                                 |
| P09 | Quoted String and Char literals, including triple-quoted strings, accept both braced Unicode scalar escapes (`\u{41}`, `\u{1F600}`; one to six hexadecimal digits) and fixed-width escapes (`\u0041`, `\U0001F600`; four or eight hexadecimal digits). Also support `\\`, `\"`, `\'`, `\n`, `\r`, `\t`, and `\${`. Unknown escapes and invalid scalar values are errors. |
| P10 | Triple-quoted strings strip common leading indentation from nonblank lines, while retaining newlines and other content. The precise treatment of tabs, blank lines, delimiter placement, and source newline encodings remains to be specified.                                                                                                                           |
| P11 | Obtain String length with the length property, for example text.length. The result is Int and counts Unicode scalar elements.                                                                                                                                                                                                                                            |
| P12 | When either operand of + is String, accept directly renderable non-null primitive operands and format them as interpolation would. Ordinary left-to-right evaluation still applies; this rule does not introduce general implicit conversion of numbers or booleans to String in assignments or calls.                                                                   |
| P13 | Automatically widen Char to a one-element String in assignments, function arguments, and string operations. The conversion preserves the scalar; exact Char parameter matches remain preferable in overload resolution.                                                                                                                                                  |
| P14 | String values preserve their scalar sequences without implicit Unicode normalization. String equality compares exact scalar sequences; canonically equivalent spellings may compare unequal.                                                                                                                                                                             |
| P15 | String supports <, <=, >, and >= using case-sensitive scalar lexicographic order: compare scalar numeric values left to right, with a matching shorter prefix sorting first. Locale-aware sorting is a separate topic.                                                                                                                                                   |
| P16 | Extract a substring with text.substring(start, endExclusive). Both Int bounds are required and use scalar positions, with 0 <= start <= endExclusive <= text.length. The end is excluded and equal bounds produce an empty String. Provably invalid constant bounds are compile errors; other invalid bounds are runtime errors.                                         |

A Char contains exactly one Unicode scalar; multiple-scalar sequences cannot be Char values. The scalar element model
does not choose a storage encoding or measure displayed glyphs.

## Numeric types and conversions

| ID  | Current decision                                                                                                                                                                                                                                                                        |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| N01 | `Int` and `Float` are distinct static types.                                                                                                                                                                                                                                            |
| N02 | `Int` is signed 32-bit: −2,147,483,648 through +2,147,483,647. Out-of-range constants are compile errors; arithmetic overflow is checked at runtime.                                                                                                                                    |
| N03 | `Float` uses finite binary64 with ordinary floating-point rounding. Division by zero, overflow to infinity, and invalid non-finite results are errors.                                                                                                                                  |
| N04 | Automatically widen `Int` to `Float` in assignments, function arguments, and mixed arithmetic. Every signed 32-bit integer is exactly representable in binary64.                                                                                                                        |
| N05 | `Float` to `Int` requires an explicit conversion. It truncates toward zero, then rejects a converted result outside the signed 32-bit range.                                                                                                                                            |
| N06 | `Int / Int` returns an `Int` truncated toward zero. A `Float` operand makes division produce a `Float`.                                                                                                                                                                                 |
| N07 | Integer `%` is truncation remainder: mathematically, `a % b = a − (a / b) × b`. Its sign follows the dividend when the remainder is nonzero.                                                                                                                                            |
| N08 | Support binary fairmath `%+` and `%-`; numeric rules follow N10-N12 and the source baseline below, compounds follow N09, and grouping follows N13.                                                                                                                                      |
| N09 | Add fairmath compound statements `%+=` and `%-=` alongside the value-producing binary `%+` and `%-` operators. Compound forms follow E11's target-once capture and read order.                                                                                                          |
| N10 | Both fairmath operands may be `Int` or `Float`; the rounded result is `Int`. Use binary64 intermediates and directional integer rounding, including when both operands are `Int`, rather than N06's ordinary integer division.                                                          |
| N11 | Preserve the pinned ChoiceScript interpreter's directional rounding and clamps. The base must be in `0..100` inclusive; provably invalid constants are compile errors and invalid dynamic bases are runtime errors.                                                                     |
| N12 | The fairmath change operand may be any finite numeric value, including negatives and magnitudes above 100. There is no separate percentage-range restriction; the operator and modifier sign determine direction.                                                                       |
| N13 | Require explicit parentheses when binary `%+` or `%-` combines with another binary operation or a fairmath chain. Standalone `a %+ b` and `a %- b` remain valid. Ordinary arithmetic retains E04's conventional precedence; fairmath combinations have no implicit chain associativity. |

Examples:

- Integer division: `3 / 2` is `1`; `-3 / 2` is `-1`.
- Floating division: `3 / 2.0` is `1.5`.
- Integer remainder: `-5 % 3` is `-2`.
- Explicit conversion: `3.9` becomes `3`, and `-3.9` becomes `-3`. The conversion's spelling is undecided.

### Fairmath numeric contract and source baseline

At the inspected [ChoiceScript baseline][s1], the numeric base x must be between 0 and 100 inclusive. With effective
modifier d, the interpreter uses:

- d > 0: floor (x + d * ((100 - x) / 100)), capped above at 99.
- d <= 0: ceil (x - (-d) * (x / 100)), raised below to 1.

For %+ the effective modifier is the right operand; %- negates it. The right operand has no separate percentage-range
check. These are directional clamps, not a uniform clamp to 1..99: 0 %+ 0 yields 1, 100 %+ 0 yields 100, and 100 %+ 1
yields 99. Fractional inputs use the same formulas.

N09-N12 adopt this numeric behavior for Bifoil's typed fairmath operators. Preserve the baseline's binary64 calculation
order, directional rounding, and clamps; ordinary checked Int arithmetic and integer division do not replace these
intermediates. For `%-`, negate the change in the binary64 intermediate domain, including an `Int` change of
−2,147,483,648. The rounded result is `Int`; compound statements then follow ordinary assignment conversions. Grouping
adaptation follows N13. Legacy files retain S04, including their original operand-coercion behavior.

**Grouping reference:** The [pinned ChoiceScript expression evaluator][s2] accepts a singleton or one binary operation
per group; nested operations need parentheses. The [official
introduction](https://www.choiceofgames.com/make-your-own-games/choicescript-intro/) also requires explicit grouping
when combining operators. N13 applies explicit grouping to Bifoil's binary fairmath combinations while E04 continues to
govern ordinary arithmetic.

For example, `50 %+ 10 + 20` and `50 %+ 10 %+ 20` require grouping. Valid forms include `50 %+ (10 + 20)`, `(50 %+ 10) +
20`, and `(50 %+ 10) %+ 20`; their written grouping determines which operation runs first.

## Type declarations and aliases

| ID  | Current decision                                                                                                                                                                                                                                                                                  |
|-----|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| U01 | Support transparent `typealias` declarations, for example `typealias Transform = (Int) -> Int`. An alias denotes its existing type without another runtime identity; generic aliases follow G01. Placement, scope-wide resolution, and cycle rules follow U25-U27; remaining visibility details are open.                               |
| U02 | Support user-defined data types with named, statically typed fields.                                                                                                                                                                                                                              |
| U03 | Declare fields in an indented `data class` block: `data class Character:` with declarations such as `val name: String` and `var health: Int`. Field types are explicit; `val` fields cannot be reassigned, while `var` fields can.                                                                |
| U04 | Generate a field constructor called with the data-type name, for example `Character(name = "Ada", health = 100)`. Parameters follow field declaration order and the existing positional/named/default-argument rules. Field initializers supply defaults evaluated per construction when omitted. |
| U05 | Assigning or passing a data instance shares that instance. Reassignable-field updates are visible through aliases; copying requires an explicit operation. Referenced field values retain their own semantics, and a `val` instance binding does not freeze its `var` fields.                     |
| U06 | Data-instance `==` and `!=` use structural equality over corresponding fields of compatible types. Equality is available only when every field supports it. Nominal compatibility follows U07; exact equality follows E28-E30.                                                                    |
| U07 | Data types are nominal: distinct declarations define distinct types even when their fields match. Conversion between such types requires an explicit operation. Transparent aliases under U01 do not create another type.                                                                         |
| U08 | Support enum types as closed sets of typed, named constants with stable equality and exhaustive `when` coverage. Declaration and case-reference syntax follow U12-U13. Data-bearing variants belong to the separately selected closed sum types under U14.                                        |
| U09 | Data types support member `fun` and `suspend fun` declarations, called through an instance. Existing parameter, return, overload, and suspension rules apply.                                                                                                                                     |
| U10 | Methods have an implicit receiver named `this`: write `this.health` inside a method, while `instance.heal(amount)` supplies the receiver without a declared parameter. Bare member access follows U23 and bound references follow F43-F44; remaining receiver and lookup details are open.                                |
| U11 | Data fields and methods are public by default, with explicit `public`/`private` modifiers. Private members are inaccessible from outside the data type. File-level visibility follows M08/M16.                                                                                                    |
| U12 | Declare a plain enum with `enum`, not `enum class`: `enum Mood:` followed by named cases such as `Happy` and `Sad` on separate indented lines.                                                                                                                                                    |
| U13 | Enum cases may use expected-type shorthand: when an expected enum type uniquely resolves a case, a bare name such as `Happy` is permitted; otherwise use `Mood.Happy`. Conflicts with ordinary bindings follow U24; exact import rules remain open.                                                               |
| U14 | Support closed sum types with typed payload variants, separate from plain enums. Their declaration, construction, matching, and equality follow U15-U22.                                                                                                                                          |
| U15 | Declare a closed sum type with `sealed class`, for example `sealed class Outcome:`. This does not select general class inheritance.                                                                                                                                                               |
| U16 | Declare variants inside the sum-type block with `case`, such as `case Success(value: String)` and `case Pending`. Payload types are explicit; payload-free variants are allowed.                                                                                                                  |
| U17 | Variant payload field bindings are immutable. Referenced values retain their existing mutability; fixed bindings do not recursively freeze their contents.                                                                                                                                        |
| U18 | Each variant has a distinct, nameable nominal subtype, such as `Outcome.Success`, which may widen to its enclosing sum type. Unrelated variants remain distinct.                                                                                                                                  |
| U19 | Construct payload variants with qualified names, such as `Outcome.Success("Ada")`; payload-free constants use `Outcome.Pending`. Payload constructors follow existing positional/named/default-argument rules.                                                                                    |
| U20 | `when` supports explicit `is` variant tests and payload destructuring: `case is Outcome.Success:` and `case is Outcome.Success(value):`. The marker distinguishes patterns from ordinary value expressions.                                                                                       |
| U21 | Destructured payload names create inferred immutable bindings scoped to the matched branch. For example, `case is Outcome.Success(value):` binds `value` without an explicit `val`; no-shadowing and capture rules apply.                                                                         |
| U22 | Through a compatible sum type, different variants compare unequal; matching variants compare payloads structurally when all payload types support equality. Exact comparison retains E28-E30's type and recursive equality rules.                                                                 |
| U23 | Inside a method, allow bare instance-member names such as health and heal(...) when lookup resolves them unambiguously. Explicit this.health and this.heal(...) remain available; detailed lookup interactions must respect the existing no-shadowing rules. |
| U24 | If an ordinary visible binding and an expected-type enum case are both interpretations of a bare name, report a name conflict and require qualification. Do not silently prefer either interpretation. |
| U25 | Permit transparent typealias declarations at file scope and inside ordinary lexical blocks. They introduce no new runtime type; generic aliases remain supported under G01. |
| U26 | A type-alias name is visible throughout its enclosing scope, including before its declaration, subject to alias-cycle checks. Local variable visibility remains unchanged. |
| U27 | Reject cycles through transparent alias expansion, such as typealias Nested = List<Nested>. Recursive structures must pass through nominal data or sum types; nominal recursion is not prohibited. |
| U28 | Separate private field access from generated constructor inputs. If a data class is externally constructible, outside callers may supply a private field constructor parameter but cannot read or update the private field afterward. |
| U29 | Generate explicit shallow data-instance copying with instance.copy(...): supplied fields replace values, and omitted fields retain their current values. The new instance shares referenced field values according to their ordinary semantics. Private inputs follow U28. Complete copy evaluation timing remains open. |
| U30 | After narrowing a sum value to a payload-bearing variant, allow named payload-field access, such as result.value. Payload bindings remain immutable; the existing destructuring patterns remain available. |
| U31 | Use _ as an ignored payload-pattern position, for example case is Outcome.Success(_):. It creates no binding and is exempt from the no-shadowing rule. |
| U32 | Initially limit payload patterns to one level. Bind payload values and use another when to inspect nested variants; recursive nested-pattern syntax has not been selected. |
| U33 | Comma-separated case alternatives introducing payload bindings must all bind the same names with compatible types. Infer each shared branch binding using the existing compatible-type join rules; no-shadowing and capture rules still apply. |

## User-defined generics

| ID  | Current decision                                                                                                                                                                                                                                                                  |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| G01 | Support type parameters on named functions, data classes, sealed sum types, and transparent type aliases. Built-in collection type parameters remain supported.                                                                                                                   |
| G02 | Function type parameters precede the name: `fun <T> identity(value: T) -> T = value`. Generic data and sum types use name-following parameters, such as `Box<T>`.                                                                                                                 |
| G03 | Infer generic call and constructor type arguments from supplied arguments and expected types when unambiguous. Allow explicit arguments, such as `identity<Int>(3)`, and require them when inference cannot resolve the types. Function parameter annotations remain mandatory.   |
| G04 | Unconstrained type parameters are nullable-capable: `T` may stand for `String?`. An unmarked type parameter alone does not prove non-nullness; applying `T?` follows B17's nullable flattening.                                                                                   |
| G05 | Support static nominal bounds and operation-capability requirements on type parameters, such as supported equality and stable map-key eligibility. Automatic qualification, capability names, and constraint syntax follow G09-G13; complete constraint rules remain open.                                                            |
| G06 | User-defined generic type parameters are invariant by default, with optional checked `in`/`out` declaration-site variance. Reject field or method usage that violates the declared variance. Variance uses subtyping and does not introduce value-conversion or copying adapters. |
| G07 | Support existential/star projections, such as `Box<*>`, that hide a type argument. Permit only operations the type checker proves safe from the projected argument's bounds.                                                                                                      |
| G08 | Check generic bodies at their definition against their declared constraints; invalid bodies are errors even when unused. Every instantiation must satisfy the constraints. This does not choose a code-generation strategy.                                                       |
| G09 | Automatically derive built-in generic capability qualification from the type and its fields or payloads, without a separate author opt-in. Existing structural equality remains available under the previously selected rules. |
| G10 | Name the equality capabilities Equatable and StableKey. Equatable permits supported equality operations; StableKey additionally permits set-element and map-key storage with equality that cannot change while stored. |
| G11 | Support inline generic bounds, such as fun <T: Equatable> same(...), and trailing where clauses for additional nominal bounds or capabilities. Complete declaration grammar remains to be specified. |
| G12 | Combine requirements conjunctively with repeated comma-separated constraints, for example where T: Outcome, T: Equatable. This does not introduce general intersection types. |
| G13 | A bound T: Any excludes nullable type arguments. Unconstrained T remains nullable-capable under G04. |
| G14 | Generic inference uses existing compatible-type joins for arguments constraining the same parameter: Int and Float arguments may infer Float and convert the Int argument. Do not infer container-family copies or fall back to arbitrary Any. |
| G15 | Retain runtime generic type arguments for type tests, including empty collections: value is List<Int> is permitted. Tests follow the chosen subtype rules without scalar conversions or container copying. This does not select a code-generation strategy. |

## Expressions and conditionals

| ID  | Current decision                                                                                                                                                                                                                                                                                                                                                 |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| E01 | Conditions require boolean values. Numbers, strings, and nullable values require explicit tests; they have no implicit truthiness conversion.                                                                                                                                                                                                                    |
| E02 | Logical operands must be booleans. `&&` and `\|\|` short-circuit: the right operand is skipped when the left already determines the result.                                                                                                                                                                                                                      |
| E03 | `==` and `!=` require compatible types. Unrelated types are compile errors; Int/Float comparisons use the agreed widening, and nullable values may be compared with `null`. Function-value comparisons follow F39; the separately requested `===` and `!==` operators follow E28.                                                                                |
| E04 | Use conventional precedence: multiplication/division before addition/subtraction, comparisons before `&&`, and `&&` before `\|\|`. Parentheses override grouping.                                                                                                                                                                                                |
| E05 | Explicit comparisons remain valid. Encourage integer range membership using `in` for suitable bounds checks.                                                                                                                                                                                                                                                     |
| E06 | `if` may be a statement or an expression. A value-producing form must cover every path and yield compatible branch types.                                                                                                                                                                                                                                        |
| E07 | A value-producing `if` requires an `else`. Each branch's final expression supplies its value; earlier statements may prepare the result.                                                                                                                                                                                                                         |
| E08 | Both `elif` and `else if` introduce additional conditional branches with identical meaning. Formatting preserves the author's spelling; alignment follows L07.                                                                                                                                                                                                   |
| E09 | Ordinary binary operators fully evaluate the left operand before the right; precedence determines grouping. The selected short-circuit rules still apply.                                                                                                                                                                                                        |
| E10 | For plain `=` assignments, evaluate and capture target receivers and indexes/keys once, from left to right, before evaluating and converting the right-hand side; then write. Exact bounds-check timing remains separate.                                                                                                                                        |
| E11 | Support compound assignment statements `+=`, `-=`, `*=`, `/=`, and `%=` where their operators and target types permit them. Capture and read the target once before evaluating the right-hand side; apply the existing operator, overflow, conversion, and assignment rules. Fairmath `%+=` and `%-=` follow the same target order with N09-N12's numeric rules. |
| E12 | Use Kotlin's precedence for `?:`: arithmetic, ranges, and infix range forms/modifiers bind more tightly; `in`/`!in`, comparisons, equality, `&&`, and `\|\|` bind less tightly. Repeated fallbacks group right-to-left as proposed in this batch: `a ?: (b ?: c)`. Fairmath's relative grouping remains subject to N13.                                          |
| E13 | Common-type inference for value-producing branches and function returns may use approved scalar/nullable widening and widening through immutable collection layers. Do not infer a common type by copying between mutable and immutable container families; a suitable explicit expected type may request approved copies.                                       |
| E14 | Support `when` as a multi-branch statement or expression. Value-producing branches require compatible result types under E13/E25; coverage follows E21.                                                                                                                                                                                                          |
| E15 | Support subject-based `when value:` and subjectless `when:`, each with indented branches. Subject-based cases compare against one evaluated value; subjectless cases test Boolean conditions.                                                                                                                                                                    |
| E16 | Use `case` with colon branch headers, such as `case 1:` or `case condition:`, followed by an indented body. The fallback header is `else:`. Branch results follow E22; fallback placement follows E33.                                                                                                                                               |
| E17 | Subject-based cases support compatible-type value equality, null for nullable subjects, and `in`/`!in` range or collection tests. Sum-type variant patterns follow U20-U21.                                                                                                                                                                                      |
| E18 | Allow comma-separated alternatives in one `when` branch, including multiple value cases or multiple Boolean conditions in a subjectless form. Test alternatives left to right and stop at the first match.                                                                                                                                                       |
| E19 | Evaluate a `when` subject once, then test branches in source order until a match and execute only that branch. Subjects and case-test expressions follow the enclosing context's suspension permissions; preserve completed evaluation when resuming. Ordinary non-suspending state changes remain allowed.                                                      |
| E20 | Allow overlapping `when` matches; selection follows E19. Provably unreachable later branches may receive warnings.                                                                                                                                                                                                                                               |
| E21 | A value-producing `when` may omit its fallback when coverage of every possible subject is proven, such as true and false for Boolean; otherwise require a fallback. Statement forms need not produce a value and follow E23 when unmatched. Exact coverage analysis remains to be specified.                                                                     |
| E22 | A value-producing `when` branch supplies its result through its final expression, matching value-producing `if` branches. Earlier statements may prepare the result; early control transfers follow their own rules.                                                                                                                                             |
| E23 | If a statement-form `when` has no matching branch or `else`, execute no branch and continue normally.                                                                                                                                                                                                                                                            |
| E24 | A subject-based `when` may declare an immutable subject binding: `when val value = expression:`. The binding is visible in case tests and branch bodies but unavailable after the `when`. Existing no-shadowing and capture-lifetime rules apply.                                                                                                                |
| E25 | Expose the bottom type `Nothing`, which has no values and is compatible with every result type. Paths that never produce a value do not force incompatible branch-result types. This does not introduce exceptions or additional control-transfer operations.                                                                                                    |
| E26 | Existing `return`, `break`, `continue`, and `goto` transfers may appear in expression positions, such as `val name = maybeName ?: return`. Each transfer must remain valid in its function, loop, or story context; a transferring path produces no value and has type `Nothing`.                                                                                |
| E27 | Plain `=` assignment is a statement, not a value-producing expression. It changes a binding or container element under E10's target-first evaluation order. Compound updates retain E11's statement forms.                                                                                                                                                       |
| E28 | Support `===` and `!==` as exact type-and-value equality operators alongside `==` and `!=`. Compare without widening: different non-null value types are unequal, so `3 === 3.0` is false. Comparable values of the same type use value equality; `!==` negates that comparison. Nullable and composite comparison follow E29-E30.                               |
| E29 | Exact equality compares contained values or null. Two nulls are equal regardless of their nullable annotations; one null is unequal to a present value. A present `Int?` containing 3 is exactly equal to `Int` 3. Conversions performed before comparison still determine the stored value's type.                                                              |
| E30 | Collections, data instances, and eligible sum values support typed structural exact equality. Collection families/type arguments or nominal value types must match; recursively compare supported contents without widening or copying. Sum-specific eligibility follows U22.                                                                                    |
| E31 | If an operand has static type Any or Any? and its concrete equality capability is unknown, require narrowing or other static proof of equality eligibility before comparison. Existing null comparisons remain available; this does not introduce runtime failure-based equality dispatch. |
| E32 | Support Boolean when pattern guards, such as case is Outcome.Success(value) if value != "":. Payload names are available to the guard. Evaluate it once after the pattern matches, under the enclosing suspension permissions; a false guard continues to later cases. |
| E33 | A when may have at most one else: fallback, which must follow all case branches. Choice-fallback placement remains a separate matter. |
| E34 | Ordinary and exact structural equality handle eligible cyclic data or collection graphs without infinite recursion. Track pairs being compared so revisiting a pair terminates that recursive step. Shared-reference layout does not determine equality; the ordinary and exact type rules remain distinct. |
| E35 | Initially fail fast on checked runtime failures, including overflow, invalid indexes, and failed checked casts: stop the story and report the original Bifoil source location. Catchable language-level exceptions are deferred. Compilation and budget errors follow S15. |

Precedence reference for E12: [Kotlin's expression
grammar](https://kotlinlang.org/spec/syntax-and-grammar.html#expressions).

A bounds-comparison rewrite using `in` must preserve R04's invalid-range behavior: a false comparison must not become a
range-construction error.

## Collections

| ID  | Current decision                                                                                                                                                                                                                                                                                                                                            |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| D01 | Provide `List<T>`, `Set<T>`, and `Map<K, V>` as the initial collection families.                                                                                                                                                                                                                                                                            |
| D02 | Use separate immutable and mutable container families: List<T>, Set<T>, and Map<K, V> cannot have their contents changed through any alias; MutableList<T>, MutableSet<T>, and MutableMap<K, V> permit container changes. Element values retain their own mutability rules.                                                                                 |
| D03 | Support collection literals: `[a, b]` for lists, `{a, b}` for sets, and `{key: value}` for maps. Contextual typing and inference follow D10-D11; empty literals follow D17. Factory APIs remain separate.                                                                                                                                                   |
| D04 | When no expected type supplies context, collection construction infers the immutable List/Set/Map family by default. Mutable construction uses the explicit prefix in D09 or expected-type guidance in D10.                                                                                                                                                 |
| D05 | Same-family assignment and argument passing of mutable collection values share the same container, so mutations are visible through aliases. Cross-family copying follows D21. These rules concern container contents rather than `val`/`var` binding reassignment.                                                                                         |
| D06 | List indexing uses zero-based, nonnegative indexes, matching String indexing. Provably invalid constant indexes are compile errors; other invalid indexes are runtime errors. Negative indexes are invalid.                                                                                                                                                 |
| D07 | Map lookup with `map[key]` returns `V?`. A missing key yields null, and a stored null also yields null. Map key presence is tested with `in` or `!in` under D19.                                                                                                                                                                                            |
| D08 | Equality and inequality for compatible collection values are structural. Lists compare elements in order; sets compare members and maps compare entries independent of iteration order. Element, key, and value equality must be supported. Remaining type-compatibility details are open; cyclic comparison follows E34.                                       |
| D09 | Explicit mutable collection construction uses the mutable literal prefix, for example mutable [1, 2], mutable {"a", "b"}, and mutable {"gold": 3}.                                                                                                                                                                                                          |
| D10 | Expected types guide collection literal element/key/value types and mutability. An annotation or parameter type may request mutable construction without a mutable prefix, for example val items: MutableList<Int> = [1, 2]. The no-context default remains immutable under D04.                                                                            |
| D11 | Collection literals infer compatible-type joins using existing scalar widening: `[1, 2.5]` yields `List<Float>`, and `['a', "b"]` yields `List<String>`. Mixing `T` with null yields `T?`. Unrelated types require a suitable explicit expected type or are errors. Empty or all-null collections require an expected type; empty set/map forms follow D17. |
| D12 | Set elements and map keys must have statically stable equality that cannot change while stored. Accept known-stable types; immutable containers qualify only when their contained values also qualify. Reject mutable composites. Exact eligibility analysis and hashing machinery remain open.                                                             |
| D13 | Sets and maps preserve first-insertion order for iteration. Replacing a map value retains its key's position; removing and reinserting moves it to the end. Lists retain positional order.                                                                                                                                                                  |
| D14 | Set construction coalesces equal duplicate members. Map construction rejects duplicate keys: compile errors when provable and runtime errors otherwise. Literal evaluation and dynamic key-check timing follow D29.                                                                                                                                         |
| D15 | For loops over lists and sets yield elements; loops over maps yield entry values with .key and .value. The existing fresh immutable iteration-binding rule applies. Entry type naming and destructuring remain separate decisions.                                                                                                                          |
| D16 | For loops snapshot elements or map entries when traversal starts, including traversal of mutable collections. Mutating the original container does not change that traversal. Referenced element values retain their own semantics; the snapshot is not a recursive freeze or deep copy.                                                                    |
| D17 | Empty literals use context: `[]` is a list; `{}` is a set or map according to its expected type. Empty collections require sufficient expected element/key/value types; insufficient context is a compile error.                                                                                                                                            |
| D18 | Use the `size` property for collection element or entry counts, with an `Int` result. `String` retains its `length` property.                                                                                                                                                                                                                               |
| D19 | Use `in` and `!in` for collection membership. Lists and sets test elements; maps test keys, including keys whose stored value is null. `!in` negates the test.                                                                                                                                                                                              |
| D20 | Mutable collections support indexed assignment plus methods: `items[i] = value` replaces a list element, and `mapping[key] = value` inserts or replaces a map entry. Add/remove operations use methods; exact method names and results remain open.                                                                                                         |
| D21 | Assignments and arguments may implicitly convert between corresponding immutable and mutable collection families by copying container contents into the requested family. The resulting container is independent; referenced element values retain their own semantics rather than being recursively frozen or copied.                                      |
| D22 | Lift approved lossless scalar widening through immutable `List`/`Set`/`Map` element, key, or value types, converting contents as needed, for example `List<Int>` to `List<Float>`. Same-family mutable collection type arguments must match exactly. Combining family copies with widening follows D25; recursive immutable lifting follows D28.            |
| D23 | A variadic parameter exposes a fresh immutable `List<T>` of its declared element type on each call, for example `vararg values: Int` yields `List<Int>`. Referenced elements retain their own semantics.                                                                                                                                                    |
| D24 | Use the star prefix to spread `List<T>` or `MutableList<T>` elements into typed variadic arguments, for example `total(1, *numbers)`. Multiple groups and source-position expansion follow A07; other iterable families remain separate.                                                                                                                    |
| D25 | A container-family copy may combine with approved scalar widening: `MutableList<Int>` to `List<Float>` and `List<Int>` to `MutableList<Float>` produce independent containers. Same-family `MutableList<Int>` to `MutableList<Float>` remains forbidden; implicit copy chains must not bypass that invariance.                                              |
| D26 | Argument conversion and snapshot timing follow A04. An earlier requested snapshot completes before a later argument expression can mutate its source.                                                                                                                                                                                                       |
| D27 | Rank overload argument conversions as exact, widening, container-family copying, then copying plus widening. These are semantic categories, not allocation counts. Candidate dominance and tie-breakers follow F28-F29.                                                                                                                                     |
| D28 | Approved widening recurses through nested immutable containers, for example `List<List<Int>>` to `List<List<Float>>`. Stop at mutable contained types, whose type arguments require exact matching. This does not authorize recursively copying or freezing mutable element objects.                                                                        |
| D29 | Collection literals evaluate elements or entries from left to right. For each map entry, evaluate its key, reject a dynamically duplicated key before evaluating its value, then proceed to the next entry. Provable duplicate map keys remain compile errors.                                                                                              |
| D30 | Immutable List and Set element types and Map value types are covariant through genuine subtype relationships, without copying; Map keys remain invariant. For example, List<Outcome.Success> may satisfy List<Outcome>. Scalar conversions remain separate, and mutable collection type arguments remain invariant. |

## Integer ranges and membership

| ID  | Current decision                                                                                                                                                             |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| R01 | `a..b` is an ascending inclusive integer range.                                                                                                                              |
| R02 | `a..<b` is an ascending half-open integer range: include `a`, exclude `b`.                                                                                                   |
| R03 | Ranges are immutable first-class values. They can be stored in bindings, passed to functions, and reused in membership tests. A `var` may be rebound to another range value. |
| R04 | Invalid or empty ascending ranges are errors. Reject constant cases at compile time and dynamically computed cases at runtime. Examples include `5..1` and `5..<5`.          |
| R05 | `a downTo b` explicitly creates an inclusive descending range. The ascending forms retain their direction.                                                                   |
| R06 | `step n` selects every nth value. The step must be a positive `Int`; direction comes from the range form.                                                                    |
| R07 | Use Kotlin's implementation as the reference for stepped integer progression membership. Membership follows the values produced by the progression.                          |

Examples:

- `1..9 step 2` produces `1, 3, 5, 7, 9`.
- `9 downTo 1 step 2` produces `9, 7, 5, 3, 1`.
- `3 in (1..9 step 2)` is true; `4 in (1..9 step 2)` is false.
- Following the requested Kotlin reference, `1..8 step 2` ends at `7`; an unreachable bound is not added to the
  sequence.

Kotlin's implementation was requested in response to the stepped-membership question. This does not replace Bifoil's
earlier decision to report invalid/empty ascending ranges as errors.

The Kotlin source inspected during the discussion uses an iterable search for stepped progressions. Literal copying
therefore brings linear searches and possible search-index overflow on very large progressions. A different
constant-time implementation or a changed failure contract has not been selected. See [Kotlin's progression source][s3],
[its membership/search source][s4], and [range/progression documentation](https://kotlinlang.org/docs/ranges.html).

## Loops and jumps

| ID  | Current decision                                                                                                                                                           |
|-----|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| C01 | `for i in range:` creates a fresh, inferred immutable binding each iteration, scoped to the loop body.                                                                     |
| C02 | `break` exits the innermost loop; `continue` skips to its next iteration.                                                                                                  |
| C03 | Loops may have optional labels. A targeted jump must name an enclosing loop in the same function; invalid targets are compile errors.                                      |
| C04 | Label a loop using `outer@ for ...:`; target it with `break@outer` or `continue@outer`.                                                                                    |
| C05 | Support both `while` and `do/while`. A `while` tests before the body; a `do/while` tests after it and runs the body at least once.                                         |
| C06 | Write `do:` with an indented body, followed by `while condition` aligned with `do`. The closing `while` has no colon.                                                      |
| C07 | Declarations directly in a `do` body are visible to its closing condition, but unavailable after the loop. Declarations inside nested blocks retain those narrower scopes. |
| C08 | Every variable read by the closing condition must be initialized on every path reaching it, including paths through `continue`.                                            |

## Functions, parameters, and calls

| ID  | Current decision                                                                                                                                                                                                                                                                                                                                                                                |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| F01 | Declare functions using `fun` exclusively.                                                                                                                                                                                                                                                                                                                                                      |
| F02 | Parameters require type annotations. Infer return types when unambiguous; require annotations when inference cannot resolve them.                                                                                                                                                                                                                                                               |
| F03 | Explicit return annotations use `->`: `fun double(value: Int) -> Int:`. The final colon opens a block body.                                                                                                                                                                                                                                                                                     |
| F04 | Named function block bodies use explicit return value. Value-returning named functions must return on every reachable path. Anonymous function bodies follow F27.                                                                                                                                                                                                                               |
| F05 | Support expression bodies: `fun double(value: Int) = value * 2`. The expression supplies the returned value; return annotations may still use `->`.                                                                                                                                                                                                                                             |
| F06 | `Unit` is a regular type with one value. Infer it for functions that return no value. Such functions may end naturally or use bare `return`. An explicit annotation is `-> Unit`.                                                                                                                                                                                                               |
| F07 | Parameters are immutable by default. An optional `var` modifier permits reassignment of a parameter binding inside the function.                                                                                                                                                                                                                                                                |
| F08 | Each parameter has its own local binding. Reassigning a `var` parameter does not update the caller's binding. Ordinary argument expressions are allowed.                                                                                                                                                                                                                                        |
| F09 | Parameters may declare default argument values using `=`, while retaining required type annotations. Calls omitting an argument use its default.                                                                                                                                                                                                                                                |
| F10 | For parameters permitted to have defaults, evaluate an omitted default at each call only when that argument is omitted. Variadic parameters follow F33 instead.                                                                                                                                                                                                                                 |
| F11 | Defaults may reference already-resolved earlier parameters and bindings visible where the function is declared. Later parameters are unavailable.                                                                                                                                                                                                                                               |
| F12 | Defaulted parameters may appear anywhere, including before required ones. Positionals bind in declaration order; named arguments can omit earlier defaults.                                                                                                                                                                                                                                     |
| F13 | Support self-recursion and mutual recursion, with fresh parameter and local bindings for every call. Return typing follows F02.                                                                                                                                                                                                                                                                 |
| F14 | Function names are visible throughout their enclosing scope. Calls may precede declarations in that scope, so declaration order does not restrict ordinary calls or mutual recursion.                                                                                                                                                                                                           |
| F15 | Allow fun declarations at file scope and inside functions or ordinary code blocks. Local function names follow the scope of their enclosing block and the scope-wide visibility rule in F14.                                                                                                                                                                                                    |
| F16 | Local function bodies may read bindings from enclosing lexical scopes that are visible where the function is declared. Reads of enclosing var bindings follow F17, and reassignment follows F18.                                                                                                                                                                                                |
| F17 | Each read of an enclosing var observes that lexical binding's current value at the time of the read, including reassignments since the local function was declared.                                                                                                                                                                                                                             |
| F18 | Local functions may reassign visible enclosing var bindings. Assignment updates that same enclosing binding, subject to its type and ordinary assignment rules.                                                                                                                                                                                                                                 |
| F19 | A local function may be declared before an enclosing binding it reads has been initialized. Every call that could read the binding requires compile-time proof of initialization; unprovable cases are compile errors.                                                                                                                                                                          |
| F20 | Functions are first-class, statically typed values. They may be stored in variables, passed as arguments, and returned, including references to local functions.                                                                                                                                                                                                                                |
| F21 | Escaping functions retain their captured lexical bindings as long as needed. Functions capturing the same var binding share its current state; separate enclosing invocations still have their own bindings.                                                                                                                                                                                    |
| F22 | Function types use arrow notation, such as (Int, Int) -> Int, with an explicit return type. Unit-returning function types spell (Int) -> Unit or () -> Unit. Omission of -> Unit applies to function declarations.                                                                                                                                                                              |
| F23 | Functions in the same scope may form overload sets distinguished by parameter types or counts. Ambiguous calls are compile errors, and return types alone cannot distinguish overloads. Nested shadowing remains prohibited.                                                                                                                                                                    |
| F24 | Support typed variadic parameters accepting zero or more arguments of one declared element type. Spelling follows F30 and placement follows F31; the fresh immutable `List<T>` representation follows D23.                                                                                                                                                                                      |
| F25 | Support anonymous function expressions without a declared name, with mandatory parameter annotations. Arrow syntax follows F26/F40, final-expression returns follow F27/F34, and variadic parameters follow F41.                                                                                                                                                                                |
| F26 | Anonymous functions use `(x: Int) => x + 1`, or `(x: Int) =>:` with an indented block. Optional return annotations follow F40.                                                                                                                                                                                                                                                                  |
| F27 | Anonymous expression bodies and block bodies return their final expression, with contextual Unit-result discarding under F34. An early return exits the anonymous function itself. Named function block bodies retain F04's explicit-return rule.                                                                                                                                               |
| F28 | Overload resolution compares each supplied argument's conversion rank under D27. A candidate wins on argument types only if it is no worse on every supplied argument and better on at least one. The selected scalar widenings and collection conversions participate in these ranks.                                                                                                          |
| F29 | For overloads otherwise equally good on supplied arguments, prefer nonvariadic candidates, then candidates requiring fewer omitted defaults. Remaining generic/nongeneric ties follow F42; other ties are compile errors.                                                                                                                                                                                                                 |
| F30 | Declare a typed variadic parameter with the vararg modifier, such as vararg values: Int. The annotation denotes the element type.                                                                                                                                                                                                                                                               |
| F31 | Allow at most one variadic parameter per function signature, always as the last parameter.                                                                                                                                                                                                                                                                                                      |
| F32 | Retain variadic function-value types, such as `(vararg Int) -> Unit`, with zero-or-more individual or spread arguments. Other function-value call rules follow A05.                                                                                                                                                                                                                             |
| F33 | Variadic parameters have no explicit default expressions; omission supplies an empty group under D23. Use an ordinary `List` parameter for a custom default.                                                                                                                                                                                                                                    |
| F34 | When constructing an anonymous function with an expected return type of `Unit`, evaluate its final expression, discard any non-Unit result, and return `Unit`. Ordinary inferred functions retain their existing return rules. This selects contextual anonymous-function construction, not a conversion of existing function values.                                                           |
| F35 | Take a named function reference with `::`, for example `val transform = ::double`. Its calling interface follows A05/F32.                                                                                                                                                                                                                                                                       |
| F36 | Resolve an overloaded function reference using an expected function type from an annotation or parameter context. Select a unique compatible overload; unresolved or ambiguous references are compile errors.                                                                                                                                                                                   |
| F37 | For function types with the same parameter count and variadic shape, allow safe variance through subtype relationships: broader parameter types and narrower return types may satisfy the expected type. For example, `(Int?) -> String` may satisfy `(Int) -> String?`. Numeric widening and container copying are separate conversions; T21's ordinary-to-suspend widening remains available. |
| F38 | Do not automatically create function adapters when signature compatibility would require scalar value conversions or container copies. Write an anonymous function to perform those conversions explicitly. Ordinary argument conversions when calling a function remain available.                                                                                                             |
| F39 | Function values do not support `==` or `!=` comparisons except nullable comparisons with `null`; other such comparisons are compile errors. Eligibility for the newly requested exact-equality operators remains subject to E28.                                                                                                                                                                |
| F40 | Anonymous functions may declare an explicit return type with `->` between their parameters and `=>`: `(x: Int) -> Float => x * 2`, or `(x: Int) -> Float =>:` followed by an indented block. Parameter annotations remain mandatory.                                                                                                                                                            |
| F41 | Anonymous functions may declare a variadic parameter, such as `(vararg values: Int) => values.size`, and infer a variadic function type. Existing last-parameter, fresh immutable `List<T>`, and variadic function-value call rules apply.                                                                                                                                                      |
| F42 | After the existing conversion, variadic, and default-argument tie-breakers, prefer a nongeneric overload over an otherwise tied generic overload. Other unresolved ties are compile errors. |
| F43 | Take a bound instance-method reference with receiver::method, for example val heal = character::heal. Its resulting function value already has the receiver bound and follows the existing function-value calling interface. |
| F44 | Evaluate and capture a method-reference receiver once when the reference is created. Later reassignment of the original receiver binding does not retarget that reference. Anonymous functions reading captured bindings retain F17. |
| A01 | Calls support both positional arguments and named arguments written `name = value`.                                                                                                                                                                                                                                                                                                             |
| A02 | Unknown parameter names and duplicate argument bindings are compile errors. Arguments retain static type checking.                                                                                                                                                                                                                                                                              |
| A03 | In mixed calls, positional arguments precede named arguments. Named arguments may appear in any order.                                                                                                                                                                                                                                                                                          |
| A04 | Evaluate supplied arguments left to right, completing each implicit conversion before evaluating the next argument. Then evaluate omitted defaults in parameter declaration order.                                                                                                                                                                                                              |
| A05 | Calls through function values require explicit positional arguments for fixed parameters and expose no parameter names or defaults. Variadic function types retain F32's zero-or-more argument interface. Declared function-name calls retain their named/default interfaces.                                                                                                                   |
| A06 | Evaluate and capture a call's callable expression or method receiver before supplied arguments. Then process arguments and omitted defaults under A04 and D26.                                                                                                                                                                                                                                  |
| A07 | Allow multiple spread groups interleaved with individual variadic arguments, for example `gather(1, *first, 2, *second)`. Expand groups at their source position under the selected argument order; spreads supply the variadic portion and preserve that element order.                                                                                                                        |
| A08 | A declared function name accepts a named variadic group as a list value, for example `gather(values = numbers)`, with applicable copying/widening rules and a fresh immutable `List<T>` for the callee. The same variadic parameter cannot be supplied both positionally and by name.                                                                                                           |

## Narrative and story control

| ID  | Current decision                                                                                                                                                                                                                                                                                      |
|-----|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| T01 | Introduce explicit unquoted narrative blocks with prose: followed by indented narrative.                                                                                                                                                                                                              |
| T02 | Prose interpolation uses ${expression}, such as Your score is ${score}. Literal-delimiter escaping follows T11.                                                                                                                                                                                       |
| T03 | Prose interpolation permits non-suspending value expressions, including arithmetic and ordinary function calls, that produce a renderable value. Directly renderable types follow P08; exact formatting remains open.                                                                                 |
| T04 | After removing structural block indentation, single source newlines join text within a paragraph and blank lines separate paragraphs. An explicit line-break form remains open.                                                                                                                       |
| T05 | Support executable directives inside prose. Their prefix and nested-body rules follow T09-T10.                                                                                                                                                                                                        |
| T06 | A choice uses an outer choice: block containing explicit option headers, such as option "Open the door":, each followed by its indented body.                                                                                                                                                         |
| T07 | After the selected option body finishes normally, execution continues after the choice. Existing return, break, and other control transfers still apply.                                                                                                                                              |
| T08 | Functions that may wait for player interaction carry an explicit suspension effect in their types; calls require a suspension-capable context.                                                                                                                                                        |
| T09 | A line-leading @ after indentation introduces an executable directive inside prose. The text after the prefix uses Bifoil syntax, such as @if hasKey: or @score = score + 1.                                                                                                                          |
| T10 | Conditional and loop directive bodies remain in prose mode by default. Further executable statements and branch headers use the @ prefix.                                                                                                                                                             |
| T11 | Prose uses backslash escapes: `\${` produces literal `${`, `\@` makes a directive introducer literal, and `\\` produces one backslash. Other escape forms remain open.                                                                                                                                |
| T12 | Quoted option labels support ${expression} interpolation under the same non-suspending, renderable-value rules as prose.                                                                                                                                                                              |
| T13 | Conditional option headers may use if for visibility and enabledIf for selection availability, as in option "Open" if visible enabledIf allowed:. False if hides the option; false enabledIf displays it disabled. Conditions require booleans.                                                       |
| T14 | Prepare each choice once, processing options in source order. Evaluate visibility first, then the enabled condition and label for visible options. Hidden options skip enabled-condition and label evaluation. Retain these results until selection.                                                  |
| T15 | The suspend modifier marks suspension-capable named functions, anonymous functions, and function types: suspend fun ask() -> Int:, suspend () -> Int, and a suspend-prefixed lambda.                                                                                                                  |
| T16 | Call suspending functions with ordinary syntax, such as `val answer = ask()`, in a context permitted by T08. No `await` marker is required.                                                                                                                                                           |
| T17 | A choice may contain an else: fallback for when no option is selectable. Without a fallback, provably empty choices are compile errors and dynamically empty choices are runtime errors.                                                                                                              |
| T18 | Options are reusable by default. An option with the once modifier, such as option "Ask about the map" once:, is consumed on selection and hidden on subsequent visits.                                                                                                                                |
| T19 | Once-option history is story-wide per source option site for the playthrough. Later scene visits and function calls share that site's consumed state.                                                                                                                                                 |
| T20 | New Bifoil scene bodies are automatically allowed to suspend: they may present choices and call suspend functions directly. Ordinary function bodies still require the suspend modifier.                                                                                                              |
| T21 | An ordinary function value may satisfy a suspend function type with otherwise identical parameter and return types. A suspend function value cannot satisfy an ordinary function type.                                                                                                                |
| T22 | Suspending calls may appear inside larger expressions and function arguments. Preserve the selected evaluation order and retain completed operands, arguments, and partial evaluation across suspension without repeating completed work. Prose and option-label interpolation remain non-suspending. |
| T23 | Choice-preparation expressions for visibility, enabling, and label interpolation must not suspend. Ordinary state changes and other non-suspending effects are permitted under the selected preparation order.                                                                                        |
| T24 | At supported save points, retain full suspended state: active calls, locals, captures, computed temporaries, active traversal state, choice snapshots, and option history. Resume without replay. Initial checkpoint and build-compatibility policies follow T25-T26; save-format details remain open.                                    |
| T25 | Initially support saving at fully prepared player-input waits. Every supported save point preserves the full suspended-state, no-replay contract under T24. |
| T26 | Initial saves restore only against the same compiled build. Reject incompatible saves clearly. Compatibility across game updates and migrations are outside the initial save contract. |

## Scenes, modules, and shared state

| ID  | Current decision                                                                                                                                                                                                                                                            |
|-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| M01 | Organize new source into scene files and library modules. A scene file has one executable story body plus declarations; library modules contain reusable declarations and non-suspending initialization.                                                                    |
| M02 | Scene destinations are typed first-class references that can be stored, passed, and selected with checked input signatures. Ordinary strings are not scene destinations.                                                                                                    |
| M03 | Scene entries may declare typed input parameters local to that visit. Scene entry and calls reuse the existing argument and default-argument rules.                                                                                                                         |
| M04 | Support returning scene calls and one-way scene transfers. A call runs a fresh visit and returns control with Unit; a transfer replaces the current story position. Value-returning routines use suspend functions. Operation syntax and transfer unwinding follow M12-M13. |
| M05 | A scene body may finish naturally. Return to its scene caller if one exists; otherwise finish the story.                                                                                                                                                                    |
| M06 | Ordinary scene-body `val`/`var` declarations are local to that visit. Persistent shared storage follows M14.                                                                                                                                                                |
| M07 | Initialize shared story state once before the first scene of a new playthrough, using non-suspending initializers. Loading restores saved state without replaying initializers. Dependency ordering and cycle policy follow M15.                                            |
| M08 | Top-level symbols are private by default. Export intended interfaces and explicitly import the symbols a file uses. Import/export spelling follows M16; detailed resolution and conflict rules remain open.                                                                 |
| M09 | A scene file declares its entry with a named header such as scene forest(danger: Int = 0): and an indented body. The header supplies the logical scene name; helpers and shared declarations remain outside that body.                                                      |
| M10 | Scene references use input types: `Scene<Int, Float>`, or bare `Scene` for zero inputs. Reference-valued targets require every input explicitly and positionally; named targets retain named/default arguments.                                                             |
| M11 | Obtain a named scene reference with the explicit `::` prefix, for example `val destination = ::forest`. Named function references use the same prefix under F35.                                                                                                            |
| M12 | Use `goto` for a transfer and `visit` for a returning scene call, such as `goto forest(danger = 3)` or `visit forest(danger = 3)`. Input and return rules follow M03-M04/M10.                                                                                               |
| M13 | Transfers are permitted only in scene bodies or suspend functions. A transfer replaces the current scene visit and abandons its active function calls, while retaining earlier scene-call callers. If A visits B and B transfers to C, C's natural completion returns to A. |
| M14 | At file/module scope, declare persistent story values with shared val or shared var, for example shared var gold: Int = 0. Allowing shared declarations inside functions or scene bodies requires a separate placement decision.                                            |
| M15 | Shared names resolve throughout their module, including forward references. Initialize dependencies first, use stable module/source order for independent values, and reject cycles requiring uninitialized values. Local-variable visibility retains B10.                  |
| M16 | Use dotted explicit imports with optional `as` aliases, such as `import story.stats.gold as coins`; prefix exported declarations with `export`.                                                                                                                             |
| M17 | Place new Bifoil sources under src/ and derive dotted module names from directory and file paths. Existing explicit import and export rules remain in force. |
| M18 | Use bifoil.toml as the project manifest and name the entry scene there. Exact manifest keys and schema remain to be specified. |
| M19 | The user prefers .bfl as the new-source extension over the earlier .bifoil default. Use it as the preferred candidate in the provisional design with the documented extension conflicts below. |

M15 clarification, 2026-10-25: finish every dependency before beginning the dependent initializer. For shared val a =
record() + b, b must finish initializing before record() runs. Discover dependencies conservatively through branches,
calls, and default expressions, and reject dependency cycles conservatively. This replaces read-triggered initialization
as an implementation option.

## Combined illustrative sketches

These examples use four spaces per level for readability. They are original design sketches, not compiled or verified
conformance fixtures. Their layout does not select a default formatter indentation style.

### Explicit return and a locally reassignable parameter

```
fun increment(var amount: Int) -> Int:
    amount = amount + 1
    return amount

var score = 10
val nextScore = increment(amount = score)
```

Under the selected binding rules, `nextScore` is `11` and the caller's `score` is `10`.

### Delayed initialization

```
fun chooseReward(score: Int) -> Int:
    val result: Int
    if score > 0:
        result = 10
    else:
        result = 0
    return result
```

Each reachable branch initializes the same local `val` exactly once before its read.

### Conditional expression and continuation after assignment

```
val score = 7
val sign =
    if score < 0:
        -1
    elif score == 0:
        0
    else:
        1
```

The middle branch may equivalently use `else if score == 0:`. A formatter preserves that spelling.

### Scope of a post-test condition

```
var attempts = 0

do:
    attempts = attempts + 1
    val again = attempts < 3
while again
```

The closing condition can read `again`; code following the loop cannot.

### A labeled range loop

```
outer@ for i in 1..9 step 2:
    for j in 1..3:
        if i == j:
            break@outer
```

An outer-targeted continuation would use `continue@outer`. Each iteration binding is immutable, and existing visible
bindings named `i` or `j` would make those declarations invalid under the no-shadowing rule.

### Prose paragraphs and a structured choice

```
val score = 12
prose:
    Your score is ${score}.
    The corridor is quiet.

    A door stands at its end.

choice:
    option "Open the door":
        prose:
            You turn the handle.
    option "Walk away":
        prose:
            You leave the door untouched.

prose:
    Your next step awaits.
```

The first two narrative lines form one paragraph. After either selected option finishes normally, execution reaches the
final prose block. This sketch belongs in story code allowed to suspend under T08/T20. Embedded directives are
illustrated below.

### Directives and a suspending function

```
suspend fun askToEnter(keyCount: Int) -> Int:
    prose:
        @if keyCount > 0:
            You feel the key in your pocket.
        @else:
            Your pockets are empty.

    choice:
        option "Enter (${keyCount} keys)" enabledIf keyCount > 0:
            return 1
        option "Stay outside":
            return 0
```

The directive branches contain prose by default. The Enter option is visible but disabled when no key is available; the
Stay outside option remains selectable. A caller in a suspension-capable context may write `val answer = askToEnter(1)`.
Scene contexts follow T20 and entry headers follow M09; saved execution-state representation remains open.

### A once option and an empty-choice fallback

```
choice:
    option "Hear the old tale" once:
        prose:
            The ferryman tells his story.
    else:
        prose:
            The ferryman has nothing more to add.
```

The option is reusable only until it is selected once. A later visit to the same option site during this playthrough
uses the fallback when no other selectable option exists. Save/load must retain the consumed history rather than replay
the selected option body. This example does not establish stable option identifiers across source edits.

### Typed strings, characters, and interpolation

```
val name: String = "Ada"
val initial: Char = name[0]
val active: Boolean = true
val greeting = "Hello, ${name}."

prose:
    ${greeting}
    Your initial is ${initial}.
```

The index yields the first Unicode scalar as Char. The ordinary string template and the prose interpolations use
renderable non-null primitive values. Length and concatenation now follow P11-P12.

### Typed collection literals and nullable lookup

```
val rewards: List<Int> = [1, 2, 3]
val badges: Set<String> = {"bronze", "silver"}
val rewardNames: Map<Int, String> = {1: "coin", 2: "key"}
val firstReward = rewards[0]
val missingName: String? = rewardNames[99]
val sameRewards = rewards == [1, 2, 3]
```

These literals create immutable containers. The list index is zero-based, the absent map key yields null, and matching
list contents compare structurally. Mutable construction and collection iteration follow D09-D16.

### Mutable construction and map entry iteration

```
val inventory = mutable ["key", "rope"]
val inventoryAlias = inventory
val scores: MutableMap<String, Int> = {"gold": 3}

for entry in scores:
    prose:
        ${entry.key}: ${entry.value}.
```

The inventory bindings share one mutable container. The scores annotation requests mutable construction without a
prefix. Map iteration snapshots entries in insertion order; each entry exposes its key and value. Indexed mutation
syntax follows D20; add/remove methods and the entry type's name remain pending.

### Implicit collection copies and immutable widening

```
val source = mutable [1, 2]
val frozen: List<Int> = source
val wider: List<Float> = frozen
val editable: MutableList<Int> = frozen

source[0] = 9
editable[1] = 8
```

The copied containers are independent: frozen retains [1, 2], wider contains [1.0, 2.0], source contains [9, 2], and
editable contains [1, 8]. Combining family copying with scalar widening now follows D25, and recursive immutable
widening follows D28.

### Variadic values, named groups, and compound assignment

```
fun total(vararg values: Int) -> Int:
    var result = 0
    for value in values:
        result += value
    return result

val first = [2, 3]
val second = [5]
val consumer: (vararg Int) -> Int = ::total
val combined = consumer(1, *first, 4, *second)
val named = total(values = first)
val empty = consumer()
```

The calls produce 15, 5, and 0 respectively. Function-value calls retain variadic arguments without names or defaults.
Each invocation receives a fresh immutable List<Int>, and the compound update reads its target once.

### Scene references, visits, and transfers

A scene file may export this entry alongside shared declarations:

```
export shared var gold: Int = 0

export scene forest(danger: Int = 0):
    prose:
        Danger level: ${danger}.
```

A caller that imports the scene may use both named and reference-valued targets:

```
import story.woods.forest

scene crossroads():
    val destination: Scene<Int> = ::forest
    visit destination(3)
    goto forest(danger = 1)
```

The visit returns before the transfer executes. The transfer replaces the crossroads visit while preserving any earlier
scene caller. This sketch does not decide filesystem-to-module mapping or general modifier ordering.

## Revisions and corrections

Use the current decisions above when older discussion differs.

| Earlier choice or interpretation                                           | Current status                                                                                                                                        |
|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Int bounded by JavaScript's safe-integer interval, ±9,007,199,254,740,991  | Superseded by signed 32-bit Int.                                                                                                                      |
| Signed 64-bit Int                                                          | Explored as an alternative; not selected.                                                                                                             |
| Uppercase `AND`, `OR`, and `NOT`                                           | Superseded by `&&`, `\|\|`, and `!` when equality spelling was chosen.                                                                                |
| Only `elif` for additional branches                                        | Extended to equivalent `elif` and `else if` forms, preserving authored spelling.                                                                      |
| Both `fun` and `def` as function keywords                                  | This came from a misinterpreted, delayed steer about conditional branches. The user corrected it and explicitly selected `fun` only.                  |
| Colon return annotation, such as `fun f(x: Int): Int:`                     | The user identified a misclick and corrected it to `fun f(x: Int) -> Int:`.                                                                           |
| Arbitrary consistent indentation widths normalized to four spaces          | A proposal that was not selected. The chosen rule counts tabs and complete four-space groups as structural levels, with leftover spaces as alignment. |
| Broad interpretation that Unit may be omitted in function-type annotations | Clarified: omission applies to function declarations. Function-type annotations explicitly include Unit, for example () -> Unit.                      |
| Immutable arrays for variadic parameter containers                         | Superseded by fresh immutable `List<T>` containers for each call, following the user's correction.                                                    |

## Remaining design work and holes

These are unresolved topics, not additional approved features. This section is the canonical open-issue list.

### Completed steering checkpoint

The final six-topic round is recorded in S10-S15, T25-T26, M17-M19, and E35. The initial target includes precompiled
modules and permits runtime extensions, with explicit typed legacy bridges, input-checkpoint saves for the same build,
path-derived modules, a project manifest, and fail-fast runtime diagnostics.

The questionnaire is complete. The items below are specification and feasibility work, not another planned batch of
feature questions. Accepted features remain in the language direction; precise implementation phasing has not been fixed
beyond the explicit first-milestone requirements.

### Specification and engineering work

The details below can be resolved during drafting and feasibility review. They are not a pending questionnaire. Escalate
a detail to steering only when it exposes a material conflict, requires a scope change, or changes an observable
contract that cannot be reconciled with the accepted direction.

- **Grammar and formatting:** Complete lexer/grammar, keyword and identifier rules, comments, source newline handling,
  indentation jumps and blank/comment-only lines, alignment spaces interleaved with tabs, block expressions inside
  continuations, full precedence/associativity, `when` guard grammar and coverage analysis, and formatter defaults.
  Python-style chained comparisons such as `0 < score < 100` remain unsettled and must not be assumed supported.
- **Text and rendering:** Remaining string operations, malformed external text and storage encoding, length limits,
  escape parsing and Unicode-escape formatter preference, and mixed Char/String equality, ordering, joins, and
  overloads. Triple-string dedent must specify mixed tabs/spaces, blank and delimiter lines, newline encodings, and
  interpolation timing. Conversion APIs and exact Boolean/numeric output formatting remain open.
- **Numbers and ranges:** Numeric literals and conversion spelling, the minimum Int literal, integer zero division and
  overflow details, floating remainder, negative zero, fairmath grammar/lowering, and terminal-step overflow. The
  minimum Int divided by −1 overflows, while its remainder by −1 is mathematically zero; lowering must distinguish them.
  Range/progression type relationships, equality, endpoint/property APIs, reversed descending bounds, descending
  half-open forms, and a pinned Kotlin reference remain open. Large-progression membership cost and search-index failure
  behavior require review; `0..<count` must account for `count == 0` under R04.
- **Types and equality:** Formal constraint, inference, projection, and variance rules; universal-type and subtype/join
  interactions; Elvis result typing; complete equality operand eligibility; and non-returning-path proof. Generic-alias
  grammar and visibility, receiver/member lookup, private-constructor details, copy evaluation timing and method-name
  collisions, and exhaustive guarded-pattern analysis remain open. Define cycle-safe comparison for ordered and
  unordered structures, including recursive capability eligibility. Key eligibility must prove stable equality despite
  mutable fields or referenced values; hashing must agree with equality, including across approved widening. General
  inheritance and recursive nested payload patterns have not been selected.
- **Collections:** Complete literal and empty-literal inference, conversion and duplicate edge cases, mutable
  invariance, allocation/resource contracts, entry type naming and destructuring, add/remove method names/results,
  bounds-check timing, and remaining receiver/index/key cases. Equality eligibility for every element type remains open.
- **Scope and functions:** Symbol namespaces, module/import resolution, placement, alias conflicts and qualified access;
  label collisions and visibility; loop-bound evaluation timing and interaction with suspension. Recursion limits,
  failure behavior, and the Unit value's spelling remain open. Complete overload/reference resolution and function
  compatibility, Unit-context interactions with early returns/overloads/branch typing, and variadic edge cases need
  specification. Definite assignment and narrowing must account for forward/indirect calls, recursion, escaping
  captures, and captured delayed `val` initialization without expanding lexical name visibility.
- **Narrative:** Complete directive surface and lexing of embedded functions/continuations, mixed whitespace and
  remaining literal escapes, explicit line breaks, residual indentation, and paragraph boundaries across directives and
  nested prose. Once-option stable identity, modifier combinations, and history-filter timing relative to effectful
  visibility tests remain open.
- **Scenes and initialization:** Complete manifest schema, scene-name conflicts, scene-reference compatibility, and
  input binding modifiers. Evaluate targets/inputs/defaults consistently with visit replacement and frame abandonment.
  M15 now requires dependencies to finish before an initializer starts, with conservative discovery and cycle rejection.
  Shared-storage placement inside bodies, library-level ordinary bindings, initialization proof, re-exports, and
  declaration-modifier combinations still need specification.
- **Suspension and persistence:** Exact effect/flow analysis, continuation/capture representation, input-checkpoint
  detection, full-state serialization, stable identities, build matching, and target-runtime support. Cross-update saves
  are outside the initial contract. The contracts have not been verified through ChoiceScript lowering.
- **ChoiceScript interoperability:** Supported runtime profiles and command surface, explicit bridge declarations,
  dynamic legacy validation, and preservation of legacy behavior. Identify every required runtime extension.
- **Lowering and runtime:** Type representation using ChoiceScript facilities, nominal/generic identity for exact
  equality, case-sensitive name encoding, block scopes, activation frames, checked operations, temporary storage, source
  maps, diagnostics, generated helpers, and runtime requirements.
- **Errors and conformance:** Fail-fast reporting, compile-time versus runtime checks, source-location mapping, and
  original conformance examples for the selected semantics.
- **Broader scope:** Turing completeness, any future native target and self-hosting path, libraries/I/O, implementation
  technology, repository interfaces, and release commitments.

A whole-design review is required before treating this record as a finalized language specification.

[s1]: https://github.com/dfabulich/choicescript/blob/60a6c3ee7393c9ee7e42650b8e1642ae38e3cb6a/web/scene.js#L4995-L5028
[s2]: https://github.com/dfabulich/choicescript/blob/60a6c3ee7393c9ee7e42650b8e1642ae38e3cb6a/web/scene.js#L4173-L4251
[s3]: https://github.com/JetBrains/kotlin/blob/master/libraries/stdlib/src/kotlin/ranges/Progressions.kt
[s4]: https://github.com/JetBrains/kotlin/blob/master/libraries/stdlib/common/src/generated/_Collections.kt

[ext1]: https://github.com/betaflight/blackbox-log-viewer/pull/749
[ext2]: https://ptolemy.berkeley.edu/projects/embedded/mescal/forum/7/coreconnect_bfl.pdf?download=1
[ext3]: https://raw.githubusercontent.com/github-linguist/linguist/main/lib/linguist/languages.yml

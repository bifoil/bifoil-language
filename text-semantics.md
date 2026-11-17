# Text and comparison contracts

These rules complete drafting details under P03-P16, N03-N05, and E04-E05. They reconcile the selected Unicode scalar,
common-indent, explicit-conversion, and conventional binary-operator rules. They do not add Python comparison-chain
semantics, automatic composite interpolation, string-to-number parsing, or locale-sensitive formatting. Accepted
steering remains in [language-steering.md](language-steering.md); representation compatibility follows the separate
[profile contract](compatibility-contract.md).

## Triple-quoted strings

Source is UTF-8. Physical LF and CRLF line endings become LF in the logical contents of a multiline literal. An explicit
`\r`, including the `\r` in `\r\n`, remains a carriage-return scalar in the resulting value. The formatter preserves the
source file's authored line endings; source normalization for parsing does not rewrite that file.

Dedent processes exactly the raw contents between the delimiters, before decoding escapes or evaluating substitutions:

1. Split those contents at physical newlines. The first and last content fragments participate, including fragments
   sharing a line with an opening or closing delimiter.
2. Ignore whitespace-only lines when calculating the minimum indentation. Preserve their contents unchanged in the
   result. An all-blank literal therefore retains all its whitespace.
3. On each nonblank line, measure only leading ASCII spaces and tabs. A space contributes one column; a tab contributes
   four columns independently of its position. The minimum measured width is the common indentation.
4. Remove that many columns from every nonblank line. If removal cuts through a tab, retain its unused columns as
   spaces. Retain every other character and every newline. No extra first/last-line trimming occurs.
5. Decode the ordinary quoted-string escapes and parse substitutions. Evaluate substitutions left to right under the
   enclosing suspension permissions. Do not dedent or otherwise trim the String supplied by a substitution.

A nonblank first fragment with no indentation prevents removal from later lines. An indentation-only closing-delimiter
line remains a blank content fragment; its spaces are retained. The delimiters themselves never enter the value.
Whitespace-only Unicode content is excluded from the minimum calculation and retained; only ASCII spaces/tabs count as
removable indentation on a nonblank line.

For example, `"""\n    first\n      second\n    """` below denotes physical source newlines rather than escape
sequences. Its decoded content is `"\nfirst\n  second\n    "`. With a tab before `first` and two spaces before `second`,
the result instead retains two spaces before `first` and none before `second`. An escaped `\t` in source is decoded
after dedent and contributes no leading indentation to its raw line.

Interpolation code keeps its ordinary block-layout rules. Dedent preserves physical line count, so a failure inside a
multiline template still reports its original line. A suspension retains completed substitutions and decoded literal
segments; restoration must not repeat them. Formatting protects literal-content rows, including whitespace-only rows and
the indentation before a closing delimiter.

## Primitive rendering

Direct prose, option labels, String interpolation, and String concatenation render non-null String, Char, Int, Float,
and Boolean values. They share these spellings:

- String and Char contribute their scalar contents without surrounding quotes or Unicode normalization.
- Boolean contributes `true` or `false`.
- Int contributes ordinary base-ten digits, with a minus sign only for negative values and no grouping separators.
- Float uses the finite radix-ten `Number::toString` algorithm in the
  [ECMAScript numeric specification](https://tc39.es/ecma262/#sec-numeric-types-number-tostring).
  This is a precise formatting reference, not permission to expose non-finite values or JavaScript coercions.

Both zero signs render `0`; an integral Float such as 3.0 renders `3`. Examples include `0.000001`, `1e-7`,
`100000000000000000000`, `1e+21`, and `5e-324`. Output is independent of the host locale. Ordinary equality treats the
two Float zero signs as equal; exact equality still distinguishes Int from Float. A save may normalize the sign of zero
because none of these value, comparison, or rendering rules distinguishes it. Checked division by either zero sign
fails.

## Explicit conversions

The built-in operations are non-suspending; ordinary argument and receiver evaluation order still applies. A numeric
argument can use approved Int-to-Float widening. No operation below parses numeric text implicitly.

| Operation | Input | Result and checks |
| --- | --- | --- |
| `Int(value)` | Int or Float | Int; truncate toward zero, then check the signed 32-bit result range. |
| `Float(value)` | Int or Float | Finite Float; every Int value is represented exactly. |
| `number.toInt()` | Non-null Int or Float receiver | The same checked result as `Int(number)`. |
| `number.toFloat()` | Non-null Int or Float receiver | The same result as `Float(number)`. |
| `Char(value)` | Int | One Unicode scalar; reject negatives, surrogates, and values above U+10FFFF. |
| `character.code` | Char | Int Unicode scalar number. |
| `String(value)` | Any? | Explicit diagnostic rendering, including null and composites. |
| Built-in `value.toString()` | Non-null receiver | The same explicit rendering as `String(value)`. |

An authored data-class `toString` member uses ordinary member lookup and may define its own result. It does not
override the built-in `String(value)` conversion. The table describes the built-in method when no authored member
replaces that lookup.

Nullable numeric inputs must be handled before numeric conversion. `String(null)` is `"null"`; safe nullable member
access retains its usual null-skipping behavior instead of calling `toString`. `Unit` is both the type name and the
built-in sole value. `String(Unit)` is `"Unit"`. Numeric conversion errors report the original call line.

## Explicit composite rendering

This diagnostic representation is deterministic for a given value graph and insertion order. It is not a parser or a
save format. Transparent aliases add no runtime display identity. Stored values determine rendering; an exposed
covariant comparison view does not rewrite a nominal name, enum tag, or container contents.

- Lists render `[first, second]`; sets render `{first, second}` in insertion order; maps render `{key: value}` in
  insertion order. Empty sets and maps both render `{}`. An Entry renders `key: value`.
- Data values render the qualified nominal name followed by fields in declaration order, such as
  `story.Character(name=Ada, health=100)`. Private fields participate; privacy controls source member access, not an
  alternative automatically generated equality or diagnostic representation. Generic arguments are not printed.
- Sealed variants use their qualified variant name and payload field names, such as `story.Outcome.Success(value=Ada)`.
  A payload-free variant renders the qualified variant name followed by `()`.
- Under the current v3 profile, plain enums render the qualified enum and selected case, such as `story.Mood.Happy`.
  V1/v2 compiled programs retain their earlier `story.Mood()` rendering. The profile selects this behavior explicitly.
- Function values render `<function>`. Scene references render their qualified scene identity. No capture values or
  native addresses are printed for callable values.
- Integer ranges/progressions render their effective first/last values with `..` or `downTo`, followed by ` step n`
  when the step magnitude exceeds one.

Render nested supported values recursively in this order. A value already on the active ancestor path renders `<cycle>`;
remove it from that path after its contents finish. A repeated alias reached after an earlier occurrence has finished
renders again in full. This distinguishes cycles from repeated sharing without exposing addresses. Use an owned work
stack so graph depth does not consume the host call stack. Explicit conversion can render composites that lack static
equality eligibility; rendering does not grant Equatable or StableKey.

## Scalar validation and limits

Every String and Char contains valid Unicode scalar values. Source decoding rejects malformed UTF-8, and literal escapes
reject incomplete encodings, surrogates, and values above U+10FFFF. Runtime program/checkpoint values and typed legacy
text reject unpaired UTF-16 surrogates rather than replacing them silently. Valid supplementary pairs remain one scalar.
The host representation may use UTF-16; length/index/substring still use scalar positions.

Source and artifact readers apply their published byte limits before accepting input; checkpoints retain their published
size limit. The development runtime admits at most 16,777,216 UTF-16 storage units in one typed String, input response,
option label, prose buffer, output paragraph, or rendered result. This implementation guard counts storage units;
language length/index/substring operations still count Unicode scalars. An accepted supplementary pair occupies two
storage units and one scalar. The limit is unrelated to source-line capacity or the compiler's aggregate memory budget.

External typed text is checked for size before scalar scanning. Malformed scalar diagnostics identify a zero-based
scalar index and UTF-16 offset without echoing the rejected text. Runtime failures retain the original Bifoil operation
span. Size rejection takes precedence over invalid contents in oversized text. Concatenation, interpolation, diagnostic
rendering, and prose assembly account for result length before allocating the combined text. Rendered graph expansion
uses a bounded output length even when a small shared graph denotes a much larger textual expansion.

Invalid text submitted at a prepared native input wait is an API rejection: it does not invoke the host, consume the
wait, or fail the story. A valid replacement may still be submitted. Malformed host output is a checked story failure;
earlier completed paragraphs remain drainable once. Restored prose, labels, transcript text, and typed values
are checked
before any external host restoration.

Scalar validation and traversal process supplied text directly without constructing a character array. Source locations,
scalar indexes, and storage offsets retain their separate meanings. This bounds admission and combined text results;
it does not bound the allocation an external host made before returning a String, arbitrary native engine scripts,
total transcript retention, every heap allocation, or process memory. Full allocation and extreme-size runtime
acceptance remain separate work.

## Repeated comparisons

Conventional precedence and associativity apply to every ordinary binary operation. There is no pairwise-conjunction
comparison-chain production: `0 < score < 100` groups as `(0 < score) < 100` and fails because Boolean and Int do not
support ordering. Write `0 < score && score < 100`, or prefer `score in 1..<100` for those strict integer bounds. `true
== false == false` is an ordinary left-associated Boolean equality and evaluates to true. Parentheses can make that
grouping explicit. Fairmath retains its separately selected explicit-grouping requirement.

## Verification

The [text-contract cases](conformance/text-contracts.json) exercise triple whitespace/escapes, inserted multiline
values, checked numeric/scalar conversions, primitive formatting thresholds, repeated comparison typing, enum identity,
cyclic and shared data rendering, and actual suspended interpolation. Helper modules are compiled independently and
removed before the client build. Every tested input wait restores into a fresh runtime host in both output modes.
[Native lexer tests](../bifoil-compiler/src/lexer/tests.rs), [grammar
tests](../bifoil-compiler/src/parser/grammar_contracts.rs), and [formatter
tests](../bifoil-compiler/src/source_format/tests.rs) assert delimiter lines, Unicode blank content, mixed tabs/spaces,
CRLF normalization, escape order, and preserved source bytes. [Runtime
tests](../bifoil-runtime/test/text-contracts.test.mjs) cover both zero signs, decimal/exponent thresholds, legacy enum
compatibility, aliases/cycles, deep graphs, and malformed external scalar text.

The [text-admission cases](conformance/text-admission.json) assert malformed external scalar positions and dynamic
concatenation/interpolation failures at the original source line. [Runtime admission
tests](../bifoil-runtime/test/text-admission.test.mjs) cover exact storage boundaries, supplementary pairs, pre-join
checks, graph rendering, recoverable input rejection, completed-output retention, and validation before host restore.

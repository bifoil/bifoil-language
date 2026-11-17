# Development profile source grammar

This grammar describes the `bifoil-vm.v3` compiler profile. The [steering record](language-steering.md) remains the
language's requirements authority. Profile restrictions and permissive parser forms do not settle the unresolved
whole-language contracts in the [specification draft](language-specification-draft.md).

## Notation and lexical input

Quoted strings denote terminals. `|` selects an alternative, brackets denote optional content, braces denote repetition,
and parentheses group a production. Uppercase names denote lexical tokens. A terminal inside a quoted string includes
its punctuation literally. Spaces between EBNF elements do not require source whitespace unless needed to separate names
or numbers.

Input is valid UTF-8. A physical row ends with LF or CRLF; the last row need not have a newline. Names contain ASCII
letters, digits, and underscores and cannot start with a digit. Names and keywords are case-sensitive. Unicode scalar
text is supported in literals and prose; this does not introduce Unicode identifiers. There are no semicolon statement
separators, backtick identifiers, block comments, or backslash code continuations in this profile.

```ebnf
IDENTIFIER = (LETTER | "_"), {LETTER | DIGIT | "_"};
LETTER = "A" … "Z" | "a" … "z";
DIGIT = "0" … "9";
HEX = DIGIT | "a" … "f" | "A" … "F";
QUALIFIED_NAME = IDENTIFIER, {".", IDENTIFIER};
```

The following spellings are reserved at identifier-declaration positions:

```text
val var fun suspend scene shared legacy export import as if elif else prose choice option enabledIf once
return true false null when case is in for while do break continue goto visit vararg mutable data class
sealed enum typealias downTo step
```

`out`, `where`, `public`, `private`, `transfer`, `label`, and `result` are contextual words. Built-in type and value
names are resolved names, rather than additional lexical keywords. The type checker applies its ordinary conflict and
no-shadowing rules after parsing. The parser recognizes `as?`, `!in`, and `!is` as compound operators; the latter two
require a following identifier boundary. Longest recognized punctuation wins, including `%+=`, `%-=`, `..<`, `===`, and
`!==`. Negative signs are prefix operators, rather than part of numeric tokens.

Outside literals and prose, `#` or `//` starts a comment through the physical row end. A comment-only or blank row does
not open or close a block. Comments inside literal interpolation belong to its code; text that resembles a comment in
literal content or prose remains text.

Numeric token scanning admits decimal digits and underscores, an optional decimal fraction with a digit immediately
after the point, and an optional `e`/`E` exponent with an optional sign. `0x`/`0X` and `0b`/`0B` introduce hexadecimal
and binary integers. The lexer removes underscores, then the literal parser validates digits, radix, exponent, range,
and finite Float representation. Separator placement is currently permissive; stricter separator rules remain a
whole-language lexical detail. `1..3` contains an Int, a range operator, and an Int, rather than a decimal fraction.

String tokens use `"..."` or `"""..."""`; Char tokens use `'...'`. A Char must decode to exactly one scalar and cannot
interpolate. Literal scanning balances `${...}` through nested literals and delimiters before parsing that expression.
Escapes are `\\`, `\"`, `\'`, `\n`, `\r`, `\t`, `\${`, `\u` plus four hex digits, `\U` plus eight hex digits, or `\u{`
plus one to six hex digits plus `}`. Unknown/incomplete escapes, surrogate values, and values beyond U+10FFFF fail.
Literal LF characters require triple quotes except inside a continued interpolation. The [text
contract](text-semantics.md#triple-quoted-strings) defines exact common-indent removal, blank and delimiter lines, tabs,
source newline normalization, and substitution timing.

## Layout

`NEWLINE` below ends a complete logical statement. `INDENT` and `DEDENT` represent layout, rather than source text. Each
tab contributes one level and every complete group of four leading spaces contributes one level; remaining spaces are
alignment. For example, a tab plus four spaces is two levels. Ordinary body rows have exactly one more level than their
header, and an ordinary dedent must return to an enclosing level. Blank/comment rows are ignored for this test.

A statement continues inside open parentheses, brackets, or braces, or after an unfinished operator, assignment, comma,
arrow, member separator, or reference separator. Such continuation indentation is alignment. A closing `>` that
completes a type or explicit reference application does not by itself continue the statement. Nullable type headers
ending in `?:` mean `?` plus the block colon; an unfinished Elvis expression instead continues to its fallback.

Embedded `if`, `when`, and block-lambda expressions keep the structural indentation of their own header. Parsing their
bodies does not turn the surrounding call's remaining arguments or closing delimiters into body statements.

```ebnf
SUITE = ":", NEWLINE, INDENT, STATEMENT, {STATEMENT}, DEDENT;
```

## Files and declarations

```ebnf
FILE = {IMPORT | TOP_LEVEL}, EOF;
IMPORT = "import", QUALIFIED_NAME, ["as", IDENTIFIER], NEWLINE;
TOP_LEVEL = ["export"], (FUNCTION | SCENE | SHARED | ALIAS | DATA | SUM | ENUM | LEGACY);
SHARED = "shared", BINDING, NEWLINE;
BINDING = ("val" | "var"), IDENTIFIER, [":", TYPE], "=", EXPRESSION;
DELAYED = ("val" | "var"), IDENTIFIER, ":", TYPE;
FUNCTION = ["suspend"], "fun", [GENERICS], IDENTIFIER, PARAMETERS, ["->", TYPE], [WHERE], BODY;
SCENE = "scene", IDENTIFIER, PARAMETERS, SUITE;
BODY = SUITE | "=", EXPRESSION, NEWLINE;
PARAMETERS = "(", [PARAMETER, {",", PARAMETER}], ")";
PARAMETER = ["var"], ["vararg"], IDENTIFIER, ":", TYPE, ["=", EXPRESSION];
GENERICS = "<", GENERIC, {",", GENERIC}, ">";
GENERIC = ["in" | "out"], IDENTIFIER, [":", TYPE];
WHERE = "where", CONSTRAINT, {",", CONSTRAINT};
CONSTRAINT = IDENTIFIER, ":", TYPE;
ALIAS = "typealias", IDENTIFIER, [GENERICS], "=", TYPE, [WHERE], NEWLINE;
DATA = "data", "class", IDENTIFIER, [GENERICS], [WHERE], ":", NEWLINE,
       INDENT, {FIELD | METHOD}, DEDENT;
FIELD = [VISIBILITY], ("val" | "var"), IDENTIFIER, ":", TYPE, ["=", EXPRESSION], NEWLINE;
METHOD = [VISIBILITY], FUNCTION;
VISIBILITY = "public" | "private";
SUM = "sealed", "class", IDENTIFIER, [GENERICS], [WHERE], ":", NEWLINE,
      INDENT, VARIANT, {VARIANT}, DEDENT;
VARIANT = ["case"], IDENTIFIER, ["(", [PAYLOAD, {",", PAYLOAD}], ")"], NEWLINE;
PAYLOAD = IDENTIFIER, ":", TYPE, ["=", EXPRESSION];
ENUM = "enum", IDENTIFIER, ":", NEWLINE, INDENT, ENUM_CASE, {ENUM_CASE}, DEDENT;
ENUM_CASE = ["case"], IDENTIFIER, ["(", ")"], NEWLINE;
LEGACY = "legacy", (LEGACY_STORAGE | LEGACY_CALL);
LEGACY_STORAGE = ("val" | "var"), IDENTIFIER, ":", TYPE, "=", STRING, NEWLINE;
LEGACY_CALL = ["suspend"], ["transfer"], "fun", [GENERICS], IDENTIFIER, PARAMETERS,
              ["->", TYPE], [WHERE], "=", STRING, ["label", STRING], ["result", STRING], NEWLINE;
```

An import must contain at least a module and a symbol. Shared declarations require initializers. Ordinary file-level
`val`/`var` declarations and executable library statements are not implemented by this profile. Scene functions have
Unit results and may suspend; generic scene parameters are not part of the selected scene interface. The parser also
accepts explicit `-> Unit` on scene headers and `suspend legacy` ordering. The optional `case` prefix and empty enum
parentheses above describe permissive parser forms; examples should use `case Name`. The type checker rejects plain enum
payloads, illegal modifiers, invalid visibility, unsupported bridge types, and misplaced declarations.

A named or anonymous callable can have at most one variadic parameter, last, without an explicit default. Parameters
require annotations. Defaults may precede required parameters. Type parameters on functions are invariant; nominal
variance must pass the static field/method usage checks. Declaration/body checking is required even for unused code.

## Types

```ebnf
TYPE = TYPE_ATOM, ["?"];
TYPE_ATOM = QUALIFIED_NAME, ["<", TYPE, {",", TYPE}, ">"]
          | "*"
          | "(", TYPE, ")"
          | ["suspend"], "(", [TYPE_PARAMETER, {",", TYPE_PARAMETER}], ")", "->", TYPE;
TYPE_PARAMETER = ["vararg"], TYPE;
```

Parentheses around one type group it. A function type requires its result, including Unit; a nullable function value
therefore uses `((Int) -> Unit)?`. A variadic function-type parameter is last. Repeated explicit nullable markers fail.
Stars require an admissible projected generic position; the grammar alone does not establish safe operations on them.
`Scene` is the no-input scene-reference type and `Scene<Int, String>` carries positional input types. Aliases introduce
no distinct runtime identity. Named type arity, bounds, visibility, and references are checked after name resolution.

## Statements and control flow

```ebnf
STATEMENT = (BINDING | DELAYED | ASSIGNMENT | EXPRESSION), NEWLINE
          | SHARED | ALIAS | FUNCTION | IF | WHEN | LOOP | PROSE | CHOICE;
ASSIGNMENT = TARGET, UPDATE, EXPRESSION;
TARGET = IDENTIFIER | POSTFIX, ".", IDENTIFIER | POSTFIX, "[", EXPRESSION, "]";
UPDATE = "=" | "+=" | "-=" | "*=" | "/=" | "%=" | "%+=" | "%-=";
IF = "if", EXPRESSION, SUITE, {("elif" | "else", "if"), EXPRESSION, SUITE}, ["else", SUITE];
WHEN = "when", [WHEN_SUBJECT], ":", NEWLINE, INDENT, WHEN_ARM, {WHEN_ARM}, DEDENT;
WHEN_SUBJECT = EXPRESSION | "val", IDENTIFIER, [":", TYPE], "=", EXPRESSION;
WHEN_ARM = "case", PATTERN, {",", PATTERN}, ["if", EXPRESSION], SUITE | "else", SUITE;
PATTERN = EXPRESSION | ("in" | "!in"), EXPRESSION
        | "is", TYPE, ["(", [IDENTIFIER, {",", IDENTIFIER}], ")"] | "!is", TYPE;
LOOP = [IDENTIFIER, "@"], ("for", IDENTIFIER, "in", EXPRESSION, SUITE
       | "while", EXPRESSION, SUITE | "do", SUITE, "while", EXPRESSION, NEWLINE);
CHOICE = "choice", ":", NEWLINE, INDENT, {OPTION}, ["else", SUITE], DEDENT;
OPTION = "option", STRING, ["if", EXPRESSION], ["enabledIf", EXPRESSION], ["once"], SUITE;
TRANSFER = "return", [EXPRESSION] | ("break" | "continue"), ["@", IDENTIFIER]
         | ("goto" | "visit"), EXPRESSION;
```

An `else` arm is unique and last. A choice requires at least an option or a fallback. Subjectless cases are Boolean
expressions; type/membership patterns require a subject. Payload patterns have one level; `_` creates no binding. Comma
alternatives must bind the same names with compatible types. Guards run after the match. Transfer expressions retain
function, loop, scene, and suspension-context checks. `visit` produces Unit; non-returning transfers produce Nothing.
Assignments and compound updates produce no expression value. Only labeled loops accept labeled jumps.

## Expressions and precedence

```ebnf
EXPRESSION = BINARY_EXPRESSION | LAMBDA | IF | WHEN | TRANSFER;
LAMBDA = ["suspend"], PARAMETERS, ["->", TYPE], "=>", (EXPRESSION | SUITE);
POSTFIX = PRIMARY, {"(", [ARGUMENTS], ")" | "?.", "(", [ARGUMENTS], ")"
        | ("." | "?." | "::"), IDENTIFIER | ("[" | "?["), EXPRESSION, "]" | "!!"
        | "<", TYPE, {",", TYPE}, ">"};
ARGUMENTS = ARGUMENT, {",", ARGUMENT}, [","];
ARGUMENT = [IDENTIFIER, "="], ["*"], EXPRESSION;
PRIMARY = IDENTIFIER | NUMBER | STRING | CHAR | "true" | "false" | "null"
        | "::", IDENTIFIER | "(", EXPRESSION, ")" | COLLECTION;
COLLECTION = ["mutable"], ("[", [ELEMENTS], "]" | "{", [ELEMENTS | ENTRIES], "}");
ELEMENTS = EXPRESSION, {",", EXPRESSION}, [","];
ENTRIES = EXPRESSION, ":", EXPRESSION, {",", EXPRESSION, ":", EXPRESSION}, [","];
```

`NUMBER`, `STRING`, and `CHAR` are the tokens defined above. `BINARY_EXPRESSION` is the precedence-climbing expression
with prefix `-`/`!`, postfix forms, and the operators below. The explicit type-argument postfix is recognized before a
call or on an explicit function/bound reference; ordinary `<` otherwise remains a comparison. Bare overloaded names are
not implicitly function references. Calls enforce positional-before-named ordering and prohibit duplicates.

The table is ordered from strongest to weakest. Binary operators associate left except Elvis, which associates right.
The cast and type-test right operands are types, rather than value expressions. Prefix operands include casts; for
example `-x as Float` parses as `-(x as Float)`. Parentheses override grouping.

| Binding | Operators/forms | Association |
| --- | --- | --- |
| Postfix | Calls, members, indexes, `::member`, explicit type arguments, `!!` | Source order |
| Cast/prefix | `as`, `as?`; prefix `-`, `!` | Casts left; prefix nests right |
| Multiplicative | `*`, `/`, `%` | Left |
| Additive | `+`, `-` | Left |
| Range | `..`, `..<` | Left |
| Infix progression | `downTo`, `step` | Left |
| Null fallback | `?:` | Right |
| Membership/type test | `in`, `!in`, `is`, `!is` | Left |
| Ordering | `<`, `<=`, `>`, `>=` | Left |
| Equality | `==`, `!=`, `===`, `!==` | Left |
| Conjunction | `&&` | Left |
| Disjunction | `||` | Left |

Fairmath `%+` and `%-` use the additive parser binding only to recognize an isolated operation. Combining a fairmath
operation with any other binary operation or another fairmath operation requires explicit parentheses; the additive
binding is not permission to omit them. Comparison chains do not gain Python's pairwise conjunction semantics; a parsed
Boolean/numeric comparison still fails ordinary operand checking. The [repeated-comparison
contract](text-semantics.md#repeated-comparisons) explicitly retains binary grouping and ordinary operand checking; it
does not introduce a comparison-chain production.

## Prose mode

```ebnf
PROSE = "prose", ":", NEWLINE, INDENT, PROSE_ITEM, {PROSE_ITEM}, DEDENT;
PROSE_ITEM = NARRATIVE_ROW | BLANK_ROW | "@", STATEMENT;
```

`NARRATIVE_ROW` contains unquoted scalar text and balanced `${EXPRESSION}` substitutions. `BLANK_ROW` separates
paragraphs. After structural indentation removal, single narrative row endings become spaces. `\${`, `\@`, and `\\`
escape interpolation, directive introduction, and backslashes. An `@` starts a directive only after the row's
indentation and outside an unfinished interpolation. Directive headers and branch headers use Bifoil syntax; nested
bodies stay in prose mode. Further executable rows in those bodies also require `@`. Ordinary `#`, `//`, and quote
characters do not become code comments or string delimiters merely by appearing in narrative text.

Callable and value-producing directive suites retain lexical prose mode; executable results still need @. A prose-body
callable owns an output context when invoked. The [prose contract](prose-semantics.md) defines separators, line breaks,
comments, formatting, and callable transfers. Prose and option-label interpolation requires a directly renderable
non-null primitive and must not suspend. Ordinary quoted-string interpolation follows its enclosing effect context.
Expression validation, static checking, and physical source locations remain necessary in all modes.

Interpolation expressions use the ordinary expression and block-layout grammar in code mode, including value-producing
`if`/`when` and block-bodied anonymous functions. They do not inherit narrative mode from surrounding prose. A block's
body is one structural level deeper than its header; subsequent branch headers align with that header. An interpolation
contains one expression, so another statement following a completed expression is rejected. Nested interpolation and
quoted text retain the same effect checks and nesting budget.

```bifoil
scene start():
    val flag = true
    prose:
        Result: ${if flag:
            val bonus = 2
            bonus + 3
        else:
            0
        }
```

Physical source lines survive paragraph folding and nested template parsing. Statements inside an interpolated block
retain their own locations; parser errors report the inner failing line once at the source-file boundary. Ordinary
continued operations without an individual AST location retain their containing expression's source precision.

The built-in progression member `step` is contextual after `.`, `?.`, or `::`; it does not become an unfinished infix
operation there. It remains reserved in declaration positions. Member references still require a callable member, so
recognizing its spelling does not turn the numeric property into a method.

## Implementation correspondence

The compiler separates [AST definitions](../bifoil-compiler/src/syntax.rs), [lexing](../bifoil-compiler/src/lexer.rs),
[layout](../bifoil-compiler/src/parser/layout.rs), [declarations](../bifoil-compiler/src/parser/declarations.rs),
[types](../bifoil-compiler/src/parser/types.rs), [expressions](../bifoil-compiler/src/parser/expressions.rs),
[patterns](../bifoil-compiler/src/parser/patterns.rs), and [prose](../bifoil-compiler/src/parser/prose.rs). The
[operator table](../bifoil-compiler/src/parser/operators.rs) owns numeric parser bindings. Internal AST forms such as
lowered construction and branch yields are not additional source syntax. Resource guards limit accepted depth and volume
independently of these productions; [resource limits](../bifoil-compiler/RESOURCES.md) document those guards.

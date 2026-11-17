# Prose modes, paragraphs, and callable output

This contract completes current-profile details around T01-T05 and T09-T11. Ordinary typing, lexical scope, return
conventions, and suspension checks remain in force.

## Lexical modes and executable suites

An explicit prose: enters unquoted narrative. A line-leading @ after structural indentation introduces an ordinary
executable statement. Conditional, loop, when, choice-option, named-function, and anonymous-function block suites retain
that lexical prose mode. Their literal rows remain narrative; executable rows and branch headers require @. An
unprefixed keyword-looking word is still prose.

~~~bifoil
fun factory() -> () -> Int:
    prose:
        @fun answer() -> Int:
            The answer arrives.
            @return 7
        @return ::answer
~~~

The example returns a function value. Invoking it later renders its narrative and returns Int 7. A named expression body
remains one ordinary expression. A prose-mode anonymous block returns its final executable expression, with the existing
Unit-context discarding and early-return rules. Value-producing if/when suites introduced by a directive also retain
prose mode; prefix their executable results and branch headers.

Interpolation is a separate expression fragment: inside ${...}, ordinary code mode applies to block expressions,
lambdas, strings, and explicit nested prose: blocks. Continued expressions retain parentheses/trailing-operator rules;
continuation indentation remains alignment.

~~~bifoil
scene start():
    prose:
        @val score: Int = if true:
            Chosen
            @3
        @else:
            @4
        Result ${score}; ${if score == 3:
            "confirmed"
        else:
            "unexpected"
        }.
~~~

Ordinary # and // rows are literal prose. After an explicit @ prefix they are code comments and produce no output. Code
comments may separate aligned branch headers. Literal prose cannot disappear during branch lookahead.

## Paragraphs and whitespace

Remove the structural prose prefix. A tab counts as four structural spaces; preserve residual leading/trailing content,
including alignment. A physical single newline within a literal paragraph becomes one space. Text chunks separated by
nonprinting directives join the active paragraph in execution order.

One or more blank rows separate paragraphs. A blank run before a dedent belongs to the surrounding suite containing the
next row. It does not execute once on every visit to a completed loop or branch. Blank separators between aligned
branch/case/option headers are layout and create no output for unselected alternatives. A trailing blank run at the end
of a suite creates no empty output paragraph.

An internal blank run becomes one paragraph boundary and preserves physical line numbers for later content. The parser
scans that run once instead of rescanning every suffix. Source formatting protects narrative/literal content.

## Explicit line breaks and escapes

Write \n inside prose for a line break within the current paragraph. It does not begin another paragraph. Ordinary
quoted-text escapes are available alongside \@ and \${ for literal introducers. In particular, \\n produces literal
backslash-plus-n. Unknown escapes and invalid Unicode scalar escapes fail. Interpolated String/Char values retain their
actual contents, including newline characters.

The VM transcript and custom output hooks receive real newline characters. Default ChoiceScript presentation maps LF,
CRLF, and CR to the pinned renderer's existing inline line-break marker before publishing one paragraph. It does not
perform native variable interpolation on formatted Bifoil text. Other layout, including ordinary space collapsing,
follows the host's established paragraph renderer.

## Callable contexts, transfers, and suspension

A callable with a block suite parsed in prose mode owns a fresh prose context when invoked. It may escape its defining
scope and render when called from ordinary code. Starting its context flushes pending outer prose in execution order.
Returns and normal completion flush/close its own output without taking ownership of its caller's context.

Expression-bodied functions gain no implicit prose context. Ordinary code-mode functions/lambdas retain ordinary bodies;
explicit prose: introduces narrative there. Prose-body callables retain a real call frame when captured initialization
proofs would otherwise permit compact expansion.

Loop transfers retain the appropriate surrounding prose depth. Suspended calls and choices preserve active prose
contexts and completed output at input checkpoints. Restoration does not print earlier text again. Interpolation and
choice-preparation expressions remain non-suspending even when calling prose-producing helpers; ordinary effect checks
still reject input waits there.

## Evidence

The [prose-boundary cases](conformance/prose-boundaries.json) exercise escaped named/anonymous functions, suspension,
source-free checkpoints, directive value blocks, code-mode interpolation, separator ownership, comments, and explicit or
literal newline escapes. Negative controls preserve executable-prefix requirements.

The [native tests](../bifoil-compiler/src/tests/prose_callables.rs) and [formatter
tests](../bifoil-compiler/src/source_format/tests.rs) check typed bodies, physical origins, and long blank runs. The
[presentation tests](../bifoil-runtime/test/presentation-newlines.test.mjs) run the actual pinned paragraph renderer
with a minimal DOM stub; they do not establish production browser/save-host acceptance.

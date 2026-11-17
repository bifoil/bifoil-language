# Legacy ChoiceScript compatibility

Bifoil's typed legacy adapter executes native source through the explicitly supplied, unmodified ChoiceScript engine. It
does not translate native expressions into Bifoil. The current development bridge profile covers typed primitives, plain
enums, nullable forms, ordinary returns, explicit transfers, and the prepared waits described below. Full native
UI/platform acceptance and composite boundary ownership remain separate work.

## Native command inventory

The [machine-readable inventory](../bifoil-runtime/native-command-profile.json) classifies every command in the pinned
engine's Scene.validCommands once. It records the exact engine revision and source SHA-256. Command presence in that
engine does not establish host support. The groups have these explicit implementation boundaries:

### Engine core

Delegated to the unchanged engine; ordinary native data/control semantics.

`comment`, `goto`, `gotoref`, `label`, `looplimit`, `create`, `create_array`, `temp`, `temp_array`, `delete`,
`delete_array`, `set`, `setref`, `print`, `if`, `else`, `elseif`, `elsif`, `rand`, `gosub`, `gosub_scene`, `return`,
`params`, `hide_reuse`, `disable_reuse`, `allow_reuse`.

### Prepared input

Adapter-owned prepared waits; suspension permission, checkpoint restoration, and no replay are required.

`choice`, `fake_choice`, `page_break`, `input_text`, `input_number`.

### Transfer boundary

Explicit transfer bridges only; ordinary bridges reject replacement or termination before its destination executes.

`goto_scene`, `finish`, `ending`, `abort`.

### Host rendering

Requires the engine host renderer. Paragraph ordering is checked for image/stat_chart/line_break; other renderers need
host-specific acceptance.

`image`, `text_image`, `stat_chart`, `line_break`, `sound`, `youtube`, `kindle_image`, `kindle_search`,
`kindle_product`, `link`, `link_button`.

### Startup metadata

Upstream startup rules still apply. The typed adapter does not run a complete native startup or synthesize these host
services.

`achievement`, `author`, `ifid`, `product`, `scene_list`, `title`.

### Platform lifecycle

Outside the built-in prepared-continuation profile. Browser globals may execute upstream behavior, but callbacks,
external services, persistence, and replacement lifetimes are not integrated or claimed supported.

`advertisement`, `achieve`, `ai`, `bug`, `check_achievements`, `check_purchase`, `check_registration`, `config`,
`delay_break`, `delay_ending`, `end_trial`, `feedback`, `finish_advertisement`, `goto_random_scene`, `login`,
`more_games`, `page_break_advertisement`, `print_discount`, `purchase`, `purchase_discount`, `redirect_scene`, `reset`,
`restart`, `restore_checkpoint`, `restore_game`, `restore_purchases`, `save_checkpoint`, `save_game`, `script`,
`share_this_game`, `show_password`, `subscribe`, `timer`, `track_event`.

## Prepared continuation boundary

Native choice/fake-choice, page breaks, text input, and number input are represented by checked adapter waits. Choice
labels, enabling results, input bounds, and completed preparation are retained across same-build saves. No ordinary
bridge can transfer or terminate the story. An explicit transfer bridge abandons Bifoil callers and may transfer/end
through the supported native boundary. Native finish can prepare a chapter button before entering the next scene.

The adapter does not serialize arbitrary browser callbacks, timers, native password saves, purchases, login sessions,
remote configuration, script closures, or external DOM/application state. Supplying browser globals may let an upstream
platform command execute, but does not make its lifecycle saveable or supported by this profile. Unsupported callbacks
are not converted into prepared waits. A custom legacy host must implement its own explicit checked continuation
interface; a browser global by itself is insufficient. Bifoil saves use the VM checkpoint API at prepared input waits.

Image/chart/line-break ordering has direct adapter tests with supplied renderers. Those tests check ordering and escaped
presentation boundaries, not a full production browser, media platform, or host persistence service. Headless clients
must supply the renderers needed by their selected native sources.

## Checked value boundary

Every legacy read and returned result is checked against its declared Bifoil type before typed use. Number-like Strings
do not become Int/Float implicitly; fractional/out-of-range Int, non-finite Float, malformed scalar text, invalid Char,
and wrong enum tags fail. Plain enum Strings are checked against the exact expected nominal declaration. Unit results
discard the external return value; nullable results preserve native null. Composite collections/data/generics are not
implicitly trusted or assigned an unselected ownership representation.

Failures report the original Bifoil bridge/read source span. Native engine failures additionally retain their native
diagnostic. Completed output is drainable once; failure cannot repeat a native resume or run trailing Bifoil code.
Volatile shared native proxies are checked on each read; copied typed values follow ordinary Bifoil narrowing rules.

## Verification

[Legacy conformance](conformance/legacy.json) pairs valid values with wrong numeric, enum, and Char rejections; checks
volatile proxies, defaults/varargs, ordinary/transfer effects, source-free interfaces, nested calls, prepared input, and
fresh-engine checkpoint restoration. The [returned-value location case](conformance/legacy-validation.json) asserts a
failed native result after an actual prepared wait and source-free module import. It checks the original Bifoil location
and preserved completed output. [Runtime boundary tests](../bifoil-runtime/test/legacy.test.mjs) verify terminal error
identity and one-time external cleanup after a bad result; [engine tests](../bifoil-runtime/test/legacy-engine.test.mjs)
use the unmodified interpreter and compare input validation with its original callback. [Text
admission](text-semantics.md#scalar-validation-and-limits) separately covers malformed external text, valid replacement
submission, and validation before host restoration.

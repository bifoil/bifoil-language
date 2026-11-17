# Source selection and shared file extensions

The .bfl suffix is a preferred source name, not proof that an arbitrary file contains Bifoil. The [dated conflict
check](language-steering.md#preferred-extension-and-conflict-check) records unrelated uses.

## Compiler entry points

A project build explicitly selects a project containing bifoil.toml. Its entry scene and explicit imports determine the
reachable source/module graph under the configured roots. An unrelated .bfl file does not become a module merely because
it sits beside a referenced source. The compiler does not register system-wide extension associations.

The module and format commands explicitly select a source file. They parse it as Bifoil because the command selects the
language, including when that file uses another extension. Explicitly selecting foreign binary/log content reports an
error and preserves both the input bytes and any previous completed output artifact.

Future editor/file-picker integrations must use a project manifest or explicit language selection in addition to the
suffix. Those integrations remain separate work; the current compiler does not claim their detection or UI acceptance.
Existing legacy ChoiceScript inputs retain their explicit manifest/bridge selection and native parsing rules.

## Evidence

The [CLI regression](../bifoil-compiler/tests/cli/file_detection.rs) builds a manifest-selected story beside a foreign
binary .bfl file, independently compiles an explicitly selected .txt source, and checks foreign-file rejection with
unchanged input and prior artifact bytes.

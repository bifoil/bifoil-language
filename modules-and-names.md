# Modules, aliases, and shared storage

This contract specifies explicit cross-file visibility, transparent alias interfaces, enum case lookup, declaration
grammar, separate type/value namespaces, and persistent storage with lexical visibility. The namespace, export-name, and
nested-shared rules incorporate the user's explicit clarifications of 2026-11-05.

## Modules and public interfaces

Sources under src/ derive dotted module names from their relative paths. For example, story/stats.bfl supplies module
story.stats. Module names select files or independently compiled artifacts; they do not automatically introduce source
bindings or permit otherwise unimported access.

Import one exported symbol with import story.stats.gold, optionally followed by as coins. Bind that symbol under its
last component or the explicit alias. Imports are file-level declarations and must contain both a module and symbol.
Wildcard, module-only, and export import forms are not part of the selected grammar. Importing a declaration does not
implicitly import every dependency of its owning module.

File-level declarations are private unless prefixed with export. A client can import only the owner's exported
interface. This applies equally when the owner source was removed after precompilation. An import alone does not
re-export its binding. Reusable public forwarding uses another authored exported declaration, such as a transparent type
alias or function wrapper:

~~~bifoil
import colors.Mood as Underlying
import colors.count as sourceCount
export typealias Mood = Underlying
export fun current() -> Int = sourceCount
~~~

The alias exposes the same underlying type rather than a new declaration identity. The wrapper has its own checked
signature and body. Shared bindings imported under multiple names still refer to the same persistent cell; an ordinary
local value initialized from one is a separate binding. Exporting a wrapper does not export the imported source name.

The compiler resolves the complete imported interface before checking bodies. Missing exports, duplicate/conflicting
bindings, invalid types, and inconsistent artifacts fail before output publication. Checked cyclic imports and source
dependencies follow their existing component/interface contracts; explicit imports do not disable cycle checks.

## Transparent type aliases

Type aliases denote existing types and introduce no runtime type or allocation. Their annotations, generic arguments,
bounds, and exported interfaces normalize to the underlying type. File-level aliases are private by default and can be
exported/imported with the ordinary declaration rules.

Aliases are also allowed in ordinary lexical blocks. Their names are visible throughout that block and nested blocks,
including before their written declaration. They do not escape sibling blocks or another function. Each function or
nominal generic parameter retains its owning identity; an alias inside that scope refers to that parameter. The same
alias spelling in separate sibling scopes denotes their independent lexical definitions.

Register the complete alias group before expansion, resolving forward references in its shared lexical scope. Expansion
checks both bodies and bounds. Reject direct and indirect alias-expansion cycles, including cycles hidden inside a
generic argument or bound. Recursive structures must pass through nominal data or sum types; nominal recursion does not
require expanding an alias forever. Alias argument counts and bounds remain checked even when unused.

Aliases cannot hide visible type names, built-in types, or generic parameters. Duplicate type imports fail even if their
expansions match. A type alias and an ordinary value may share a name; annotations and value expressions use their
respective namespaces. Same-namespace duplicate declarations and shadowing remain errors.

## Enum and member lookup

Importing an enum, or a transparent nongeneric alias to it, exposes its qualified cases under the imported local name.
For example, an imported alias State supports State.Happy. Constructor and enum identities remain owned by the original
declaration, including through a transitive exported alias and source-free module loading.

An expected enum type can resolve a bare case such as Happy in an annotation, argument, default, or branch context.
Without a uniquely suitable expected enum, use a qualified case. If an ordinary visible binding and that case are both
interpretations, report a conflict and require qualification; do not silently choose one. A type namespace itself is not
an enum value. Case-sensitive identifiers and designated keyword spelling remain in force.

Fields and methods use the existing instance member namespace. Methods can use this.member or an unambiguous bare
member. Their nested local declarations cannot hide those implicit member bindings. Public/private access and the
generated reserved copy member follow their separate accepted rules. A bound reference captures its receiver once.

Ordinary values, parameters, iteration and pattern bindings retain no-shadowing, and local variables remain visible only
from their declarations. Function overload sets may combine compatible same-scope declarations, including explicitly
imported callable groups. The normal type/arity, conversion, default, and variadic rules resolve calls; scenes do not
become overloadable functions.

## Shared state and visits

Every library-module value declaration requires shared val or shared var. There is no executable module initialization
block or ordinary file-level val/var storage. Shared declarations require initializers, which cannot suspend. A new
playthrough initializes each shared value once before scene entry, using the selected dependency order. Loading restores
stored state without replaying initialization.

An ordinary val/var inside a scene body belongs to that fresh visit and follows lexical block scope. Returning and later
visiting the scene again creates fresh locals and inputs. Shared imports continue to observe the same story state across
those visits and their input checkpoints. A val binding cannot be reassigned; this does not freeze a referenced mutable
object.

Nested shared val/var declarations are also permitted in ordinary lexical blocks, including function and scene bodies.
Their names become visible from the declaration onward and do not escape their block. Each source site has one cell per
playthrough, shared across calls, recursion, loop iterations, and generic instantiations. Separate sibling sites have
separate cells even when their names match.

Initialize every site before the first scene, including unused functions and untaken branches. Executing the declaration
only introduces its lexical name; it does not rerun an initializer or copy the value. Initializers may use module
declarations and earlier lexically visible shared cells, but cannot use enclosing parameters, ordinary locals, local
functions, receivers, or function/class type parameters. Local type aliases must resolve independently of those
parameters. Calling module-level generic helpers with independently determined concrete arguments remains valid.

All sites participate in dependency-first initialization and conservative cycle checks. Independent sites retain stable
module/source order. Loading restores cells without replay. Lexical aliases and escaping closures keep using the same
stored cell across input checkpoints.

## Declaration grammar and modifiers

The [source grammar](development-source-grammar.md#files-and-declarations) defines every supported header and its AST
role. An optional export prefixes a file-level declaration. Shared then precedes val/var; suspend precedes fun. Function
type parameters follow fun and precede the name; data/sum/alias arguments follow their declaration name. Typed
parameters use optional var then optional vararg; variadic parameters must be last and have no explicit default. Return
annotations use an arrow. Where constraints follow a function result or an alias's right-hand type.

Data member visibility precedes a field or method. Data fields use explicit types and val/var; their defaults are
per-construction defaults. Sealed variants use typed fixed payload bindings. Enum cases have no payload. A scene has a
named block body and Unit result. Imports, aliases, declarations, references, and scene headers retain the documented
layout and continuation rules. Duplicate or misplaced modifiers and incomplete declarations are errors.

Legacy bridge declarations retain their separate typed grammar and supported boundary representation; this document does
not choose a composite legacy ownership policy.

## Export names and member lookup

One exported entity owns each public name. Co-exporting a type alias and a value/function as Label is a compile error,
even though local/private names may overlap. A single data declaration and its generated constructor form one entity.
Check this before publishing provisional cyclic interfaces as well as complete artifacts. An import binds the single
exported entity in its appropriate namespace; explicit aliases or wrappers provide authored public forwarding.

A visible ordinary value prefix owns member lookup over a same-named type alias. After a value Flag is declared,
Flag.Happy reads its member. Check initialization and member existence normally; failure cannot fall back to a static
enum case. Before that declaration, the alias's qualified case remains available. Capturing functions retain the
ordinary receiver binding and observe its current value.

Generated constructor/copy field operands refer directly to their known parameters. A field named Happy of type Mood
remains constructible when Mood.Happy exists. Authored bare Happy expressions still report the selected expected-type
ambiguity when an ordinary binding is also visible. The generated copy name remains reserved.

## Artifact compatibility

Module v5 requires ordinary value-prefix priority, including capture and definite-initialization checks. An older body
may contain a different enum constant while keeping the same public result type. Regenerate v1/v2/v3/v4 modules from
source; changing a format field or digest cannot repair that body. Existing VM v3 instructions represent fields, lexical
aliases, and persistent cells, so program/package/code/checkpoint versions remain unchanged.

## Evidence

The [source-free namespace cases](conformance/namespace-contracts.json) remove enum, alias, function, and scene sources
before client compilation. They check transparent generic/forward aliases, captured generic ownership, transitive enum
shorthand, imported overload groups, private imports, and absence of automatic re-exports. Two restored visits retain
shared counts while recreating local variables. Paired errors cover hidden/unimported names, case conflicts, alias
cycles and scope, missing shared initialization, invalid placement, and modifier/import grammar.

[Parser assertions](../bifoil-compiler/src/parser/grammar_contracts.rs) inspect the distinct declaration ASTs, imports,
generic constraints, parameter modifiers, legacy targets, and scene headers. [Module
tests](../bifoil-compiler/src/tests/modules.rs), [enum alias tests](../bifoil-compiler/src/tests/enum_aliases.rs), and
[lexical alias tests](../bifoil-compiler/src/tests/normalization_scopes.rs) cover artifact identity and scope isolation.
These contracts do not establish target-scale discovery/indexing capacity, production-host acceptance, or a release.

The [separate-namespace cases](conformance/namespace-separation.json) check value-prefix capture and initialization,
duplicate imports, built-in conflicts, generated enum fields, and co-export rejection. The [nested-shared
cases](conformance/scoped-shared.json) check eager startup, generic-independent cells, source-free closure checkpoints,
dependencies, and rejected enclosing-state access. The original placement fixture's source is retained with an
expectation matching the explicit user clarification.

# java.lang nullness roadmap

Scope is pinned to the JDK source underlying PR #7 (`ded0ec1cf95`). The first
pass uses Checker Framework annotations in JSpecify mode. It does not verify
initialization, map keys, purity, or native implementations. Native contracts
remain reviewed assumptions. Subpackages such as `java.lang.reflect`, `invoke`,
`ref`, `constant`, and `module` are separate studies.

## Delivery and milestone gates

Each PR covers one related API group and targets the preceding branch while
its parent is open. Each changed Java file has its own annotation commit;
workflow and documentation changes are separate. Tests and the shared script
live in the matching Checker Framework branch, not in this repository.

A group is complete only when all its files have documentation-oracle records,
complete declaration-scope review, passing source checks with suppression audits,
and relevant valid/invalid caller tests in CF. The cumulative verified set and
native JDK build must pass fork CI at the exact proposed head. Retained default
assumptions and trusted native/serialization boundaries must be disclosed.
A source file with correct existing annotations can join CI without a source edit.
An annotation opt-in or clean body check alone does not establish completeness.

Merge the stack from the bottom up. After merging a parent, retarget its child
to the surviving base; if squash/rebase merging changes ancestry, rebase the
child and review the resulting diff. Refresh the matching CF branch and pin
when it changes, then rerun CI before considering that new head complete.
No PR is automatically merged or sent upstream by this roadmap.

CI also runs on pushes to branches matching `codex/nullness-java-lang-*` and
supports manual dispatch for an explicitly selected branch. This provides a check for
stack layers even when GitHub does not queue a pull-request event; the workflow
uses the same branch concurrency group for push and pull-request runs. The
checked-out JDK head and pinned CF revision are recorded in either case.

## Milestones, in priority order

| Milestone | Shared files added | Cumulative target | Deliverable / exit focus |
| --- | ---: | ---: | --- |
| M0: exception foundations | 5 | 5/126 | PR #7; successful fork CI, pending review/merge. |
| [M1: exception follow-up and core interfaces](https://github.com/aosen-xiong/jdk/milestone/1) | 16 | 21/126 | Two dependent PRs; nullable diagnostics, nullable append inputs, generic element propagation and override contracts. |
| [M2: everyday object/value and numeric APIs](https://github.com/aosen-xiong/jdk/milestone/2) | 15 | 36/126 | Three PR groups below; nullable parsing/property inputs, equality, enum bounds, and wrapper consumers. |
| [M3: strings and Unicode](https://github.com/aosen-xiong/jdk/milestone/3) | 14 | 50/126 | Three PR groups; distinguish nullable objects/sequences, nonnull arrays/elements, and internal caches. Review the generated recipes and record binary dependency provenance; generated-source checking remains M7. |
| [M4: remaining exceptions and annotation types](https://github.com/aosen-xiong/jdk/milestone/4) | 46 | 96/126 | Split the 41 exception/error files by ancestry (runtime, bounds, reflective/checked, linkage, VM); annotation declarations form their own PR. |
| [M5: class loading, reflection helpers and modules](https://github.com/aosen-xiong/jdk/milestone/5) | 10 | 106/126 | Two PR groups; nullable lookups, lazy state, class-loader boundaries, and module consumers. |
| [M6: runtime, threads, processes and stack walking](https://github.com/aosen-xiong/jdk/milestone/6) | 20 | 126/126 | Four PR groups; temporal state, callbacks, native effects, and platform dependencies. |
| [M7: platform/generated coverage and integration](https://github.com/aosen-xiong/jdk/milestone/7) | separate denominator | package closure | Check the six platform variants and six Unicode templates/generated outputs in matching build contexts; package-wide and cross-module regression review. |

These are scope targets, not completion claims or date estimates. M2 and M3
prioritize widely used APIs before the remaining simple exception subclasses.
Dependencies may require a small prerequisite PR; update the inventory rather
than silently moving a blocked file out of the denominator.

## Current stack

1. [PR #7](https://github.com/aosen-xiong/jdk/pull/7): `codex/nullness-java-lang`
   targets `master`; five files verified, all 17 CI jobs passed.
2. [PR #9](https://github.com/aosen-xiong/jdk/pull/9):
   `codex/nullness-java-lang-exception-causes` targets `codex/nullness-java-lang`;
   eight more files have passed local checks. Hosted CI is pending.
3. [PR #10](https://github.com/aosen-xiong/jdk/pull/10):
   `codex/nullness-java-lang-interfaces` targets the exception-causes branch;
   all eight interfaces have passed local source/consumer checks, with no Java
   source changes needed. Hosted CI is pending.
4. [PR #11](https://github.com/aosen-xiong/jdk/pull/11):
   `codex/nullness-java-lang-values` targets the interfaces branch; five more
   source files and their consumer contracts are reviewed. All 26 cumulative
   source checks pass locally. Hosted CI remains unverified.

5. [PR #12](https://github.com/aosen-xiong/jdk/pull/12):
   `codex/nullness-java-lang-wrappers` targets the values branch; seven
   wrapper files pass with the cumulative 33-file local check.
6. [PR #13](https://github.com/aosen-xiong/jdk/pull/13):
   `codex/nullness-java-lang-arithmetic` targets the wrappers branch; the
   final three M2 files pass in the cumulative 36-file run with no new suppressions.
7. [PR #14](https://github.com/aosen-xiong/jdk/pull/14):
   `codex/nullness-java-lang-text` targets the arithmetic branch; four public
   text files pass in the cumulative 40-file local check.
8. [PR #15](https://github.com/aosen-xiong/jdk/pull/15):
   `codex/nullness-java-lang-text-helpers` targets the text branch; four helpers
   and a coordinated builder follow-up pass in the cumulative 44-file local check.

9. [PR #16](https://github.com/aosen-xiong/jdk/pull/16):
   `codex/nullness-java-lang-unicode` targets the helper branch; six Unicode sources
   and two coordinated text-helper follow-ups pass in the cumulative 50-file local check.

10. [PR #17](https://github.com/aosen-xiong/jdk/pull/17):
    `codex/nullness-java-lang-runtime-exceptions` targets Unicode; sixteen more
    runtime/bounds exception files pass without source edits or suppressions.

11. [PR #18](https://github.com/aosen-xiong/jdk/pull/18):
    `codex/nullness-java-lang-checked-exceptions` targets the runtime branch; six
    checked/reflection source bodies pass with their existing annotations.

12. [PR #19](https://github.com/aosen-xiong/jdk/pull/19):
    `codex/nullness-java-lang-linkage-errors` targets checked exceptions; thirteen
    linkage errors pass in the complete 85-file local regression.

13. [PR #20](https://github.com/aosen-xiong/jdk/pull/20):
    `codex/nullness-java-lang-vm-errors` targets linkage; five existing VM error
    classes pass, and ThreadDeath receives its missing whole-file opt-in.

14. [PR #21](https://github.com/aosen-xiong/jdk/pull/21):
    `codex/nullness-java-lang-annotations` targets VM errors; all five annotation
    declarations pass, completing M4 source work locally.

CI checkpoint (2026-11-17): the fork's Actions page explicitly says workflows
are not running due to the scale of GitHub Actions usage and require maintainer
re-enablement. REST reports Actions enabled and the workflow active, but manual
dispatch returns HTTP 422, "Actions has been disabled for this repository."
Re-enabling through the repository/workflow APIs did not clear the restriction.
Hosted checks on #9 through #21 remain unverified; the reflection layer has no
claimed hosted result either. The existing PR #7 result remains green. Re-enable
workflows on the fork's Actions page, then run CI for each exact stack head.
M1/M2/M3/M4 remain open pending hosted checks and review/merge.

The current branch enrolls **100/126** shared Java source files. All 100 pass
in cumulative run.QKgSf6 with no errors or warnings under the frozen profile;
source hashes and checker visitation are verified. Seventeen files have nullness
suppressions: StackTraceElement, Enum, Boolean, Integer, Long, String,
StringBuilder, StringBuffer, AbstractStringBuilder, Character, CharacterName,
StringLatin1, StringUTF16, Class, PublicMethods, ClassValue and WeakPairMap.
The other 83 do not. The generated-record and polymorphic-lambda caller fixtures
have separate known/suspected checker-bug suppressions. Private callers do not
inflate JDK coverage. The other 26 shared files remain in M5b/M6, with
platform/generated coverage separately in M7. The pinned Class null-caller
source defect is disclosed below and remains unresolved for upstream readiness.

## Exact shared-source inventory

Every name below denotes `src/java.base/share/classes/java/lang/NAME.java`.
The groups partition all 126 non-package-info Java files exactly once.
`package-info.java` is additionally reviewed for inherited defaults and opt-ins:
it already opts into nullness and initialization, and adds a KeyFor lower-bound
default; it contains no general documented null policy. This study does not
change it or treat its opt-in as evidence that all classes were checked.

| Group | Count | Source names |
| --- | ---: | --- |
| M0 — Exception foundations | 5 | `StackTraceElement`, `Throwable`, `Exception`, `RuntimeException`, `Error` |
| M1a — Optional exception causes and messages | 8 | `ClassNotFoundException`, `NullPointerException`, `ExceptionInInitializerError`, `ReflectiveOperationException`, `LinkageError`, `AssertionError`, `TypeNotPresentException`, `EnumConstantNotPresentException` |
| M1b — Core interfaces | 8 | `Appendable`, `AutoCloseable`, `CharSequence`, `Cloneable`, `Comparable`, `Iterable`, `Readable`, `Runnable` |
| M2a — Object and value foundations | 5 | `Object`, `Enum`, `Record`, `Number`, `Void` |
| M2b — Primitive wrappers | 7 | `Boolean`, `Byte`, `Short`, `Integer`, `Long`, `Float`, `Double` |
| M2c — Arithmetic | 3 | `Math`, `StrictMath`, `FdLibm` |
| M3a — Public text APIs | 4 | `String`, `AbstractStringBuilder`, `StringBuilder`, `StringBuffer` |
| M3b — Text implementation | 4 | `StringCoding`, `StringConcatHelper`, `StringLatin1`, `StringUTF16` |
| M3c — Unicode | 6 | `Character`, `CharacterData`, `CharacterDataPrivateUse`, `CharacterDataUndefined`, `CharacterName`, `ConditionalSpecialCasing` |
| M4a — Remaining exception and error families | 41 | `AbstractMethodError`, `ArithmeticException`, `ArrayIndexOutOfBoundsException`, `ArrayStoreException`, `BootstrapMethodError`, `ClassCastException`, `ClassCircularityError`, `ClassFormatError`, `CloneNotSupportedException`, `IllegalAccessError`, `IllegalAccessException`, `IllegalArgumentException`, `IllegalCallerException`, `IllegalMonitorStateException`, `IllegalStateException`, `IllegalThreadStateException`, `IncompatibleClassChangeError`, `IndexOutOfBoundsException`, `InstantiationError`, `InstantiationException`, `InternalError`, `InterruptedException`, `LayerInstantiationException`, `NegativeArraySizeException`, `NoClassDefFoundError`, `NoSuchFieldError`, `NoSuchFieldException`, `NoSuchMethodError`, `NoSuchMethodException`, `NumberFormatException`, `OutOfMemoryError`, `SecurityException`, `StackOverflowError`, `StringIndexOutOfBoundsException`, `ThreadDeath`, `UnknownError`, `UnsatisfiedLinkError`, `UnsupportedClassVersionError`, `UnsupportedOperationException`, `VerifyError`, `VirtualMachineError` |
| M4b — Annotation declarations | 5 | `Deprecated`, `FunctionalInterface`, `Override`, `SafeVarargs`, `SuppressWarnings` |
| M5a — Classes and reflection helpers | 4 | `Class`, `PublicMethods`, `ClassValue`, `WeakPairMap` |
| M5b — Loading, packages and modules | 6 | `ClassLoader`, `AssertionStatusDirectives`, `Package`, `NamedPackage`, `Module`, `ModuleLayer` |
| M6a — System and runtime | 5 | `System`, `Runtime`, `RuntimePermission`, `SecurityManager`, `Compiler` |
| M6b — Threads and thread-local state | 4 | `Thread`, `ThreadGroup`, `ThreadLocal`, `InheritableThreadLocal` |
| M6c — Processes and shutdown | 6 | `Process`, `ProcessBuilder`, `ProcessHandle`, `ProcessHandleImpl`, `ApplicationShutdownHooks`, `Shutdown` |
| M6d — Stack walking | 5 | `StackWalker`, `StackStreamFactory`, `StackFrameInfo`, `LiveStackFrame`, `LiveStackFrameInfo` |

## Additional package sources

M7 also covers `ProcessEnvironment.java`, `ProcessImpl.java`, and
`Terminator.java` under **each** of `src/java.base/unix/classes/java/lang/` and
`src/java.base/windows/classes/java/lang/` (six physical sources, three APIs).
Do not combine incompatible platform roots in one patch. Configure matching
Unix and Windows builds and retain the generated roots and module arguments.

The six `make/data/characterdata/CharacterData{00,01,02,03,0E,Latin1}.java.template`
inputs produce package members absent from the shared-source inventory. Review
the templates and check their generated Java outputs; preserve generation so
annotations survive a rebuild. Inventory any other generated package members
from the configured builds before closing M7. Generated copies do not inflate
the 126-file shared-source denominator.

A full native build passing does not mean those bodies received nullness checking.
If a compiler context, checker crash, or unresolved contract blocks a file, record
its exact source, failure signature, reproducer/log, and next action here. A
blocked file remains in its milestone and is never reported as verified.

## Exception follow-up evidence

The source oracle is the Javadoc in the pinned files, plus the inherited
Throwable contracts. All eight files already opt into nullness; none has an
opt-out. The only production edits in this follow-up are:

| File / position | Evidence and decision |
| --- | --- |
| `ClassNotFoundException.getException()` return | Javadoc explicitly returns null if no loading exception exists. Add `@Nullable`; baseline body check reported `return.type.incompatible`. |
| `NullPointerException.getMessage()` return | Javadoc explicitly says the detail message may be null. Add `@Nullable`. |
| `NullPointerException.getExtendedNPEMessage()` return | Private native method documentation explicitly permits null when not applicable. Add `@Nullable`; native behavior is trusted, not checked by the Java processor. |
| `NullPointerException.extendedMessage` field | Initially null and may cache a null native result. Add `@Nullable` based on the internal implementation. |
| `ExceptionInInitializerError` | Existing nullable saved-exception return and message/cause inputs agree with Javadoc. Serialization guards the optional cause. No source change. |
| `ReflectiveOperationException`, `LinkageError` | Existing nullable message/cause inputs agree with explicit cause documentation and inherited Throwable contracts. No source changes. |
| `AssertionError` | Object detail uses string conversion (including null); message/cause constructor explicitly permits null. Existing annotations preserved. |
| `TypeNotPresentException`, `EnumConstantNotPresentException` | Nullable cause is already encoded where documented. Name/type nonnull defaults are retained assumptions: their docs describe names/types but give no explicit null policy. No source changes. |

The untouched NullPointerException body passed despite its missing contracts.
This is why documentation and caller tests are required in addition to body
checks. CF's `ExceptionCauseNullness` tests valid nullable constructors, guarded
results, a nullable override, and three invalid dereferences. The source job
checks the cumulative enrolled files separately using the shared
`checker/bin-devel/typecheck-jdk.sh`; its explicit workflow list is the regression
manifest. No new suppression or executable code change is introduced.

## Core interface evidence

All eight complete files, including CharSequence's local iterator classes,
already have nullness opt-ins and suitable annotations. No Java source edit,
new qualifier, or suppression is needed for this layer.

| Interface | Reviewed contract and validation |
| --- | --- |
| `Appendable` | Both CharSequence inputs explicitly allow null, treated as "null". Existing Nullable inputs and nonnull fluent returns agree. Test nullable calls and reject an overriding method that narrows the input. |
| `Readable` | read explicitly throws NPE for a null buffer. Preserve/test its nonnull parameter. |
| `Comparable` | Class/method Javadoc reject compareTo(null). Preserve/test its nonnull bound and argument. |
| `Iterable` | Nonnull iterator/spliterator and callback, with element nullness carried by T. Nullable T works through iterator, forEach, and spliterator under both checked profiles; no extra explicit bound is needed. |
| `CharSequence` | Subsequence, string and stream results describe concrete results. Preserve/test nonnull results. compare's nonnull inputs are retained default assumptions backed by requireNonNull, not an explicit documented null clause. Local iterator callbacks inherit nonnull action contracts. |
| `AutoCloseable`, `Runnable` | No reference parameter or return on close/run; existing signatures are sufficient. Receiver checking does not establish resource lifecycle or concurrency correctness. |
| `Cloneable` | Marker interface has no declared methods; full-file scope review requires no qualifier edit. |

All eight source checks finish with exit 0 and no warnings or nullness
suppressions. CF's `CoreInterfaceNullness` fixture matches six expected errors
in JSpecify and ordinary nullness/purity modes, alongside valid nullable append
inputs and guarded nullable elements. The preceding 13 source files are
unchanged from the validated parent; CI checks all 21 together.

## Object and value foundations (M2a)

New layer: `codex/nullness-java-lang-values`, based on
`codex/nullness-java-lang-interfaces` (#10). Scope: Object, Enum, Record, Number,
and Void. Existing qualifiers remain intact; the only JDK source edit is one
method-scoped suppression and its invariant explanation in Enum.

| File | Documentation oracle and decision |
| --- | --- |
| `Object` | equals explicitly accepts null and returns false; retain Nullable plus the existing conditional nonnull postcondition. getClass, clone and toString return concrete nonnull results on normal return. Native behavior is trusted. wait/notify have no reference parameters/results. |
| `Enum` | Name/class/result contracts are nonnull; equals accepts null; compareTo and valueOf reject null. EnumDesc.of explicitly rejects null class/name, and describeConstable uses empty Optional rather than null. Preserve these contracts and all nested scopes. |
| `Record` | Preserve nullable equals input and nonnull toString. Nullability of individual record components belongs to each record declaration. A compiler-generated equals consumer exposes the checker issue below. |
| `Number` | Conversions have primitive results and no reference arguments. Concrete byte/short conversion bodies pass with existing annotations. |
| `Void` | TYPE denotes the nonnull Class object for void. No additional nullable position or executable body change is warranted. |

Enum.getDeclaringClass has one `nullness:return.type.incompatible` false
positive: Class.getSuperclass is nullable in general. [JLS 17 §§8.9 and
8.9.1](https://docs.oracle.com/javase/specs/jls/se17/html/jls-8.html#jls-8.9)
establish that an enum constant's class extends Enum or its declaring enum
class, so its superclass cannot be null. Keep the public nonnull result and
suppress only this return diagnostic on that method. Removing only the key in
an isolated full-source checkout restores exactly one diagnostic. No executable
syntax changed, as confirmed by an annotation-normalized AST comparison.

CF fixtures ObjectValueNullness and RecordValueNullness pass under JSpecify
and ordinary nullness/purity modes with five and three expected invalid-caller
diagnostics respectively. The record workaround below is isolated from those
negative controls and passes unused-suppression auditing. The original checker
JARs remain pinned; a tentative checker implementation change was set aside,
not included or used to claim passing validation.

## Known checker issue: generated record equality

With the frozen c12ce38daa checker implementation and JDK 17.0.14,
`record Item(@Nullable String name) {}` generates an `equals(Object)` whose
argument is incorrectly treated as nonnull. `item.equals(null)` produces
`nullness:argument.type.incompatible` in both JSpecify and ordinary nullness
modes. Calling through a `Record` reference is accepted. `Record.equals` already
has the documented nullable argument; changing the JDK declaration cannot
repair this generated-member discrepancy.

The original failing caller and both logs are retained in the study evidence.
Following the requested bug-first workflow, the failure was documented before
adding a diagnostic-specific suppression around the single generated-equals
caller in its own helper method.
The direct Record contract and invalid-consumer controls remain unsuppressed.
Removing only the helper suppression restores the false positive in a scratch
fixture. Both JSpecify and ordinary nullness/purity profiles pass with it present.
Recheck and remove the suppression after a checker fix; do not treat the
suppressed caller as independently verified. No checker implementation fix is
included in this stack layer.

## Primitive wrappers (M2b)

`codex/nullness-java-lang-wrappers` builds on the value foundations (#11).
The seven complete files, including their nested cache classes, are reviewed and
checked. Each changed source has a separate annotation commit. The profile and
checker implementation remain frozen; no executable behavior changes.

| Position | Documentation oracle and change |
| --- | --- |
| `Integer`, `Long`, `Float`, `Double`: `resolveConstantDesc` lookup parameter | Each override documents the parameter as ignored and the result as the instance itself. Add Nullable to the ignored argument; preserve the nonnull return. Previously four valid null callers were rejected; all four now pass. |
| `Byte`, `Short`, `Integer`, `Long`: `Cache.archivedCache` | Internal comments and initialization show an optional CDS array before fallback allocation. Add Nullable to the array reference, preserving nonnull element types and the final nonnull cache. This is implementation-derived; native archive contents and loop-fill completeness remain trusted under the first-pass profile. |
| `Boolean` parsing/valueOf and all equals methods | Existing Nullable inputs encode documented null-to-false behavior. Preserve Boolean's conditional nonnull contracts; caller refinements are exercised. |
| `Integer.getInteger`, `Long.getLong` | Existing Nullable names/results and PolyNull boxed-default relations match the documented default behavior. Test nullable and nonnull defaults separately. |
| Numeric parsing, constructors, valueOf and compareTo | Preserve nonnull preconditions: numeric null strings are rejected with NumberFormatException or NPE, and Comparable rejects null. Explicit rejection is not normal null acceptance. decode's nonnull input remains a disclosed default assumption where its Javadoc lacks an explicit null clause. |
| Formatting, boxing, TYPE and describeConstable results | Preserve the documented nonnull String/wrapper/Class/Optional results. Primitive-only methods need no extra qualifier. |

Three source methods need suppressions for intentional exception translation.
Boolean.getBoolean, Integer.getInteger(String,Integer), and
Long.getLong(String,Long) explicitly accept null names. They call
System.getProperty, catch its documented NPE, and return false/the default.
The Nullness Checker still enforces System.getProperty's nonnull argument.
Suppress only `nullness:argument.type.incompatible` on those methods.
Boolean also needs `nullness:contracts.conditional.postcondition.not.satisfied`:
its true result implies a nonnull name, but the analysis does not recover that
relation across the catch. Preserve the existing sound conditional contract.
This is documented as an analysis limitation, not a demonstrated checker defect.

The limitation was recorded before adding suppressions. Removing each of the
four keys alone, holding the other source changes and profile fixed, restores
exactly its corresponding diagnostic. All seven source files pass with unused
suppression auditing. Annotation-normalized AST comparisons confirm unchanged
executable syntax and preservation of the other checker annotations.

The matching CF branch contains WrapperValueNullness (17 deliberate invalid
caller diagnostics) and WrapperConstantNullness (four valid ignored-null lookup
calls plus descriptor consumers). These fixtures exercise JSpecify and ordinary
nullness/purity profiles. Tests and the runner remain entirely in CF.
No initialization, purity, native implementation, or mathematical accuracy proof
is claimed by these source checks.

## Arithmetic (M2c)

`codex/nullness-java-lang-arithmetic` builds on the primitive wrappers (#12).
The scope is Math, StrictMath and FdLibm. The only source change is an explicit
class-level AnnotatedFor("nullness") and import on FdLibm, following the
whole-file annotation policy. Math and StrictMath already have appropriate
opt-ins. No nullable qualifier, suppression, or executable change is added.

The class/method Javadoc describes primitive mathematical operations; a syntax
inventory confirms all 175 method declarations across these three files have
primitive parameters and primitive results. Math/StrictMath's random() docs
promise a reused generator, and their holder fields initialize with new Random.
FdLibm's coefficient arrays are initialized by primitive-array literals. These
internal nonnull defaults are supported by implementation evidence. Native
StrictMath operations and numerical accuracy remain outside nullness checking.

All three complete source files pass individually. FdLibm includes four nested
algorithm classes: Exp, Cbrt, Hypot and Pow. A scratch control injects one null
dereference into each of those and the enclosing class, requiring five separate
diagnostics to confirm scope coverage. The original bodies remain unchanged,
as checked by annotation-normalized AST comparison.

CF's ArithmeticNullness exercises primitive and guarded boxed callers,
including all four public StrictMath entry points to FdLibm, and rejects four
unsafe nullable unboxings. Both JSpecify and ordinary nullness/purity consumer profiles match those four
expected errors. All 36 cumulative source invocations pass with no warnings or new suppressions. M2's 15 files are now enrolled;
its hosted CI/review gate remains open, and 90 shared files plus the separately
inventoried platform/generated sources remain before package completion.

## Public text APIs (M3a)

`codex/nullness-java-lang-text` builds on arithmetic (#13), covering String,
AbstractStringBuilder, StringBuilder and StringBuffer. Their class documentation
explicitly rejects null arguments unless a method says otherwise. This supplies
the default public precondition; exceptional null-tolerant methods are reviewed
against that policy and inherited Appendable/CharSequence contracts.

| Position | Evidence and decision |
| --- | --- |
| `String.resolveConstantDesc` lookup | Documented ignored, returning this; add Nullable on the concrete Lookup argument. Removing this annotation alone restores exactly one otherwise-valid caller error. |
| `AbstractStringBuilder.append(AbstractStringBuilder)` and its StringBuffer override | The internal forwarding path implements the documented null-to-"null" StringBuffer append behavior and explicitly checks null. Add Nullable to both parameters. |
| `StringBuffer.toStringCache` | Field documentation says it is cleared on mutation; 27 explicit null writes confirm its optional state. Add Nullable to the field; public toString stays nonnull. |
| Internal designated `String.join` elements and Iterable join buffer | The capacity array contains null spare slots. Annotate nullable element types in the helper parameter and array creation. Correct the private comment to require nonnull elements only in [0,size), which is the range the helper reads. The public join still accepts nullable elements and returns a nonnull String. |
| Equality, valueOf, append/insert, join and formatting | Preserve documented nullable object/sequence inputs, nullable join/format elements and nullable locale. Delimiters, array/Iterable references, constructors, replacement strings and comparison inputs retain nonnull preconditions. The formatting varargs array reference retains the class-policy default; element nullness is separate. |
| transform | Existing R carries the callback result's nullness; nullable-result consumer tests pass without adding a bound or weakening nonnull function inputs. |
| Void marker parameters and rangeCheck result | Already nullable through the frozen CF qualifier's DefaultFor(Void.class); no redundant annotation is added. |

Six new suppression annotations contain nine diagnostic-key occurrences:

- String.split: `return.type.incompatible` and
  `toarray.nullable.elements.not.newarray`. The result array and copied subList
  both have resultSize elements, so toArray cannot append a null sentinel.
- Internal String.join: `dereference.of.nullable` at three reads. Callers fill
  every slot in [0,size) with nonnull String.valueOf results; the checker does
  not express this initialized-prefix invariant. Null spare capacity is honestly
  represented rather than hidden with an assignment suppression.
- String.newStringNoRepl/getBytesNoRepl: `throwing.nullable`. Coding helpers wrap
  failures in IAE with a nonnull coding cause, but Throwable.getCause remains
  nullable in general. This trusts the expected coding-provider protocol;
  arbitrary provider exceptions are not proven to have a cause.
- StringBuilder/StringBuffer.readObject: `argument.type.incompatible` and
  `dereference.of.nullable` in each hook. Their documented serialized forms and
  writeObject bodies supply a nonnull char array. This is a trusted format
  boundary: malformed or substituted streams can violate it and are not proven
  null-safe by these suppressions.

These findings were documented before suppressions. No new checker implementation
bug is established by them and no checker fix is included. Each key is removed
alone in the full-source control checkout; the intended diagnostic returns,
including all three prefix reads and the toArray warning (which fails under
Werror). The checker and all other options stay frozen. Existing annotations
for other checkers and executable syntax are unchanged by AST comparison.

All four files pass individually with unused-suppression auditing. CF's
TextContractNullness and TextModernNullness match 11 and four deliberate invalid
caller diagnostics in both JSpecify and ordinary nullness/purity modes. Valid
nullable contents, generic results and ignored lookups are accepted. All 40 cumulative
source invocations pass without warnings. M3 still has four
text helpers and six Unicode shared files; generated Unicode outputs remain M7.

## Text implementation helpers (M3b)

`codex/nullness-java-lang-text-helpers` builds on the public text APIs (#14).
It adds complete nullness opt-in to StringCoding, StringConcatHelper, StringLatin1
and StringUTF16, preserving StringCoding's other checker names. Nested line,
character and code-point spliterators are included. The four new files add
31 Nullable positions, with no suppressions in those helpers themselves.

| Position | Evidence and decision |
| --- | --- |
| StringConcatHelper object inputs (four) | The helper's string-conversion documentation and implementation accept null and produce a concrete String. Annotate simpleConcat's two arguments, newStringOf and stringOf. Preserve nonnull results, including defensive handling of a null toString result. |
| StringConcatHelper prepend prefixes (seven) | StringConcatFactory initializes and resets its optional constant to null and passes it through the prepender pipeline. Annotate only prefix; converted String values, suffixes and byte buffers remain nonnull. This is internal caller evidence. |
| Latin1/UTF16 replace, trim, strip, stripLeading and stripTrailing results | Null means reuse the original String. Internal comments/branches and guarded public String callers establish the sentinel contract; add Nullable to helper results without weakening public String results. |
| Latin1.toBytes(int[],off,len), UTF16.compress(char[]/byte[]) | Failed Latin1 conversion returns null. Annotate the array reference only; primitive elements are unaffected. String and builder callers are checked against the corrected returns. |
| Concrete trySplit overrides | The Spliterator contract permits null when no split is available. Annotate two Latin1 and three UTF16 implementations. Keep action parameters nonnull and ordinary streams/arrays nonnull. |
| StringCoding and remaining primitives | Nonnull byte arrays are indexed/copied and primitive values returned. Full source checking needs opt-in but no new nullable position. |

The corrected compression contract requires one coordinated follow-up in
AbstractStringBuilder.initBytes. During deserialization it temporarily stores a
nullable compression result in value, tests it, and either returns with a nonnull
value or fills a nonnull UTF16 fallback. Preserve the normally nonnull field and
suppress only `nullness:assignment.type.incompatible` on that helper, with an
explanation of the temporary state. Removing only the key restores one error.
Initialization and arbitrary reentrant/malformed deserialization remain outside
this pass. No extra postcondition is added because callers already use the
field's nonnull declaration. StringUTF16 and the builder follow-up form a
dependency pair; the combined PR head is the regression target, while each
source has its own review commit.

A clean concatenation-helper body did not reveal its missing input contracts.
The CF-owned `checker/tests/jdk-source/java.base/java/lang/TextHelperContracts.java`
now checks package-private callers through the existing typecheck-jdk.sh. Its
separate invocation adds that source root using JDK_EXTRA_SOURCE_ROOTS, after
the ordinary shared-source root. No fixture is copied into JDK and the JDK
source checks retain their original patch context. The valid caller passes;
removing the eleven new concatenation-input qualifiers restores exactly eleven
argument errors. Public TextHelperPublicNullness matches four invalid caller
cases in both JSpecify and ordinary nullness/purity profiles.

All five changed sources pass individually and their annotation-normalized AST
audits preserve executable syntax and other checker annotations. The cumulative
44-file source run passes with no errors or warnings. M3 has six shared
Unicode files remaining; generated Unicode templates/outputs are still M7.

## Unicode shared sources (M3c)

`codex/nullness-java-lang-unicode` builds on the text-helper layer (#15).
Character, CharacterData, CharacterDataPrivateUse, CharacterDataUndefined,
CharacterName and ConditionalSpecialCasing are now opted in and individually
checked, including Character's nested block/script/cache classes and the
conditional-casing Entry class. The two text helpers receive coordinated local
suppression follow-ups. Each changed source has a separate review commit; use
the combined head for regression because the new return contracts affect callers.

| Position | Contract evidence and decision |
| --- | --- |
| Character.getName | Javadoc explicitly permits null for unassigned codepoints; add Nullable to String result. Retain existing Nullable UnicodeBlock.of results and equals inputs. |
| Character.UnicodeBlock.blocks | Its literal includes 54 null gaps. Annotate component nullness, keeping the array itself nonnull. |
| CharacterCache.archivedCache | Optional CDS archive; annotate array reference only, preserving the initialized nonnull cache. |
| CharacterData.toUpperCaseCharArray | Base implementation returns null for planes without a mapping override; annotate array reference. Keep CharacterData.of's singleton result nonnull. |
| CharacterName | The SoftReference cache itself is initially absent; mark its reference nullable. getName can have no table entry; mark the String result nullable. getInstance still returns a nonnull cache object. |
| ConditionalSpecialCasing | Absent mapping means a nullable char-array reference from lookUpTable and toLowerCaseCharArray. Null Entry.lang means a language-independent rule: annotate field, constructor parameter and getter. Mapping arrays, String and Locale arguments remain nonnull. |
| Primitive-only data subclasses | Full-file opt-in; no new nullable positions or suppressions. |

The six files add eleven Nullable positions, two new opt-ins and three extended
opt-in lists. Other checker annotations and executable syntax are preserved in
all eight changed files by annotation-normalized AST audits.

Four suppression keys were documented before adding them, and individually
removed in a scratch checkout to restore exactly one diagnostic each:

- Character.toUpperCaseCharArray: one return diagnostic. Its BMP assertion selects
  the generated Latin1/00 implementations, whose templates return a concrete
  array. Preserve its narrower documented result and the base nullable result.
- CharacterName's anonymous resource action: one return diagnostic. The build's
  Gendata.gmk installs the required uniName.dat resource at that exact module path.
  Missing/corrupt images remain outside this trusted packaging boundary.
- StringLatin1/StringUTF16: one local mapLen-initializer dereference diagnostic
  each. The preceding ERROR result guarantees a conditional mapping for the
  same String/index/Locale lookup. The helper's generally nullable result remains
  accurately annotated; no method-wide suppression is needed.

These are range/dispatch, packaging and relational limitations; no new checker
implementation bug or crash is claimed. The study assumes assertions enabled.
Generated CharacterData bodies remain binary dependencies from the recorded JDK17
image in this shared-source profile. Their matching source recipes were reviewed
in make/modules/java.base/gensrc/GensrcCharacterData.gmk, but the six templates and
outputs are still M7 coverage. No native build was run locally.

CF's UnicodeNullness matches ten deliberate invalid calls in both JSpecify and
ordinary nullness/purity modes. Before the new getName qualifier, its unsafe
caller was incorrectly accepted (nine diagnostics); afterwards all ten appear.
UnicodeHelperContracts passes through the shared script's additional-source-root
interface. Removing Entry's nullable language parameter alone rejects exactly
one valid private caller. Both fixtures remain in CF, with the matching branch
pinned by this layer's CI.

The cumulative 50-file run passes with no errors or warnings. M3's shared-source
annotation work is complete locally; hosted validation/review and M7 generated coverage
remain open. The next shared-source milestone is M4's 41 remaining exception/error
files and five annotation declarations, in related API groups.

## Runtime and bounds exceptions (M4a.1)

`codex/nullness-java-lang-runtime-exceptions` builds on Unicode (#16). The
sixteen files below already have complete nullness opt-in and appropriate
annotations. Documentation/body review, source checking and caller controls
justify enrollment without manufacturing Java source edits.

- ArithmeticException, ArrayStoreException, ClassCastException,
  IllegalMonitorStateException, IllegalThreadStateException,
  NegativeArraySizeException and NumberFormatException: retain nullable message
  inputs and inherited optional message/cause results.
- IllegalArgumentException, IllegalCallerException, IllegalStateException,
  LayerInstantiationException, SecurityException and UnsupportedOperationException:
  retain nullable message/cause overloads. All six explicitly permit absent cause;
  IllegalCallerException/LayerInstantiationException also explicitly permit null
  messages. For subclasses whose local message text is silent, direct superclass
  delegation supports the existing optional-message convention as secondary
  implementation evidence, not an invented explicit local promise.
- IndexOutOfBoundsException, ArrayIndexOutOfBoundsException and
  StringIndexOutOfBoundsException: retain optional message constructors and
  primitive index overloads. Do not strengthen getMessage based on a particular
  constructor. NumberFormatException's internal factories keep nonnull results
  and input preconditions; forInputString's null policy is unspecified locally
  and retained as an internal assumption, with guarded parse callers.

All sixteen complete source files pass with no suppressions. The prior fifty
sources and frozen checker binaries are unchanged; no additional whole-set run
was needed for this enrollment-only layer. CI runs the cumulative 66-file list.
CF's RuntimeExceptionNullness checks nullable message inputs across all sixteen,
twelve message/cause and cause-only overload calls, four primitive-index
constructors, guarded optional results and five deliberately invalid calls.
Both JSpecify and ordinary nullness/purity profiles match all five diagnostics.
The matching CF branch is pinned; no fixture or harness is added to JDK.

M4 now has six checked/reflection exceptions, thirteen linkage errors, six
VM/thread-death errors and five annotation declarations remaining (30 files).

## Checked and reflection exceptions (M4a.2)

`codex/nullness-java-lang-checked-exceptions` builds on the runtime group (#17).
CloneNotSupportedException, IllegalAccessException, InstantiationException,
InterruptedException, NoSuchFieldException and NoSuchMethodException all have
existing complete nullness opt-in and nullable detail-message constructors.
Their no-arg/message bodies delegate directly to Exception or
ReflectiveOperationException. Preserve inherited optional getMessage/getCause
results. Local message text is silent on null, so direct superclass delegation
supports the preserved convention as implementation evidence. No annotation,
executable source or suppression changes are needed in these six files.

All six complete source checks pass. The preceding 66 source contents and
checker binaries are unchanged; CI runs the cumulative 72-file set. The matching
CF fixture checks six nullable-message constructors, guarded optional results
and six invalid accessor dereferences. Both JSpecify and ordinary nullness/purity
profiles match exactly those six diagnostics.
M4 has thirteen linkage errors, six VM/thread-death errors and five annotation
declarations remaining (24 files).

## Linkage errors (M4a.3)

`codex/nullness-java-lang-linkage-errors` builds on the checked exceptions (#18).
The thirteen-file group is AbstractMethodError, BootstrapMethodError,
ClassCircularityError, ClassFormatError, IllegalAccessError,
IncompatibleClassChangeError, InstantiationError, NoClassDefFoundError,
NoSuchFieldError, NoSuchMethodError, UnsatisfiedLinkError,
UnsupportedClassVersionError and VerifyError.

Twelve already have correct nullness opt-in and nullable message constructors;
all pass unchanged. BootstrapMethodError receives one whole-file opt-in and
four Nullable input positions: messages in the one/two-argument constructors
and causes in the one/two-argument constructors. Its cause Javadoc explicitly
allows null. The locally unspecified message policy follows the superclass's
optional-message convention and direct delegation as implementation evidence.
There is no new suppression or executable change; the AST audit passes.

BootstrapMethodError's opted-in body passed even without these input qualifiers,
but the caller rejected four valid arguments. After annotation, the caller
accepts all thirteen nullable-message constructions and both cause-overload
calls while still producing exactly four intentional invalid-call diagnostics.
JSpecify and ordinary nullness/purity runs agree. This is another missing-contract
case, not a checker defect. Tests remain in the matching CF branch.

All thirteen files pass individually and in the complete 85-file regression. M4 then has six VM/thread-death errors and five annotation declarations
remaining. Hosted CI and native build results remain unverified for this layer.

## VM and thread-death errors (M4a.4)

`codex/nullness-java-lang-vm-errors` builds on linkage (#19). It enrolls
VirtualMachineError, InternalError, OutOfMemoryError, StackOverflowError,
UnknownError and ThreadDeath. Only ThreadDeath changes: add whole-file nullness
opt-in. It has a no-argument constructor and no new nullable contract. The other
five preserve existing Nullable messages; VirtualMachineError/InternalError
also preserve explicitly permitted nullable cause overloads. Locally silent
message text follows the documented superclass convention and direct delegation
as implementation evidence. No suppressions or executable changes are added.

The five unchanged sources pass; ThreadDeath passed its isolated preflight and
its annotation-normalized AST audit and its publication-checkout check.
CF's VmErrorNullness exercises abstract-base constructor delegation, concrete
nullable messages/causes, guarded accessors and three unsafe dereferences. Both
profiles match those three diagnostics. This does not test VM resource exhaustion,
thread termination, concurrency or native creation of errors. The previous 85
source contents are unchanged, and CI runs all 91. All 41 M4 exception/error
files are then covered locally; its five annotation declarations remain.

## Annotation declarations (M4b)

`codex/nullness-java-lang-annotations` builds on VM errors (#20). Deprecated,
FunctionalInterface, Override, SafeVarargs and SuppressWarnings all pass their
complete declaration checks. Only FunctionalInterface and SafeVarargs change:
add whole-declaration nullness opt-in, one source per commit. Both AST audits
preserve executable/declaration syntax and existing meta-annotations. No nullable
qualifier, suppression, retention/target change or executable body is introduced.

Deprecated.since returns its nonnull version String (default empty), and
SuppressWarnings.value returns a nonnull array of nonnull warning names.
Their documented values and [JLS17 9.7.1's element-value rules](https://docs.oracle.com/javase/specs/jls/se17/html/jls-9.html#jls-9.7.1)
support these defaults. forRemoval is primitive. The three marker declarations
have no declared methods; checking them is declaration coverage, not execution
coverage. Malformed proxy/manual implementations are not proved safe by the
annotation syntax rule.

The CF-owned AnnotationElementNullness fixture accepts dereferencing ordinary
String/array/component results and rejects two nullable annotation receivers.
Both profiles match those two errors. The five source checks pass, with no
additional suppression. The prior 91 checked source contents are unchanged;
CI now runs 96. M4's 46 shared files are complete locally, while hosted validation
and review remain open. M5 next covers Class, PublicMethods, ClassValue,
WeakPairMap, ClassLoader, AssertionStatusDirectives, Package, NamedPackage,
Module and ModuleLayer. M6/M7 remain as inventoried above.

## Reflection metadata and cache helpers (M5a)

`codex/nullness-java-lang-reflection-foundations` builds on the annotation layer
([PR #21](https://github.com/aosen-xiong/jdk/pull/21)). It covers Class,
PublicMethods, ClassValue and WeakPairMap; each changed source has its own commit.
Contracts were derived first from the pinned public/inherited Javadoc and then
from private helper comments, callers and the matching HotSpot native sources.
No executable JDK behavior or checker implementation changes are included.

| Source | Contract decisions and boundaries |
| --- | --- |
| Class | Nullable results for module lookup, record-component arrays, annotated superclass and permitted-subclass arrays. Elements remain nonnull. Model absent native metadata and lazy caches, preserving successful allocation and enum-value guarantees. Explicit unconstrained Class token bounds use Nullable Object; this does not make Class objects nullable. |
| PublicMethods | Nullable linked-list tails, filtered results and list/list merges; Object.equals admits null. The single-Method merge still promises a nonempty result. |
| ClassValue | Sparse cache components and absent probes are nullable. Bare T propagates the client's chosen nullness through compute/get; erased backing storage can hold null. match establishes a nonnull entry on true, and castEntry preserves reference nullness with PolyNull. |
| WeakPairMap | Documented keys/stored values are nonnull; absent/previous values and collected weak-key results are nullable. Nullable mapping results preserve the existing PolyNull relation. Explicit NonNull Object generic bounds preserve erasure. |

Class's inherited isAnnotationPresent parameter bound remains unchanged.
Unspecified public null parameter-array/element behavior retains the existing
assumptions; getMethod's explicitly documented null array remains accepted.
No general package null policy was invented from defensive checks. Native
getConstantPool, raw annotation bytes and executable type-annotation bytes admit
absence even when unchecked dependency contracts would hide a missing qualifier.

The annotation-normalized AST audit preserves executable syntax and declarations,
with only redundant Object generic bounds normalized in WeakPairMap. Existing
other-checker annotations remain intact. Added sites are 157 Nullable, 23 NonNull,
2 PolyNull, 4 EnsuresNonNullIf and 2 RequiresNonNull; the existing native isArray
conditional contract gains two reviewed expressions. Two new whole-file opt-ins
and one existing opt-in extension cover the helpers. These are CF contracts in
JSpecify mode, not a portable JSpecify-only annotation vocabulary.

Thirteen new diagnostic-key occurrences occupy eleven suppression locations
(seven new annotations, four extensions). Each limitation was recorded before
suppression, and removing each key independently restores its intended errors:

- WeakPairMap lambda forwarding reproduces a suspected checker polymorphic
  inference defect in a small test without a patched JDK. Direct forwarding
  passes; equivalent lambda forwarding reports one return incompatibility.
  Preserve the API and suppress that diagnostic. A separate argument key covers
  the two weak keys kept alive by the enclosing reachability fences.
- PublicMethods' nonempty-list invariant needs one return key (three errors).
  ClassValue's erased T storage needs one return key and one local inference key.
- Class has two array-loop alias diagnostics, allocation/Unsafe non-returning
  dependency gaps, a heterogeneous native tuple slot, paired class-loader
  assertion maps, and Method.invoke's missing nullable static-receiver contract.
  The reviewed contracts remain precise; each diagnostic has a specific scope.
- **Pinned JDK source defect:** Class.isOpenToCaller can pass a null caller module
  to Module.isOpen for an unconditionally open package. This is not a checker
  false positive. A copied-branch runtime probe reproduces the NPE; no JNI
  end-to-end test or rebuilt JDK was run. Its suppression is explicitly labeled
  as a source defect, and the path remains unresolved for upstream readiness.

Eight additional contract-removal controls validate the new conditional facts
and getter preconditions; none relies on a postcondition suppression. CF owns
ReflectionClassNullness (eight deliberate invalid calls), ClassValueNullness
(three), and PolymorphicLambdaForwarding (two); both JSpecify and ordinary
nullness/purity profiles match exactly. The old Class source misses all four
unsafe uses of the newly documented nullable results. Private helper callers
pass through the same typecheck-jdk.sh interface and ten scratch negative callers
are rejected. No tests or new runner are added to this JDK repository.

All four individual source checks pass with unused-suppression auditing.
Cumulative run.QKgSf6 passes all 100 explicit source targets with matching source
hashes, zero errors/warnings, no crashes and no truncation. Raw baselines, contracts, source hashes,
caller checks, AST audits and twenty-one removal controls are retained under the
matching CF checkout's checker/build/jdk-typecheck/reflection-foundations-study.
Personal evidence cases NULL-0017 through NULL-0022 retain the reproduced issues
and scoped controls; no general rule assumes arbitrary native or cache safety.
The six loading/package/module files remain in M5b; M6/M7 are unchanged.

## Package completion and upstream delivery

M7 closes only after every inventoried file is verified or has an explicitly
accepted exclusion (with rationale), no unexplained crash remains, and the
cumulative source/consumer checks pass against one recorded profile. Reaudit
suppressions with removal controls, review default assumptions, verify relevant
outside consumers, and test the final native builds. Report coverage and any
accepted exclusions separately; do not call exclusions fully annotated coverage.

Prepare upstream EISOP PRs by mature API group within this package, carrying
annotation changes and accessible evidence. Keep fork-only study configuration
separate when upstream does not want it. Upstream publication requires a later
request; green fork CI alone is not approval to submit or merge upstream.

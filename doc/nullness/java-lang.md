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
| [M7: platform/generated coverage and integration](https://github.com/aosen-xiong/jdk/milestone/7) | separate denominator | package closure | Check the six platform variants, six Unicode templates and VersionProps template/output in matching contexts; package-wide and cross-module regression review. |

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

15. [PR #22](https://github.com/aosen-xiong/jdk/pull/22):
    `codex/nullness-java-lang-reflection-foundations` targets annotations; four
    reflection/cache sources pass in the cumulative 100-file local regression.

16. [PR #23](https://github.com/aosen-xiong/jdk/pull/23):
    `codex/nullness-java-lang-loading-modules` targets reflection foundations;
    six loading/module sources and coordinated follow-ups pass the 106-file local gate.

17. [PR #24](https://github.com/aosen-xiong/jdk/pull/24):
    `codex/nullness-java-lang-system-runtime` targets loading/modules; five
    runtime/security files pass the 111-file local gate.

18. [PR #25](https://github.com/aosen-xiong/jdk/pull/25):
    `codex/nullness-java-lang-threads` targets system/runtime; four thread sources
    and a System bridge follow-up pass the 115-file local gate.

19. [PR #26](https://github.com/aosen-xiong/jdk/pull/26):
    `codex/nullness-java-lang-processes` targets threads; six process/shutdown
    sources pass the 121-file local gate, with one Runtime suppression retired.

20. [PR #27](https://github.com/aosen-xiong/jdk/pull/27):
    `codex/nullness-java-lang-stack-walking` targets processes and completes
    the 126-file shared-source inventory locally.

21. [PR #28](https://github.com/aosen-xiong/jdk/pull/28):
    `codex/nullness-java-lang-unix` targets stack walking; all 126 shared
    plus three Unix sources pass in their explicit platform context.

22. [PR #29](https://github.com/aosen-xiong/jdk/pull/29):
    `codex/nullness-java-lang-windows` targets Unix and adds three Windows sources;
    its complete 129-file Windows-context gate passes locally.

23. [PR #30](https://github.com/aosen-xiong/jdk/pull/30):
    `codex/nullness-java-lang-generated` targets Windows and checks six generated
    Unicode classes, with separate 135-file Unix and Windows gates passing.

The current VersionProps layer, `codex/nullness-java-lang-version-props`, targets
#30. Its template has passed local checks; CI must validate the configured
output from the actual native build.

CI checkpoint (2026-11-17): Actions is re-enabled. Run
[44113969402](https://github.com/aosen-xiong/jdk/actions/runs/44113969402)
at head `c550af9288685fb1c630185be3a82023e53e8772` passed the native JDK
build and both 136-file platform nullness jobs, including configured VersionProps
and private callers. The whole workflow failed: JDK 17 JUnit dependency downloads
received Maven HTTP 429, and JDK 21/25/27 JUnit tests reported three deprecation
warnings in RuntimeVersionNullness. The matching CF branch now suppresses only
those deprecation warnings at the two affected test methods. All eight intended
nullness failures remain in both local study profiles; a JDK 21 binary-context
comparison removes only the three warnings. No JDK source or checker fix is
part of this CI correction. The updated CF pin requires a fresh hosted run.
Earlier stack heads still need their own checks and review before merging.
M1/M2/M3/M4/M5 remain open pending hosted checks and review/merge.

The current branch enrolls **126/126** shared Java sources, **6/6** platform
variants, and **6/6** Unicode template/output pairs. Each platform context checks
135 files: Unix in `run.WUHCwm` and Windows in `run.Zkjv0h`.
All targets are visited with stable input hashes and zero errors/warnings/crashes.
Across physical variants these are 138 distinct source units, with 36 files
using nullness suppressions and 102 without. Templates and generated copies are
paired, not counted twice. **VersionProps is an additional seventh generated
member**: its annotation source/template and direct callers now pass locally,
and its real configured output passed in both hosted 136-file platform checks
at the exact head recorded above. This establishes 139 distinct source units
under the study profile; it does not resolve the recorded source-contract issues.
The prior shared-only checkpoint was run.NbeZAd on #27. Thirty-two shared files have
nullness suppressions: StackTraceElement, Enum, Boolean, Integer, Long, String,
StringBuilder, StringBuffer, AbstractStringBuilder, Character, CharacterName,
StringLatin1, StringUTF16, Class, PublicMethods, ClassValue, WeakPairMap,
ClassLoader, Module, ModuleLayer, System, Runtime, SecurityManager, Thread,
ThreadGroup, ThreadLocal, InheritableThreadLocal, Process, ProcessBuilder,
ProcessHandleImpl, ApplicationShutdownHooks and StackStreamFactory. The other
94 do not.
Caller reproducer expectations/suppressions are counted separately.
Private callers do not inflate JDK coverage. No shared source file remains
unattempted in this inventory. Platform/generated coverage and integration
remain in M7; hosted checks are still required. The Class/Module null-caller and
Redirect equality source defects remain unresolved for upstream readiness.

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
annotations survive a rebuild. `src/java.base/share/classes/java/lang/VersionProps.java.template` also produces
a package member via `GensrcMisc.gmk`. It is a separate seventh generated member;
M7c2 must check its actual configured output. The direct source/template and build
recipe inventory found no other generated classes in this package (subpackages
remain excluded). Confirm this against configured build outputs before closure. Generated copies do not inflate
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

## Historical checker issue: generated record equality

Update, 2026-11-19: the comparison stack tip ([PR #36](https://github.com/aosen-xiong/jdk/pull/36))
now incorporates EISOP master `6ac6f7813440db1cd42b9a83aeccd102180930d4`, including
[the generated-record-method fix, #2636](https://github.com/eisop/checker-framework/pull/2636)
(commit `e35d62ecfd989b90a395b5b5e9e2efb5016195af`). The rebuilt checker reports
the old caller suppression as unused. The suppression is removed in that tip's
matching CF branch, preserving the direct generated-equals call and the three
negative controls. Validation details and the exact new pin are in the
[java.util upgrade checkpoint](java-util.md#checker-refresh-2026-11-19).
Earlier stack layers retain their original checker pins and historical results.

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

## Class loading, package metadata and modules (M5b)

`codex/nullness-java-lang-loading-modules` builds on the reflection foundation
([PR #22](https://github.com/aosen-xiong/jdk/pull/22)). The six newly enrolled
sources are ClassLoader, AssertionStatusDirectives, Package, NamedPackage,
Module and ModuleLayer. AssertionStatusDirectives needs no Java edits: its
existing nonnull array contracts agree with the matching native initializer.
Class and StackTraceElement receive separately committed follow-ups for their
uses of the newly precise module contracts. No executable JDK behavior changes.

The pinned Javadoc is the primary oracle. Module names/descriptors for unnamed
modules, absent layers/resources/annotations, bootstrap loaders, startup boot
layer, class/resource/package lookups and optional package metadata retain their
actual nullable positions. Nonnull container elements and successful loading
results remain precise. Function results admit bootstrap-null mappings without
making the function itself nullable; public layer creation documents its failure
for such a mapping. The empty layer's private constructor is a separate protocol.

ClassLoader's second top-level declaration, CompoundEnumeration, now opts into
nullness too. Correct the private compareCerts input to nonnull after reviewing
its sole caller's normalization. Remove three obsolete suppressions, retaining
and checking the assertion initializer's existing EnsuresNonNull. Its two
postcondition-removal controls restore caller errors. A new RequiresNonNull on
the native CDS reset entry describes the parallel-loader precondition; source
checking does not establish native caller correctness or concurrency safety.

Module.isNamed supplies conditional facts about paired name/descriptor fields
and their getters. The name-field fact is verified directly; the three related
facts need a disclosed relational postcondition suppression. Each expression has
its own removal control and useful caller. Do not infer that a named module has
a layer. An attempted getter precondition for Class's local module alias failed
at the callers and helper, was recorded, and was removed rather than retained
with extra caller suppressions.

Sixteen new diagnostic-key occurrences have sixteen independent removal
controls. They cover the documented module/loader invariants, an exact-size array,
three dependency/protocol gaps in ClassLoader, CAS publication, module-loader
mapping and startup state. Three obsolete ClassLoader suppression keys are removed.
The source adds 120 Nullable sites and removes one incorrect private Nullable;
there are four new opt-ins, one EnsuresNonNullIf and one RequiresNonNull. Existing
other-checker annotations remain intact except two obsolete explanatory CFComment
annotations removed with their obsolete suppressions. Annotation-normalized AST
checks preserve all executable syntax and declarations.

**Pinned JDK source defect:** Module.getResourceAsStream has the same null-caller
fallthrough as Class.isOpenToCaller: an unconditionally open package can lead to
isOpen(package, null). Both suppressions are labeled as source defects. A copied
branch reproduces the Module NPE; nonnull/open and null/closed controls pass.
This is not a CF false positive, a JNI end-to-end test, or a rebuilt-JDK test.
The defect remains unresolved for upstream readiness.

CF owns ModuleLoadingNullness (12 intentional invalid uses), ClassLoaderNullness
(5), and LoadingHelperContracts. Both public profiles match all 17 errors;
valid private callers pass and six separate invalid private calls are rejected.
Comparing with the parent annotations exposes eight missing nullable module-result
diagnostics and three missing lookup-result diagnostics, while several documented
null inputs were incorrectly rejected by the parent. Twenty-three independent
removal controls cover sixteen suppression keys, four isNamed expressions, the
new CDS precondition and the two existing assertion postconditions.

Cumulative run.POwHfh checks all 106 files under the unchanged JSpecify profile,
with final hashes, checker visitation and zero-status completion recorded. The
first attempt stopped at two StackTraceElement dependency diagnostics; those
were documented and controlled before the complete rerun. Detailed evidence is
in the matching CF checkout's checker/build/jdk-typecheck/loading-modules-study
and personal evidence cases NULL-0023/24, with occurrences added to NULL-0010/22.
The matching CF revision is 3cf56232ad4b54ca96df50a689bf3c457ef9b7eb. No tests or new
runner are added to JDK. Hosted CI/native builds remain unverified.

M5 source work is complete locally. Next is M6a (System, Runtime,
RuntimePermission, SecurityManager, Compiler), then M6b threads, M6c processes
and shutdown, and M6d stack walking. Those twenty shared files remain, followed
by the separate M7 platform/generated/integration work. M5 remains open for
hosted checks and review; this is not package completion.

## System and runtime (M6a)

Branch `codex/nullness-java-lang-system-runtime` targets the loading/modules
branch (#23). All five complete files already opt into nullness; their nested
scopes have no opt-outs. RuntimePermission and Compiler need no source edits.
The other three each have a separate annotation commit. Tests and the shared
runner remain in CF, pinned to 88854cd20b4ea1fef028cf63a8c14eb8d28a8e87.

| Source | Documentation oracle and decisions |
| --- | --- |
| `System` | Logger explicitly permits null messages, formats, exceptions and resource bundles; default implementations pass null parameter arrays. Supplier itself and log(Object)'s object remain non-null. Nullable supplier results and parameter elements follow message forwarding/MessageFormat behavior. LoggerFinder's localized bundle may be null, while System.getLogger(name,bundle) rejects null. Optional state and internal bridge returns/inputs match reviewed delegates. Preserve existing non-null system-stream model and its CFComment restriction excluding programs setting streams to null. |
| `Runtime` | exec permits null environment array/directory but rejects null commands and array elements. Version equality accepts null, while parsing/comparison reject it. equalsIgnoreOptional's true result establishes its argument non-null. Lazy version and native bootstrap caller classes are nullable. |
| `SecurityManager` | Context validators explicitly deny null with SecurityException; mark these validation inputs nullable without promising normal return. Other documented NPE preconditions remain non-null. Thread constructor docs permit an override to return a null thread-group preference. Property strings/caches are optional. |
| `RuntimePermission` | Name rejects null; ignored actions should be null. Existing annotations agree. |
| `Compiler` | command result may be null; documented inputs reject null. The compatibility stub does not enforce those NPEs, a recorded documentation/body discrepancy; retain documented preconditions without changing behavior. |

The changes add 68 Nullable sites and one EnsuresNonNullIf, with no new opt-ins.
Twelve new suppression annotations contain fourteen diagnostic-specific keys:

| Location | Reason and boundary |
| --- | --- |
| Runtime.exec array overload | ProcessBuilder.environment accepts null in its body but lacks the annotation; retire this temporary argument suppression in M6c. |
| Runtime.Version.parse split declaration | VNUM is a mandatory capture after a successful match; optional captures remain nullable. |
| Runtime.Version.equals (two keys) | Known checker limitation: saving the guard result in a boolean loses the non-null fact, and an alias prevents refining the original argument. See CF Issue3622's ImmutableIntList10 and the new DelayedNullnessContract reproducer. |
| SecurityManager.getRootGroup | The current thread is live and therefore has a group; the general Thread getter remains nullable. |
| SecurityManager static boot call | Trusted VM phase ordering. This one argument key needs class scope because Java cannot annotate a static initializer; removing it restores only the intended error. |
| SecurityManager descriptor stream | Layer members are named and have descriptors; the stream loses that graph relation. |
| SecurityManager's two package checks | Matching locks and validity flags establish non-null cache snapshots. This does not verify concurrency generally. |
| System's three stream fields | Null placeholders are filled through native setters during initPhase1; preserve the existing restricted stream model. |
| System.initPhase1 (two keys) | Native properties supply line.separator, and the live main thread has a group. Native startup is outside this pass. |

All fourteen key removals independently reproduce one intended diagnostic. A
fifteenth control removes the new conditional postcondition and breaks its direct
caller. The known boolean limitation is documented before suppression; no checker
implementation fix or new crash is claimed. The minimal direct-guard control
passes; delayed/aliased cases produce three expected diagnostics in each mode.

CF's SystemLoggerNullness, RuntimeVersionNullness and LegacySecurityNullness
match 32 intentional diagnostics per profile (31 nullness checks plus the existing
clear.system.property policy). Valid nullable inputs, a nullable thread-group
override, non-null/nullable supplier results and generic components pass.
LegacySecurityNullness is restricted to JDK 17 for removed/disabled APIs.
SystemRuntimeHelperContracts validates bootstrap null callers and the conditional
postcondition. All 111 source invocations in run.EFcrDp exit zero with confirmed
visitation, unchanged input hashes, no warnings/crashes/truncation, and unchanged
checker JAR hashes. AST audits preserve executable syntax; three PrivilegedAction
diamond expressions spell their inferred Object/String type arguments explicitly
to carry qualifiers. Other-checker annotations are preserved.

Detailed original/qualifier/final sources, exact commands and removal controls
are retained in the CF study's system-runtime-study directory and personal cases
NULL-0025/26/27. The JavaLangAccess interface remains unchecked; its Thread reset
and constructor bridges are completed in the M6b follow-up below. No claim of complete
annotation coverage for jdk.internal.access is made. Hosted CI/native builds
remain unverified.

Next milestones: M6b adds four thread/thread-local files (115/126), M6c adds six
process/shutdown files (121/126), and M6d adds five stack-walking files (126/126).
M7 then handles platform/generated sources and integration; these five source
checks do not finish java.lang or close the hosted-CI/review gate.


## Threads and thread-local state (M6b)

Layer `codex/nullness-java-lang-threads` follows the system/runtime branch (#24).
The four complete shared-source files already opted into nullness, with no
nested opt-outs. This layer also aligns System's blocker-reset and optional
target/access-context constructor bridges. Each changed Java source has its own
commit; CF owns all caller fixtures. No runtime behavior is changed. The syntax
audit permits only annotations/imports/comments, explicit Object bounds, and
spelling Thread's existing Boolean privileged-action type argument explicitly.

| File | Oracle and annotation decisions |
| --- | --- |
| `Thread` | Class policy rejects null unless a constructor or method explicitly permits it. Add the missing nullable group/target positions on the five-argument constructor and nullable optional/cleared state. Keep non-null names and public stack trace arrays/elements. Native dumpThreads can return null inner traces, so annotate that dimension separately. Current-thread/start/exit assumptions remain scoped boundaries. |
| `ThreadGroup` | A root has no parent; public explicit-parent construction rejects null. Preserve the existing nullable name contract, whose null policy is unspecified by Javadoc. parentOf(null) returns false by implementation. Both internal array references and unused elements are nullable; enumeration preserves caller component nullness with PolyNull. Populated-prefix/count and snapshot facts remain explicit suppressed assumptions. |
| `ThreadLocal` | The documented default initialValue is null. Preserve the existing exact-nullable type-argument restriction, which rejects plain ThreadLocal<String>; use a CF implicit-lower-bound default and explicit nullable upper bound instead of an unsupported type-parameter annotation. Supplier/nested scopes restore ordinary implicit lower bounds. Keep get/set/childValue as T; mark lazy maps, absent entries and stored/cleared values nullable. |
| `InheritableThreadLocal` | Inherits the same default-null type restriction and returns parentValue unchanged. Its per-thread map is optional. Three receiver errors stem from an observed source/bundled-annotation interaction, with scoped workarounds. |
| `System` follow-up | The existing JavaLangAccess implementation forwards nullable blocker resets and optional thread target/access context. JavaLangAccess itself and NIO remain outside this source coverage. |

ThreadLocal's factory/non-null subclass exception is an existing CF modeling
limitation: a subclass must override initialValue with the promised T, and the
factory's final SuppliedThreadLocal does so. This does not make unsafe direct
non-null construction valid. Public controls verify nullable values, initialized
non-null values, nullable suppliers' results, and rejection of unsafe construction.

Findings were recorded before suppressions. The two generic forwarding errors
and three inherited receiver errors disappear in a diagnostic-only run without
bundled JDK stubs. A smaller ordinary generic class passes; the suspected merge
defect remains project-dependent (NULL-0028), not a claimed general defaulting
bug. The source gate keeps bundled contracts and its frozen profile. A failed
legacy-stub reduction produces caught parser AssertionError warnings (NULL-0029);
those runs fail and are retained separately, never counted as passing checks.
No checker implementation change or parser-warning suppression is included.

Other suppressions cover Reference.refersTo's documented null input missing
from its signature, live-thread/group and uncaught-dispatch lifecycle,
Thread-subclass ancestry, ThreadGroup's populated prefixes, and ThreadLocal's
caller-established stale-slot index. Native thread exit order is secondary
evidence for lifecycle assumptions, not a native/concurrency proof. Nullness
qualifiers are kept accurate at these boundaries; there is no blanket suppression.

The four new files comprise 1,441 original non-comment source lines. Across the
five edited sources the syntax inventory records 70 net additional Nullable
sites, two PolyNull helper parameters, five DefaultQualifier annotations, no new
opt-in and no new postcondition. Thirty-two declaration scopes contain 44 new
nullness suppression keys (20 new SuppressWarnings annotations and 12 extended
existing annotations). The 44 individual removal checks restore only their
intended diagnostic keys. Existing unrelated checker annotations are preserved.

Validation: all 115 cumulative source targets pass with unchanged hashes,
verified visitation, no errors/warnings/crashes or truncation. Public CF controls
match 23 deliberate errors in each of JSpecify and ordinary nullness modes;
the package-private helper fixture passes the shared source runner. Caller tests
do not inflate the 115-file denominator. Frozen checker implementation c12ce38daa,
source compiler JDK17.0.14 and original bundled JDK 0af1a5ad1f9 remain unchanged.
Initialization, KeyFor, purity, native lifecycle and concurrency are outside proof.
Hosted checks and the native build remain unverified.

Next: M6c processes/shutdown adds six shared files, reaching 121/126; M6d stack
walking adds five, reaching 126/126. M7 still requires the six platform variants,
six Unicode generation inputs/outputs, cross-module/package integration, a
suppression audit and hosted native build results. The Class/Module null-caller
source defect is still unresolved for upstream readiness. No automatic merge
or upstream submission is part of this layer.

## Processes and shutdown (M6c)

Layer `codex/nullness-java-lang-processes` follows threads (#25). All six new
shared source files are checked in full. ProcessHandle and ProcessHandleImpl
receive explicit whole-file nullness opt-ins; ApplicationShutdownHooks extends
its existing opt-in. Shutdown already has sufficient annotations and needs no
source edit. Runtime receives a coordinated suppression removal, not an extra
coverage count. Each edited Java source has its own commit; tests remain in CF.

| File | Documentation oracle and annotation decisions |
| --- | --- |
| `Process` | “Null streams” are non-null stream objects with special behavior. Keep all stream/reader/writer results non-null and Charset inputs non-null. Mark six lazily populated cache fields nullable; three paired-cache dereference suppressions record lock-protected initialization order. |
| `ProcessBuilder` | Class policy rejects null inputs except documented directory reset. Optional directory/environment/redirect-array references are nullable; redirect elements remain non-null. The Runtime-only environment helper accepts a nullable array with non-null strings. Redirect.file explicitly returns null for no file; equals accepts null. |
| `ProcessHandle` | equals explicitly accepts null, compareTo rejects it. Optional wrappers, process streams and completion futures remain non-null; present payloads are non-null. Native argument array elements retain a reviewed non-null assumption. |
| `ProcessHandleImpl` | Nullable Info fields represent unavailable native data; accessors return non-null Optional wrappers, despite stale local comments describing null. Two optional native output-array parameters are documented nullable. Companion-array and live-thread-group relations remain scoped assumptions. |
| `ApplicationShutdownHooks` | Nullable hooks map represents failed registration or consumed shutdown state. Callback dispatch relies on successful registration, completed initialization and one-shot shutdown ordering. Hook inputs retain Runtime's documented non-null precondition. |
| `Shutdown` | Existing non-null array of nullable Runnable slots and guarded dispatch are sufficient; passes unchanged. Internal hook inputs retain the actual non-null caller precondition. |

Command arrays/lists model valid commands with non-null elements. Constructors
can store an invalid list containing null and defer rejection until start; the
annotations deliberately retain the conservative valid-command model, not a
claim that constructors immediately validate every element. Native process
metadata and unchecked event/platform dependencies are not proven by this pass.

Findings precede all nine new diagnostic-specific keys: three paired-cache
checks, a local declaration covering three missing ProcessImpl.start contracts,
a pipeline predecessor-output relation, one current-thread/group invariant,
two companion-array loop relations and the one-shot shutdown map. These are
dependency, relational and lifecycle boundaries, not newly established CF bugs.
Each independent removal restores only its intended key. Completing the
ProcessBuilder environment contract removes Runtime's temporary argument key;
removing that new qualifier alone restores exactly the former Runtime error.
The platform dependency key should be revisited in M7.

A separate source defect remains open (NULL-0030): Redirect.equals promises
false for distinct redirects with no associated file, but internal pipe redirects
reach an invalid non-null assertion and dereference. A test-only class patched into
host OpenJDK17.0.14 reproduces NPE by default and AssertionError
with system assertions enabled, without starting subprocesses. Reviewed source
matches that path. The frozen JSpecify assumption that assertions are enabled
lets the annotation check pass; this does not validate the assertion premise.
No source behavior fix or JDK test is included. A second source-level observation
is that Info.info does not clear commandLine on a start-time mismatch despite
its empty-info comment; it is retained separately without a runtime claim.

The six new files contain 1,118 original non-comment source lines. Across six
edited sources: 21 additional Nullable sites, two added and one extended opt-in,
no new postconditions, nine new suppression keys in nine declaration scopes
(eight new annotations and one extended removal annotation), and one retired
Runtime key. Syntax comparison confirms executable code and unrelated checker
annotations are unchanged. Four of the six new files have suppressions.

Validation: all 121 cumulative source checks pass with matching hashes and
verified visitation, zero errors/warnings/crashes or truncation. Public process
controls match 20 deliberate errors in each profile; the earlier Runtime/security
fixture still matches ten in each. All seven package-private helper controls
pass. One helper command used an incorrect filename after three completed
fixtures; the remaining four were then checked with their actual names. That
setup failure is retained and is not counted as a successful batch. Frozen CF
implementation c12ce38daa and source compiler JDK17.0.14 are unchanged. No native
JDK build was run locally, and hosted CI remains unverified.

Next is M6d: the final five shared stack-walking files, reaching 126/126.
M7's platform/generated sources, integration, suppression review, unresolved
source defects and hosted native/CF results still gate package readiness.


## Stack walking (M6d)

Layer `codex/nullness-java-lang-stack-walking` follows processes (#26) and
finishes the five remaining shared files. Each receives an explicit whole-file
nullness opt-in, including inherited nested scopes. Each source has its own
annotation commit; the matching CF branch owns the caller controls. This
completes the shared-source annotation pass locally, not package readiness.

| File | Documentation oracle and annotation decisions |
| --- | --- |
| `StackWalker` | Class policy rejects null options/callbacks. StackFrame.getFileName explicitly admits missing source information. Optional internal extendedOption is nullable; factories and getCallerClass retain non-null normal results. walk preserves the callback's T, including nullable results. |
| `StackFrameInfo` | Nullable file name matches the interface and StackTraceElement. The lazy stack-trace-element cache is nullable; double-checked construction still returns a non-null value. Member metadata supplied by VM remains a trusted boundary. |
| `LiveStackFrame` | Local/operand arrays are non-null and may contain null reference values. Monitor components also admit observed empty slots; this is an implementation-derived contract and a documentation mismatch, not a promised non-null-element API weakened just to pass checking. |
| `LiveStackFrameInfo` | Preserve non-null array references and primitive-slot results; represent nullable locals, operands and monitor entries in both fields and overrides. |
| `StackStreamFactory` | Preserve nullable traversal exhaustion, nullable trySplit and callback result propagation. Partially filled/reserved array slots are nullable. MonotonicNonNull records the frame buffer's initialization phase; EnsuresNonNull on initFrameBuffer is verified through its overrides and used by a caller. |

Fifteen diagnostic-specific source keys in fourteen methods record native
callback order, populated buffer ranges, the hasNext/next-frame relation and
caller discovery. Every key's individual removal restores exactly one error.
The helper postcondition has its own removal control; no false postcondition is
added to checkState, since NEW can succeed before initialization. No executable
code, new runtime guard or cast is introduced. Native state, array bounds and
concurrency are outside proof. Existing NonEmpty and purity annotations remain.

The ordinary caller comparison exposed a KeyFor default incompatibility
(NULL-0032), initially suspected to be a checker defect. java.lang's existing
KeyForBottom LOWER_BOUND default reaches explicit callback wildcard bounds.
A reduced example passes if the default is removed or restricted to implicit
bounds. In the full source context, changing package-info alone still leaves
bundled defaults in effect; the diagnostic-only combination with ignorejdkastub
removes the extra failures. The frozen source gate does not use that override.
Four method-scoped keyfor-only suppressions live solely in the CF caller fixture,
with individual removal controls restoring the seven extra KeyFor diagnostics.
Both caller profiles continue to reject all nine intended nullness errors.
No package-wide default change or checker implementation fix is included.

A host OpenJDK17.0.14 interpreter probe independently confirms one null monitor
slot after exiting a synchronized block (NULL-0034). Only the test class is
patched into the host module; it does not build or replace JDK implementations.
The native source copies monitor owner slots without filtering empty entries.
This observation explains the conservative nullable component contract and is
retained for documentation review. Locals/operands have their own documented
or JVM-value basis for nullable elements.

The five files total 909 original non-comment source lines. They add 33 Nullable
sites, one MonotonicNonNull, one EnsuresNonNull and five opt-ins. Four files pass
without suppressions; StackStreamFactory has the fifteen keys. The syntax audit
confirms only annotations/imports/comments changed. Four trial generic bounds
were removed as redundant under this checker's existing implicit nullable upper
bounds; valid nullable callback consumers verify the retained declarations.

Validation: all 126 cumulative shared source files pass with unchanged input
hashes, verified visitation, zero errors/warnings/crashes or truncation. All
eight package-private helper fixtures pass; six private negative controls reject
unsafe nullable payload/state uses. Public callers match nine deliberate errors
in JSpecify and ordinary nullness modes with the scoped KeyFor workarounds.
The checker implementation, artifacts and JDK17 compiler are unchanged.
Hosted checks and native builds remain unverified.

M7 is the remaining package work: Unix and Windows variants of ProcessEnvironment,
ProcessImpl and Terminator; six CharacterData template/output pairs; matching
platform/generated compilation contexts; cross-module/package integration;
source/default/suppression review; and exact-head hosted CF/native results.
The shared 126-file denominator does not include or conceal those items.

## Unix process and termination implementations (M7a)

The Unix layer follows stack walking (#27). It adds whole-file opt-ins and
contracts in the Unix variants of Terminator, ProcessEnvironment and ProcessImpl.
The shared ProcessBuilder follow-up has its own commit. The same-name CF branch
owns the new UnixProcessHelperContracts fixture; no tests or runner are added here.

The existing source runner now receives the full shared root followed by the
Unix classes root. This is an explicit compilation-context change from M6's
shared-only checks. All 126 shared files are rerun with the three Unix files;
Windows classes are never mixed into this invocation. The source checker still
uses the same frozen JSpecify profile, artifact hashes and JDK17 compiler.

| File | Contract decisions and retained boundaries |
| --- | --- |
| Unix Terminator | The termination handler starts null; no suppression is needed. Signal delivery and shutdown remain native/lifecycle boundaries. |
| Unix ProcessEnvironment | Missing values and previous map values are nullable; equality accepts null. Null environment maps produce a null native block. Environment keys/values remain non-null. Two accessor suppressions cover intentional NPE rejection of foreign entries with null payloads, as the environment contract permits. |
| Unix ProcessImpl | Environment, directory and redirect-array defaults are nullable, as are forwarded native env/dir buffers. PolyNull preserves toCString's input/result relation. Drain helpers represent no data or asynchronous closure; deferred stream state starts null. Four keys cover redirect-factory dispatch, wrapped exception cause, paired close state and an inherited java.io field contract gap. |
| Shared ProcessBuilder | The old argument suppression becomes unused when Unix start contracts are visible and is removed. Preserving a nullable directory exposes a missing nullable contract on ProcessStartEvent.directory; one private-start-method assignment key documents that separate dependency gap. |

All new suppressions were documented before being added. None establishes a
new Checker Framework implementation bug. The redirect dispatch relies on the
pinned factory implementation: DISCARD's Javadoc permits null, although this
revision constructs and returns a non-null File. No general Redirect.file or
Throwable.getCause contract is strengthened. Foreign-entry rejection is not
claimed to be null-safe for invalid inputs. No runtime guards or casts change.

The three new sources total 1003 original non-comment source lines and add
26 Nullable sites (including one explicit Void qualifier already supplied by
the checker default), two PolyNull sites and three opt-ins. Seven new diagnostic
keys in seven source scopes are audited individually; one old key is retired.
Each removal restores one error except the redirect key, which restores three.
The 129-file set has 34 files with nullness suppressions and 95 without.

Validation includes the entire 129-file source gate, all nine package-private
helper fixtures, seven invalid caller controls, a private PolyNull positive/
negative comparison, and three independent optional-start-parameter removals.
The public process consumer fixture matches 20 deliberate errors in both
JSpecify and ordinary nullness profiles. Input hashes, complete visitation and
zero warnings/crashes/truncation are verified. The AST audit preserves executable
syntax and other-checker qualifiers. The profile does not prove native startup,
concurrency, initialization, map keys, purity or temporary-array fill completeness.

M7b remains the three Windows variants, M7c the six CharacterData template/output
pairs, and M7d integration/default/suppression review and exact-head hosted
CF/native results. The shared inventory remains 126; variants and generated
outputs have their own counts. Hosted/native results are still unverified.

## Windows process and termination implementations (M7b)

This layer follows Unix (#28). Each of the three Windows files has its own
annotation commit, with a matching CF branch and package-private caller fixture.
The entire 126-file shared inventory is checked again with only the Windows
classes root appended. The Unix source hashes remain identical to their passing
129-file run. The six platform variants are all covered locally; generated
sources and integration remain distinct work.

CI uses a two-entry platform matrix with the same 129-file manifest and existing
CF script. Each job selects its platform source root and matching helper fixture;
Unix and Windows roots are never combined. Distinct artifact names retain both
logs, fail-fast is disabled, and each job has a 45-minute limit for its checker
build and source/caller checks. Both source jobs run on Linux. The existing native build job also targets Linux;
this workflow does not establish native Windows execution or build success.

| File | Annotation decisions and retained boundaries |
| --- | --- |
| Windows Terminator | Nullable initial signal handler; otherwise existing defaults suffice. No suppression. |
| Windows ProcessEnvironment | Nullable missing/previous map values, getenv result and optional environment block; nullable equality input. Four query overrides retain the documented environment null rejection and have individual override.param.invalid suppressions for the conflicting HashMap superclass contract. |
| Windows ProcessImpl | Nullable environment, working directory and redirect-array references, including constructor/native forwarding. One start-method argument key covers the same closed redirect-factory dispatch as Unix. Public stream/handle/future guarantees remain non-null. |

The environment conflict is an existing JDK inheritance/documentation problem,
not a Checker Framework bug: HashMap promises null-query support, while the
returned environment deliberately throws. Four temporary override suppressions
preserve the documented environment precondition but do not prove or repair the
inherited HashMap promise. This remains open for upstream review. General
HashMap annotations are unchanged, as are executable guards and behavior.

No regex suppression is required: no-argument Matcher.group is already non-null.
Void already defaults nullable in this checker, so its callback argument/result
needs no additional qualifier. No postcondition is added to nonNullString when
its callers do not need refinement of their original arguments.

The three files total 703 original non-comment source lines and add 15 Nullable
sites and three opt-ins. Five new keys in five scopes each have a removal
control: one override error for each environment method, three redirect argument
errors for ProcessImpl.start. Eleven invalid caller checks and three independent
optional-input removal checks behave as expected. Nine helper fixtures pass;
public process callers match 20 intended errors in both nullness profiles. The
AST audit preserves executable syntax and other-checker qualifiers.

All 129 Windows-context sources pass with hashes and complete visitation verified,
zero errors/warnings/crashes/truncation. Each 129-file platform set has 34 files
with nullness suppressions and 95 without; across 132 physical files the counts
are 36 and 96. These are checks under the frozen assumptions and documented source
conflicts, not a proof of native behavior, concurrency or inheritance soundness.
No Windows subprocess or native JDK build was run locally.

Remaining M7c: the six CharacterData template/output pairs and matching generated
source context. M7d: integration/default/suppression review, unresolved source
contracts and exact-head hosted CF/native results. Hosted results are unverified.

## Generated Unicode classes (M7c1)

This layer adds one whole-file nullness opt-in to each authoritative CharacterData
template: Latin1, 00, 01, 02, 03 and 0E. Each template has its own annotation
commit. No extra qualifier, postcondition or suppression is needed. Generated
singleton references, primitive tables and mapping arrays are non-null under the
existing initialization assumptions; non-BMP classes retain the nullable
CharacterData uppercase-mapping default. Latin1 and 00 strengthen that result
to non-null. The generated original sources contain 4,225 non-comment lines,
including tables; this is distinct from template size.

The matching CF branch pins runner/caller commit
`3c3b624177252e3bc951d6c3e342541a8278d8c6`. The same existing script accepts
`JDK_GENERATE_CHARACTER_DATA=1`: it compiles the selected JDK's Java generator,
uses its pinned Unicode inputs and GensrcCharacterData arguments, writes fresh
outputs, rejects shadow copies, and saves input/output hashes and command/status
logs. This Java-only generation succeeds locally. It is not a native JDK build.
Normal invocations with the option unset retain their original behavior.

The two 135-file source gates pass with the shared root, exactly one platform
root, then the fresh generated root. All nine private helper fixtures pass per
platform. The 29 public caller fixtures match exact expected diagnostic lines
and keys in both JSpecify and ordinary nullness profiles; the Unicode fixture
also passes with Windows sources. Four invalid private nullable-result callers
are rejected. Removing Character's existing BMP-return suppression still gives
exactly one error: generated bodies do not eliminate the range/dispatch invariant.

AST review preserves executable syntax and all four Latin1 intrinsic annotations.
The complete 132-file ordinary-source audit finds explicit top-level nullness
opt-ins throughout, no opt-outs, and 141 source suppression-key entries across
36 files. It preserves other-checker qualifiers and executable syntax, accounting
for explicit Object bounds and four previously reviewed PrivilegedAction diamond
expansions. The five ThreadLocal-family default sites preserve their documented
generic model; package-info's existing KeyFor lower-bound default is unchanged.
Earlier per-key controls remain recorded; the generated-context cumulative runs
also enable unused-suppression warnings. No new checker defect or crash is found.

M7c2 is VersionProps: review/check its template and check its real configured
output from native CI. M7d retains exact-head hosted CF/native results, source
contract review and broader integration. Class/Module null callers, Redirect
equality, released monitor slots and Windows environment inheritance conflicts
remain explicitly recorded; suppressions do not repair those source contracts.
No local native build was run. Hosted and native Windows results are unverified.

## Generated version properties (M7c2)

VersionProps is the final additional member found by the package's source and
generation-recipe inventory. Its authoritative template gains one whole-file
nullness opt-in. No qualifier or nullness suppression is needed, and no executable
code changes. The template contains 143 original non-comment source lines.

The documentation/implementation review covers non-null build-provided string
fields, version-number lists, non-null Optional containers and the initialized
system-property map. Empty strings represent absent metadata. The jlink plugin
guards replacement values against null; VM reads and bytecode rewriting remain
trusted boundaries. Temporary array filling remains outside the frozen first-pass
array-initialization guarantees. Optional contents are not promised present.

All 17 distinct build placeholders (18 occurrences) are inside string literals.
An exact .java copy of the template therefore permits a local syntax/nullness
check without inventing configured version values. That template check passes,
as do Runtime, the new VersionProps private caller and the existing runtime helper
in separate Unix and Windows contexts. Six invalid caller cases reject null map
or parsing inputs, null version-list elements and unchecked optional contents.
The AST audit preserves behavior and the pre-existing unused suppression.
**These are template checks, not a claimed configured build output or native run.**

The same-name CF branch pins
`e8fa72969e13ab46fa42e252cb8a84e035dd4e93`; it contains the caller fixture and
inherits the existing uniform runner. No test or new script is added to JDK.
The existing native Linux CI job now checks out the exact PR head and uploads
VersionProps.java from its successful build, together with source revision and
template/output hashes. The nullness jobs depend on that build, verify the
artifact's provenance, append its root through JDK_EXTRA_SOURCE_ROOTS, and check
136 explicit sources plus ten private caller fixtures per platform context.
Unicode generation still uses the same CF runner option. A native build failure
blocks those downstream jobs; a skipped job is not a passing source check.

Remaining completion gates are explicit:

| Gate | Status |
| --- | --- |
| Shared source inventory (126) and platform variants (6) | Reviewed and locally checked. |
| Unicode template/output pairs (6) | Generated and checked locally in both complete 135-file contexts. |
| VersionProps template | Reviewed and checked locally with direct consumers; no new suppression. |
| Actual configured VersionProps output and 136-file CI set | Awaiting hosted native build and downstream checks. |
| Defaults, opt-ins and suppression inventory | Reviewed; 141 diagnostic-specific source keys across 36 files, with previous removal evidence and current unused-suppression checks. |
| Public consumer controls | All 29 fixtures match expected diagnostics in both profiles; broader CF suites await hosted CI. |
| Source-contract conflicts | Class/Module null callers, Redirect equality, released monitor slots and Windows environment inheritance remain open for upstream review. |
| Native platform behavior | Linux build awaits CI; native Windows build/execution is not provided by this workflow. |
| Upstream submission/merge | Not performed; requires maturity review and a later request. |

The annotation-source inventory is covered, but the package is not yet ready to
be called fully validated or upstream-ready. Hosted results remain unverified;
no local native JDK build was run. Subpackages remain separate studies.

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

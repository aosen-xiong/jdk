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
| [M3: strings and Unicode](https://github.com/aosen-xiong/jdk/milestone/3) | 14 | 50/126 | Three PR groups; distinguish nullable objects/sequences, nonnull arrays/elements, and internal caches. Establish generated Unicode context before its helper checks. |
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

5. `codex/nullness-java-lang-wrappers` targets the values branch; seven
   wrapper files pass individually, with cumulative validation recorded below.

CI checkpoint (2026-11-17): the fork's Actions page explicitly says workflows
are not running due to the scale of GitHub Actions usage and require maintainer
re-enablement. REST reports Actions enabled and the workflow active, but manual
dispatch returns HTTP 422, "Actions has been disabled for this repository."
Re-enabling through the repository/workflow APIs did not clear the restriction.
Hosted checks on #9, #10 and #11 have not started; the wrapper layer has no
claimed hosted result either. The existing PR #7 result remains green. Re-enable
workflows on the fork's Actions page, then run CI for each exact stack head.
M1/M2 remain open pending hosted checks and review/merge.

The current branch enrolls **33/126** shared implementation files. All 33 pass
the cumulative local run under the frozen profile, with no errors or warnings. Five source files retain nullness suppressions: StackTraceElement,
Enum, Boolean, Integer and Long. The other 28 have no nullness suppressions.
The generated-record consumer has a separate known checker-bug suppression.
The other 93 shared files remain future milestones.

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

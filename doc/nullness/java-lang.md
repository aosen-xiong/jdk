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

CI also runs on pushes to the two new study branches. This provides a check for
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

CI checkpoint (2026-11-17): GitHub reports Actions enabled and this workflow
active, but has not queued a hosted run for #9 or #10 after PR creation and
branch pushes. Workflow syntax validates locally; the trigger issue is
unresolved. Neither new layer has a claimed hosted CI result, and M1 remains
open pending those checks and review/merge.

The current branch enrolls **21/126** shared implementation files. Twenty have
no nullness suppressions; StackTraceElement retains the documented native-array
postcondition suppression from PR #7. The other 105 are not yet verified here.

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

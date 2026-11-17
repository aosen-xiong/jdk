# java.util nullness roadmap

Inventory baseline: `c11500f3ca98c5f96c7994c3705f917cf8ec05ff`.
Scope: the 120 direct Java source files under
`src/java.base/share/classes/java/util/`, plus separate review of `package-info.java`.
Subpackages (`concurrent`, `function`, `stream`, and others) are separate studies.
No additional direct java.util Java variants exist under the inspected Unix,
Linux, macOS or Windows roots. Future platform/generated inputs will be explicitly
inventoried if compilation requires them; Unix is the only target for this package.

## Delivery

Plan 25 related PR groups, subject to splitting large or tightly coupled groups
(working estimate 22–28). Each changed source file gets its own annotation commit
when published. Existing correct annotations still require checking;
a source file need not be changed just to join coverage. Tests and the shared runner
belong in the matching CF branch, not this repository. Do not merge or submit
upstream automatically. Review inherited and individual source Javadoc first.

Milestones:

- [M1: core utilities](https://github.com/aosen-xiong/jdk/milestone/8) — group 1, 5 files.
- [M2: collection contracts](https://github.com/aosen-xiong/jdk/milestone/9) — groups 2–6, cumulative 31 files.
- [M3: collections and arrays](https://github.com/aosen-xiong/jdk/milestone/10) — groups 7–14, cumulative 60 files.
- [M4: remaining package APIs](https://github.com/aosen-xiong/jdk/milestone/11) — groups 15–25, all 120 files plus package review.

Each group needs complete scope/contract records, passing file and regression checks,
valid/invalid callers, suppression removal controls, and exact-head fork CI.
A clean source check does not establish complete modeling of conditional contracts.

The first group uses paired branch `codex/nullness-java-util-core`, stacked on
[java.lang VersionProps, PR #31](https://github.com/aosen-xiong/jdk/pull/31).
Each subsequent group targets the preceding java.util branch. Hosted validation
of this group is pending; local results below do not replace exact-head CI.

## Exact inventory and proposed PR groups

All names below denote direct `.java` files in the shared java.util directory.
The groups partition all 120 files without duplicates.

| Group | Scope | Files | Sources |
| --- | --- | ---: | --- |
| 1 | Core null-handling utilities | 5 | `Objects`, `Optional`, `OptionalInt`, `OptionalLong`, `OptionalDouble` |
| 2 | Traversal | 7 | `Iterator`, `ListIterator`, `Enumeration`, `PrimitiveIterator`, `Spliterator`, `Spliterators`, `Tripwire` |
| 3 | Comparison | 2 | `Comparator`, `Comparators` |
| 4 | Collection interfaces | 8 | `Collection`, `List`, `Set`, `SortedSet`, `NavigableSet`, `Queue`, `Deque`, `RandomAccess` |
| 5 | Map interfaces | 3 | `Map`, `SortedMap`, `NavigableMap` |
| 6 | Abstract collection implementations | 6 | `AbstractCollection`, `AbstractList`, `AbstractSequentialList`, `AbstractSet`, `AbstractMap`, `AbstractQueue` |
| 7 | Lists and queues | 4 | `ArrayList`, `LinkedList`, `ArrayDeque`, `PriorityQueue` |
| 8 | Hash collections | 4 | `HashMap`, `LinkedHashMap`, `HashSet`, `LinkedHashSet` |
| 9 | Tree, weak and identity maps | 4 | `TreeMap`, `TreeSet`, `WeakHashMap`, `IdentityHashMap` |
| 10 | Enum collections | 4 | `EnumMap`, `EnumSet`, `RegularEnumSet`, `JumboEnumSet` |
| 11 | Collection factories and wrappers | 3 | `ImmutableCollections`, `KeyValueHolder`, `Collections` |
| 12 | Array utilities and parallel helpers | 3 | `Arrays`, `ArraysParallelSortHelpers`, `ArrayPrefixHelpers` |
| 13 | Sorting implementations | 3 | `TimSort`, `ComparableTimSort`, `DualPivotQuicksort` |
| 14 | Legacy collections | 4 | `Dictionary`, `Hashtable`, `Vector`, `Stack` |
| 15 | Everyday value and text utilities | 6 | `Base64`, `HexFormat`, `BitSet`, `UUID`, `StringJoiner`, `StringTokenizer` |
| 16 | Random generation and statistics | 5 | `Random`, `SplittableRandom`, `IntSummaryStatistics`, `LongSummaryStatistics`, `DoubleSummaryStatistics` |
| 17 | Formatting and scanning | 4 | `Formatter`, `Formattable`, `FormattableFlags`, `Scanner` |
| 18 | Formatting exceptions | 14 | `DuplicateFormatFlagsException`, `FormatFlagsConversionMismatchException`, `FormatterClosedException`, `IllegalFormatArgumentIndexException`, `IllegalFormatCodePointException`, `IllegalFormatConversionException`, `IllegalFormatException`, `IllegalFormatFlagsException`, `IllegalFormatPrecisionException`, `IllegalFormatWidthException`, `MissingFormatArgumentException`, `MissingFormatWidthException`, `UnknownFormatConversionException`, `UnknownFormatFlagsException` |
| 19 | Locale and currency | 4 | `Locale`, `LocaleISOData`, `Currency`, `IllformedLocaleException` |
| 20 | Calendars and time zones | 6 | `Date`, `Calendar`, `GregorianCalendar`, `JapaneseImperialCalendar`, `TimeZone`, `SimpleTimeZone` |
| 21 | Resources and properties | 7 | `ResourceBundle`, `ListResourceBundle`, `PropertyResourceBundle`, `MissingResourceException`, `Properties`, `PropertyPermission`, `InvalidPropertiesFormatException` |
| 22 | Service loading | 2 | `ServiceLoader`, `ServiceConfigurationError` |
| 23 | Events and observation | 6 | `EventListener`, `EventListenerProxy`, `EventObject`, `Observable`, `Observer`, `TooManyListenersException` |
| 24 | Timers | 2 | `Timer`, `TimerTask` |
| 25 | Remaining collection/input exceptions | 4 | `ConcurrentModificationException`, `EmptyStackException`, `InputMismatchException`, `NoSuchElementException` |

## Current checkpoint

Group 1: all five source files pass the pinned JSpecify profile locally. Public
caller controls pass in both JSpecify and ordinary nullness profiles (21 intended
invalid-use diagnostics across three CF fixtures). Eleven annotation/suppression
removal controls pass. The full 141-file Unix regression passed with zero errors,
warnings, crashes or skipped targets; input hashes stayed unchanged. Five files have
six diagnostic-specific suppression sites: four existing CF class-policy location
exceptions, one comparator conditional-input boundary, and one reproduced CF
polymorphic conditional issue. These are disclosed limitations, not silent opt-outs.
The constructors, empty-instance cast and private presence predicates were reviewed
against source documentation and implementation. No executable behavior changed.
Groups 2–25: unattempted (115 files). package-info.java reviewed: existing
KeyFor lower-bound default retained; no general package nullness policy inferred.
Full JSpecify mode remains pinned to CF c12ce38daa implementation; initialization,
KeyFor, purity and native execution are outside the proof scope. Checker defects
are documented first and then narrowly suppressed with removal controls.

Conditional Optional callbacks are an explicit review boundary: existing nonnull
callback types are safe sufficient preconditions, but reject inactive-null callbacks
that the documented implementation never invokes. Do not call that full contract
coverage or widen callbacks to Nullable without preserving rejection of unsafe calls.

## First PR configuration

The matching CF branch is `codex/nullness-java-util-core`. The workflow pins
[CF 502a563](https://github.com/aosen-xiong/checker-framework/commit/502a5630341673eb659cedf265fc7576478b3d36),
which adds caller controls and the reduced supplier issue without changing the
checker implementation. The new workflow step uses the same
`checker/bin-devel/typecheck-jdk.sh` interface and runs only
in the Unix matrix leg. Existing java.lang Windows coverage remains intact.
No new test harness, Python/JSON bookkeeping, or tests are added to this JDK tree.

Preserve one source file per annotation commit; workflow/roadmap changes are separate.
Current source delta: Objects accepts a null varargs array for hash; Optional accepts
its empty singleton's null constructor value, specifies its existing empty cast's
element qualifier, and gives private value postconditions to presence predicates.
Existing CF and Optional Checker annotations remain in place.

## First-group contract review

| File | Documentation-backed change or verified existing contract | Limitation retained |
| --- | --- | --- |
| `Objects` | `hash` now accepts a nullable array reference, following its delegated `Arrays.hashCode` contract; elements were already nullable. Existing equality, fallback and guard contracts are retained. | `compare` returns zero for identical operands and otherwise delegates null policy to the comparator. One argument-key suppression preserves that conditional contract. |
| `Optional` | The private constructor accepts the documented empty singleton's null value; the existing empty-instance cast explicitly qualifies its element as nonnull. Presence predicates establish the private value's nonnull state on their appropriate boolean result. | A reduced CF conditional/wildcard supplier issue needs one method suppression. Existing CF class policy needs a location exception. |
| `OptionalInt` | Existing nonnull containers/streams, primitive payload, nullable equality input and normal-return behavior checked. | Existing CF class policy needs a location exception; inactive-null callback domain remains conservative. |
| `OptionalLong` | Same contracts reviewed against this file's own Javadoc and implementation. | Same class-policy and conditional-callback limitations. |
| `OptionalDouble` | Same contracts reviewed against this file's own Javadoc and implementation, including its distinct numeric equality semantics. | Same class-policy and conditional-callback limitations. |

The user explicitly chose to preserve the existing CF class policy.
The compatibility exceptions suppress only `jspecify.unrecognized.location.class`.
Four negative callers confirm that nullable Optional references remain rejected;
a separate invalid local annotation confirms that location checks remain enabled.
The comparator suppression is not classified as a checker bug. The polymorphic
conditional is a suspected checker defect: an equivalent minimal `if`/return formulation and direct wildcard
forwarding pass, while the conditional form fails in both profiles. Its exact root
cause is not established, and no checker implementation fix is included.
The [minimal reproducer and negative control](https://github.com/aosen-xiong/checker-framework/blob/502a5630341673eb659cedf265fc7576478b3d36/checker/tests/nullness/PolymorphicSupplierConditional.java)
document the method suppression; removing it restores exactly one conditional-type
diagnostic under the pinned implementation.

A host-JDK17 probe confirms five inactive-null callback calls return normally,
while the source-aware checker rejects them under the retained nonnull callback
preconditions. These calls remain a disclosed completeness gap. Checker success
must not be reported as complete coverage of that documented conditional domain.

Final local checkpoint: run `run.6SeaN1` verifies the inherited 136 java.lang
sources plus 5 java.util files. This is 5/120 direct java.util sources locally checked,
all with disclosed suppressions; 115 remain unattempted. Hosted java.util validation
and the conservative callback-domain limitation remain open.

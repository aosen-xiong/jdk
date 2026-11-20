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
The core layer is [PR #33](https://github.com/aosen-xiong/jdk/pull/33). The traversal
layer uses paired branch `codex/nullness-java-util-traversal` and targets that core
branch. Each subsequent group targets the preceding java.util branch. Hosted
validation is pending; local results below do not replace exact-head CI.

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
Group 2: traversal source/caller checks, all eleven removal controls, and the
cumulative 148-file Unix regression pass locally. Group 3: both comparison files
and their affected callers pass locally. Group 4 covers the eight collection
interfaces. Group 5 adds the map interfaces, and group 6 adds their abstract
collection counterparts. The Unix manifest covers all 31 files planned through
the collection-contracts milestone. Groups 7–25 cover the remaining 89 files.
package-info.java reviewed: existing
KeyFor lower-bound default retained; no general package nullness policy inferred.
The original checks below use CF c12ce38daa; the comparison tip now uses the
checker revision in the refresh checkpoint. Initialization, KeyFor, purity and
native execution remain outside the local source-check proof scope. Checker defects
are documented first and then narrowly suppressed with removal controls.

Conditional Optional callbacks are an explicit review boundary: existing nonnull
callback types are safe sufficient preconditions, but reject inactive-null callbacks
that the documented implementation never invokes. Do not call that full contract
coverage or widen callbacks to Nullable without preserving rejection of unsafe calls.

## First PR configuration

The core PR uses CF branch `codex/nullness-java-util-core`. Its workflow pins
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

Core local checkpoint: run `run.6SeaN1` verifies the inherited 136 java.lang
sources plus 5 java.util files. Hosted java.util validation and the conservative
callback-domain limitation remain open.

## Traversal contract review (group 2)

Seven files are in scope; four need source changes. Existing `Iterator`,
`ListIterator`, and `Enumeration` contracts pass without edits, preserving nullable
element substitutions and existing annotations for other checkers.

| File | Oracle and decision |
| --- | --- |
| `Iterator` | `next` returns the element type, not an extra null sentinel; `forEachRemaining` explicitly rejects a null action. Preserve existing contracts. |
| `ListIterator` | `next`/`previous` and `add`/`set` preserve the element type; the underlying list determines nullable-element eligibility. Preserve invariance and existing contracts. |
| `Enumeration` | `nextElement` and the `asIterator` adapter preserve element nullness; emptiness throws rather than returning an extra null. Preserve existing contracts. |
| `PrimitiveIterator` | Its generic `forEachRemaining` explicitly rejects a null action: add `@NonNull` to the `T_CONS` parameter use. Primitive boxing results remain nonnull. |
| `Spliterator` | The generic primitive callback methods have the same nonnull action requirement. Existing nullable split and natural-order comparator results remain. |
| `Spliterators` | Add missing nullable results to split/comparator overrides, nullable internal payload and lazy-source storage, and nonnull empty-spliterator callback parameters. Public array factories retain their existing polymorphic element contract. |
| `Tripwire` | Opt in the whole helper file. Class-name dereferencing requires a nonnull class; the message default remains an assumption, as its Javadoc has no explicit null clause. |

### Findings and narrow boundaries

The generic primitive callback gap is an annotation defect, not a checker bug.
With the published core sources, `PrimitiveIterator<Integer, @Nullable IntConsumer>`
and the analogous `Spliterator.OfPrimitive` type allow three null-action calls
contrary to their `@throws NullPointerException` clauses. Explicit `@NonNull`
parameter uses reject all three while preserving valid calls and generic bounds.

Eight diagnostic-specific method suppressions in `Spliterators` describe internal
invariants that the current analysis cannot establish. They are not classified
as confirmed checker defects:

- Two adapter methods consume a `T` only when `valueReady` is true. Its storage
  is null before filling and after clearing; `T` may itself be nullable, so an
  unconditional `@EnsuresNonNull` promise would be wrong.
- Two array traversal methods consume only the active range containing `T` values;
  the existing `Object[]` representation and casts erase that relationship.
- Four lazy iterator methods rely on constructors establishing that either the
  iterator or collection is nonnull. The collection is present whenever the
  lazy iterator is absent.

The baseline `Spliterators` run reports 28 errors; the annotated file passes.
The CF `TraversalNullness` fixture checks valid nullable/nonnullable elements,
factory contracts, split/comparator results, all three primitive specializations,
and callback rejection: 31 expected invalid-use diagnostics in each of JSpecify
and ordinary nullness profiles. Tests remain exclusively in the paired CF branch.
The traversal workflow pins [CF a4e96ed](https://github.com/aosen-xiong/checker-framework/commit/a4e96ede63249afe193cc461ec66935537a68b54);
the [caller fixture](https://github.com/aosen-xiong/checker-framework/blob/a4e96ede63249afe193cc461ec66935537a68b54/checker/tests/nullness/TraversalNullness.java)
includes the three generic-callback regression controls. This changes tests only;
the checker implementation and study profile are unchanged.
No checker implementation change, executable JDK change, blanket suppression,
or new opt-out is included. The CI job budget grows to 90 minutes to accommodate
the cumulative source checks and helper callers as the verified set expands.

Final traversal checkpoint: runs `run.6roSeF`, `run.6lALRQ`, and `run.jYpCki`
partition the same 148-file regression set without duplicates. All selected files
were visited and completed with zero errors, warnings, crashes, or truncation;
141 physical source hashes stayed unchanged. The three contexts generate fresh
CharacterData sources and reuse a provenance-checked configured VersionProps
artifact from the earlier java.lang CI. Exact-head native generation is left to
hosted CI. This brings local direct java.util coverage to 12/120 files, with
108 remaining. Six traversal files pass without nullness suppressions; only
`Spliterators` needs the eight documented boundaries.

Review queue for later groups: source inspection found that `SortedSet.spliterator`
has an anonymous `getComparator` override with a nonnull default even though it
forwards the documented nullable `SortedSet.comparator` result. Review this in
group 4. `Comparators.NullComparator` stores an optional delegate and accepts null
when all nonnull elements compare equal; its field/constructor annotations need
review in group 3. These are observed annotation gaps, not reproduced checker
bugs or completed coverage of those files.


## Comparison contract review (group 3)

The comparison layer targets the traversal branch (PR #34). Both `Comparator`
and `Comparators` are selected; only `Comparators` needs source changes. Public
`Comparator` contracts already distinguish strict operands, nullable-friendly
comparators, optional null-ordering delegates, and key extractors. They remain
unchanged. `Comparators` receives whole-file nullness opt-in.

`nullsFirst` and `nullsLast` explicitly allow a null delegate. Accordingly, the
private delegate field and constructor parameter become nullable. The helper
checks both operands before invoking a present delegate. Its stored comparator,
constructor wildcard lower bound, existing cast, and secondary comparator lower
bound therefore use `@NonNull T`. These four qualifiers narrow type-variable
uses; ordinary concrete reference types keep the existing nonnull default. The
secondary comparator is invoked only through the same null-guarding wrapper.
This refines the internal override with a weaker caller precondition, preserving
the public `Comparator` contract. Executable code is unchanged.

### Checker findings

Two reduced cases are retained in the matching Checker Framework branch:

- **NULL-0045, reproduced checker crash:** a candidate implementation of
  `Comparator<@Nullable T>` crashes with `StructuralEqualityComparer: unexpected
  combination` for `NULL` and `TYPEVAR`, through `visitNull_Typevar` and conditional
  checking. The complete source failure repeats in a fresh run; a standalone
  example reproduces in both JSpecify and ordinary nullness modes without a JDK
  source patch. Plain javac succeeds. Its root cause is unconfirmed. The crashing
  candidate is rejected, and its CF test is explicitly skipped until fixed; it is
  not counted as a passing test or a suppressed crash.
- **NULL-0046, reproduced suspected conditional/wildcard defect:** the initial
  representation reports `conditional.type.incompatible` when choosing between
  `other` and `real.thenComparing(other)`. Both alternatives accept nonnull `T`,
  as required by the constructor. A standalone example reports the same single
  diagnostic in both profiles; equivalent separate returns pass. An initial narrow
  suppression was documented and validated by removal, then retired: recording
  the secondary comparator's nonnull input domain also makes the conditional
  check succeed. The final JDK source needs no suppression or expression rewrite.
  The reduced diagnostic fixture preserves the narrower experiment separately.
  Its relationship to the crash is not established.

The CF-owned `ComparatorNullness` fixture exercises operand domains, reverse and
null ordering, comparator chaining, nullable extracted keys, and primitive key
extractors. It expects 23 invalid-use diagnostics in each profile. The reduced
conditional fixture adds two unsafe-use controls. `ComparisonHelperContracts`
checks that the concrete wrapper accepts strict delegates while comparing nullable
operands, including a missing primary delegate. Tests and reproducers remain
in CF; no tests or harness files are added to this JDK repository.

The syntax audit confirms annotation-only edits, no lost other-checker
annotations and no scope opt-outs. The final source uses no nullness suppression.
The final source and affected-caller validation are recorded below; exact-head
hosted validation remains pending.

The original comparison workflow pinned [CF 6281829](https://github.com/aosen-xiong/checker-framework/commit/628182975650b61bd275d89bb2f71b4594c93278).
Its [caller contracts](https://github.com/aosen-xiong/checker-framework/blob/628182975650b61bd275d89bb2f71b4594c93278/checker/tests/nullness/ComparatorNullness.java),
[conditional controls](https://github.com/aosen-xiong/checker-framework/blob/628182975650b61bd275d89bb2f71b4594c93278/checker/tests/nullness/ComparatorConditional.java),
and [skipped crash reproducer](https://github.com/aosen-xiong/checker-framework/blob/628182975650b61bd275d89bb2f71b4594c93278/checker/tests/nullness/ComparatorConditionalCrash.java)
are reviewable independently of the JDK annotations. At that checkpoint, the
checker implementation remained c12ce38daa; those were test-only additions. Run the skipped reproducer
explicitly with the JDK 17 checker wrapper and `-processor nullness
-Amode=jspecify -proc:only` to reproduce the crash; omit the mode flag for the
ordinary-profile reproduction. The successful javac control uses `-proc:none`.

Final comparison checkpoint: the earlier complete 150-file Unix regression
(`run.N0OyoS`, `run.sOCuHM`, `run.Ar2Pq1`) passed with stable 143 physical-source
hashes while the first representation still had its single conditional suppression.
After the final secondary-delegate refinement removed that suppression,
`run.LfnIhX` verified all 14 covered java.util files plus the concrete helper
caller, with no errors, warnings, crashes, or skipped targets. Public comparator
controls were replayed in both profiles and matched all 23 expected diagnostics.
The reduced conditional fixture separately matches its two negative controls.
The private helper is referenced only by `Comparator` and itself in the shared
JDK sources; the public `Comparator` signatures did not change.

These are distinct source snapshots: the earlier 150-file result is not a claim
of a full final-snapshot rerun. The fork's CI checks the complete final set and
builds the native JDK. Local checks generated fresh CharacterData and reused
provenance-checked VersionProps from the prior java.lang CI. Direct java.util
coverage is 14/120 files; 106 remain. Source annotation delta: two Nullable uses,
four NonNull type-variable uses, one whole-file opt-in, and zero new nullness
suppression keys. Comparator.java is unchanged.


## Checker refresh, 2026-11-19

The comparison PR's matching CF branch now merges EISOP master
`6ac6f7813440db1cd42b9a83aeccd102180930d4`, including the generated-record-method
fix in [EISOP CF #2636](https://github.com/eisop/checker-framework/pull/2636).
The checker was rebuilt with JDK 21 and the same bundled JDK source revision
`0af1a5ad1f994431fc6e08540000c4ae1ab13153`. Source checks still use JDK 17.0.14,
CF annotations, and the existing JSpecify mode. The runner and qualifier JAR are
unchanged; the rebuilt checker JAR is a new artifact. Positive and negative mode
probes confirm the expected opt-in/defaulting behavior and location diagnostics.

The previous record-equals workaround now triggers `unneeded.suppression`.
`RecordValueNullness.generatedEquals` therefore calls `item.equals(null)` without
a suppression. The nullable component dereference and two invalid EnumDesc calls
remain negative controls. No JDK annotation or executable source changes are
required for this checker fix; tests stay in CF.

The original comparison head `d22796cf5aaa2c5f8f4c32cd5d6a2a6f18ab08e1` passed
all hosted checks, including the native build and both source-check matrix legs.
Those results belong to the previous checker. Targeted upgrade validation and
new full CI results are tracked separately below.

The upgraded workflow pins [CF 95a0ac01388d9465288d965dd0cfe0af2bbd117c](https://github.com/aosen-xiong/checker-framework/commit/95a0ac01388d9465288d965dd0cfe0af2bbd117c),
which includes current EISOP master plus the study runner and fixtures. The
[record caller](https://github.com/aosen-xiong/checker-framework/blob/95a0ac01388d9465288d965dd0cfe0af2bbd117c/checker/tests/nullness/RecordValueNullness.java)
now exercises generated equality directly without a workaround.

Upgrade validation: `RecordValueNullness`, `ObjectValueNullness`,
`ComparatorNullness`, and `ComparatorConditional` match respectively 3, 5, 23,
and 2 intended invalid-use diagnostics in each of JSpecify and ordinary nullness
profiles. No unexpected warning or crash occurs in those fixtures. Source run
`run.5mT0nQ` checks Object, Record, Comparator, Comparators, and the concrete
comparison helper caller successfully. The unrelated NULL-0045 comparator crash
still reproduces in both profiles; its skipped reproducer remains open. The
NULL-0046 reduced fixture still needs its narrow suppression, while the final
JDK comparator implementation remains suppression-free.

The full upgraded Unix/Windows source checks and native JDK build run in CI.
The previous 150-file local runs and prior green CI are retained as historical
results and are not relabeled as checks of this new checker artifact.

## Group 4. Collection interfaces

The JDK 17 Javadoc for `Collection.toArray(IntFunction)` requires the generator
to create an array of the requested length. The method copies the receiver's
elements, including any nulls. The generator selects the runtime array type.
A collection containing a single null previously passed the checker and threw
`NullPointerException` at `names.toArray(String[]::new)[0].length()`.
[Upstream annotation question and executable example](https://github.com/eisop/checker-framework/issues/2656)

The study uses this CF contract for the generator overload.

```java
default <T> @PolyNull T[] toArray(Collection<@PolyNull E> this, IntFunction<T[]> generator)
```

`@PolyNull` applies to the returned array's elements. The method has two
diagnostic-specific suppressions. JSpecify excludes a type argument on an
explicit receiver from its recognized locations. The default implementation
also delegates to the array overload, whose return allows the trailing null of
an oversized destination. A conforming generator supplies length zero here, so
that extra slot cannot occur. Removing either key restores its own diagnostic.
The pre-existing no-argument declarations in Collection, List and Set retain
their polymorphic contracts with the receiver-location exception alone.
[JSpecify annotation locations](https://jspecify.dev/docs/spec/#recognized-locations-for-type-use-annotations)

| Source | Evidence and decision |
| --- | --- |
| Collection | Both array-returning contracts above preserve the receiver's element nullness. The caller-supplied array overload retains its oversized-array contract. |
| List | The sort Javadoc permits a null comparator for natural order. Its temporary array may store null elements. Arrays.sort currently requires a nonnull comparator. ListIterator.set cannot recover E from the erased temporary array after sorting. Both calls use the argument diagnostic exception. Revisit the former in group 12. |
| Set | The inherited element semantics also apply to its redeclared no-argument toArray. |
| SortedSet | Its default spliterator returns the set's comparator. Natural ordering returns null, so its anonymous getComparator override needs a nullable result. |
| NavigableSet | Neighbor queries and polling can return null when no element qualifies. Existing declarations cover these results. |
| Queue and Deque | Peek and poll return null on absence. Element and getFirst throw on an empty receiver and preserve the element type on success. |
| RandomAccess | Marker interface with no member contracts. |

The eight interfaces already opt into nullness checking. Four needed source
changes. Six new method/diagnostic combinations across Collection, List and Set
were removed individually in scratch copies. The four receiver locations each
produced one diagnostic, the default delegation produced one, and List.sort
produced two argument diagnostics. Reverting the List temporary component and
SortedSet comparator qualifiers separately restored the original diagnostics.
The four changed interfaces and the Collections wrapper changes below produced
64 class files with identical JVM method descriptors and instructions before and
after annotation.

Four overrides in Collections forward this overload to a backing collection or
deque. The unmodifiable, synchronized, checked and LIFO wrappers preserve the
element contract of their backing view. Checking the entire file against only
the changed interfaces exposed eight new errors at those four overrides. Giving
each override the same element relationship and just the receiver-location
exception cleared all eight. Each wrapper's exception has its own removal control.
The rest of Collections has 204 pre-existing errors and two warnings on both
snapshots. It remains outside the enrolled set until its full group 11 review.

The CF caller fixture exercises nullable, nonnull and guarded array elements,
assignment to a nonnull-component array, inherited List and Set calls, all
four concrete overrides, natural ordering, and the absence contracts of
NavigableSet, Queue and Deque. The JDK workflow uses the existing CF source
runner on Unix with unused suppressions treated as errors.

Both checker modes produced the same 12 intended diagnostics after removing the
test expectations. On the parent signatures, four existing diagnostics remained
and all eight unsafe array uses passed. Generic array allocation with a nonnull
element collection and a guarded nullable element both passed on the new signatures.
[CF caller fixture](https://github.com/aosen-xiong/checker-framework/blob/dcee2774c697693ce8616cdc2246b860df9f2ec7/checker/tests/jdk-source/java.base/java/util/CollectionInterfaceContracts.java)

## Group 5. Map interfaces

All three files already declare nullness coverage. The JDK 17 contracts distinguish
absence, an explicitly stored null, and a null callback result that declines or removes
a mapping. SortedMap.comparator returns null for natural order. Its extremal key methods
throw on an empty map. NavigableMap's neighbor keys and entries, and its polling methods,
can return null on absence. The existing sorted and navigable declarations cover those
cases. The Map factory and Entry.copyOf declarations reject null inputs as documented.

The Map default methods forward a key of type K to an erased Object lookup. The
conservative lookup signature allows implementations to reject null. Seven narrow
argument suppressions preserve that public policy. In merge, the remapper may return
null to request deletion. The implementation checks that result before insertion.
The eighth suppression covers its conditional expression. Removing each suppression
separately restores one diagnostic on the stated expression. The ten caller controls
cover lookups, remapping, ordered views and immutable factories in ordinary nullness
and JSpecify mode. The corresponding safe uses pass in each mode.

Two limits matter when interpreting lookup results:

- On a Map with nonnull values, JSpecify mode enables the checker's assumeKeyFor
  option. It accepts an unguarded dereference of get on a missing key. Ordinary
  nullness mode flags the same use. Neither result changes the API's nullable return.
- A Map with nonnull values may legally receive a null fallback in getOrDefault.
  The existing V fallback type rejects this caller. A scratch contract tying the
  receiver's V, fallback and result to a single PolyNull also rejected the legal
  guarded caller due to the invariant receiver. The study retains the conservative
  signature. Inferring results from the fallback alone would miss a stored null.

### Existing fork discrepancy in conditional removal

The inherited JDK source assigns the key itself to curValue in Map.remove(key, value).
Its own implementation specification compares the stored value. A minimal AbstractMap
backed by a HashMap exercised the default method with `"k"` mapped to `"v"`.

| Call on a fresh map | Stock OpenJDK 17 | Stock runtime patched with the fork's Map class |
| --- | --- | --- |
| `remove("k", "v")` | true, entry removed | false, entry retained |
| `remove("k", "k")` | false, entry retained | true, entry removed |

This predates the annotation stack. The annotation PR preserves the executable body.
[Parent source](https://github.com/aosen-xiong/jdk/blob/94e3491d847342e79ca2f4c1232c20d95e171dd7/src/java.base/share/classes/java/util/Map.java#L920-L930)
and [OpenJDK 17 implementation](https://github.com/openjdk/jdk17u/blob/master/src/java.base/share/classes/java/util/Map.java).

[Caller fixture on the matching Checker Framework branch](https://github.com/aosen-xiong/checker-framework/blob/ce50cf3e282b77b8a97cbd73d9de9a9c701579ba/checker/tests/jdk-source/java.base/java/util/MapInterfaceContracts.java)

## Group 6. Abstract collection implementations

These six files finish the planned 31-file Unix scope of the collection-contracts
milestone. They all already opt into nullness checking. Four needed changes.

| Source | Contract checked against JDK 17 |
| --- | --- |
| AbstractCollection | No-argument toArray returns precisely the iterator's elements. Its temporary and growing arrays can contain nulls until the initialized prefix is returned. The typed overload writes a null sentinel into an oversized caller array. Every runtime array class has a component type. removeAll and retainAll may encounter a collection that rejects null. |
| AbstractList | RandomAccessSpliterator only stores an AbstractList for matching list implementations. Its split result is nullable when subdivision is impossible. Outermost SubList has no parent. |
| AbstractSequentialList | Iterator-based access preserves E. Invalid positions use exceptions. |
| AbstractSet | Equality accepts an arbitrary set and catches null rejection. Bulk removal may propagate the argument collection's rejection of an element. |
| AbstractMap | keySet and values are lazy caches and clone clears both. Their public accessors return initialized views. The internal entry equality helper accepts null on either side. Equality catches optional null-key rejection by the other map. |
| AbstractQueue | The default remove and element throw on an empty queue. Inherited poll and peek may signal absence with null. The LIFO adapter overrides the head operations and can wrap a deque whose element type permits null. A class-wide nonnull element bound rejected a valid adapter view in a caller probe, so the existing generic domain is retained. |

The private finishToArray helper accepts and returns potentially nullable array
components. The public no-argument override preserves the polymorphic element
contract. Its suppression for returned elements is confined to the override,
where the documented initialization of the prefix guarantees the result. The
reflective allocation, sentinel write, receiver location and bulk-query
exceptions are audited independently. Nine new source suppression keys across
three files each restore the intended diagnostic(s) when removed. The fourth
changed file, AbstractList, needs no suppression.

Seven invalid caller uses exercise nullable array/list elements, inability to
split, both uninitialized map caches, nullable entry values and an empty queue.
Positive callers exercise array conversions, initialized public views, guarded
access, iteration and throwing queue operations. Both checker modes use the
same patched sources. The existing CF runner checks the enrolled files and
caller fixtures on Unix.

Five qualifier-removal checks independently recover the original diagnostics
on the absent spliterator backing list, exhausted split, root sublist parent
and both cloned map-view caches. Source checks of HashMap, LinkedHashMap,
TreeMap, EnumMap, IdentityHashMap and WeakHashMap produced no new diagnostics
relative to the parent. Two existing HashMap cache-reset errors disappeared.
These six concrete classes are comparison subjects for later groups.

A JDK 17 disassembly check across both PRs found the same method descriptors
and executable instructions in all 18 class files emitted from the five
changed sources. The earlier conditional-removal discrepancy originates in
[EISOP JDK commit d792ac4](https://github.com/eisop/jdk/commit/d792ac4e84be3f9bb3aade9da27ef896f880d915).

[Caller fixture on the matching Checker Framework branch](https://github.com/aosen-xiong/checker-framework/blob/7d6de84cdec51f5c13f602e363d753e7857a5476/checker/tests/jdk-source/java.base/java/util/AbstractCollectionContracts.java)

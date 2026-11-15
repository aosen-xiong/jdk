---
name: jdk-nullness-annotation
description: Use when adding or checking nullness annotations in eisop/jdk with the Nullness Checker's JSpecify mode — porting annotations from the JSpecify jdk, marking a package @AnnotatedFor("nullness"), or type-checking JDK sources with --patch-module. Triggers on "annotate the JDK", "java.time"/"java.util..." nullness, "@AnnotatedFor on package-info", "port from jspecify/jdk", "patch-module", "TypecheckedList". Codifies the setup, the measure-after-every-batch loop, the fix order, and the traps that make a clean run meaningless.
---

# Annotating eisop/jdk for nullness in JSpecify mode

Neither eisop/jdk nor the JSpecify jdk is fully annotated (about a quarter and a third of `java.base`'s
public API).  The work is: mark a package, type-check its implementation against its own annotations,
and drive the error count to zero with real annotations first and justified suppressions last.  The
`java.time` pilot (66 files, 210 -> 0) is the worked example; its notes are in `NOTES.md` of the work
directory it ran from.

## Setup

1. **A separate eisop/jdk worktree** on its own branch, from `origin/master`.  Do not edit the shared
   `jdk` checkout that sits beside the Checker Framework: its build reads it.
2. **A Checker Framework checkout that can run `-Amode=jspecify`.**  Until eisop#2273 is merged, the mode
   crashes with "`flowResult` is null" on almost any class; apply #2273 to the checkout.
3. **A work directory** (`$WORK`, outside both repositories) holding `TypecheckedList.txt`, the jars and
   the logs.
4. Build the jars **from this worktree's annotations**:
   ```bash
   CF=<checker-framework checkout> WORK=<work dir> scripts/rebuild-checker.sh
   ```
   Rerun it after every batch of annotation changes.  `check.sh` reads every JDK declaration that is not
   in the list, and the target of every `Interface.super.m()` call even when it is, from the annotated
   JDK bundled in `checker.jar`.  A jar built from the shared `jdk` reports errors against annotations
   you already changed.
5. javac must match the JDK's feature version (`make/conf/version-numbers.conf`; 17 today).
   `check.sh` picks it.

## Mark the scope with package-level @AnnotatedFor

JSpecify mode checks only code in an `@AnnotatedFor("nullness")` (or `@NullMarked`) scope; an unmarked
file reports 0 errors whatever it contains.  Mark packages, not classes, in `package-info.java`:

```java
@AnnotatedFor({"nullness"})
package java.time.temporal;

import org.checkerframework.framework.qual.AnnotatedFor;
```

**`@AnnotatedFor` on a package also covers its subpackages** (`BaseTypeChecker`), unlike JSpecify's
package-level `@NullMarked`.  Marking `java.time` puts `java.time.temporal`, `chrono`, `format` and
`zone` in scope too, even where they are only read from `checker.jar`: their unannotated parameters
become non-null instead of the mode's permissive `@Nullable`.  In the pilot that alone took 210 errors
to 15.

Put every file of every marked package in `TypecheckedList.txt` (paths relative to
`src/java.base/share/classes`), and include the packages that hold the marked classes' supertypes.
Overrides are checked against them.

## The check

```bash
WORK=<work dir> scripts/check.sh
```

It is the pico-artifact command (`Artifact-Evaluation-Checker.md`) with `-processor nullness
-Amode=jspecify`: `--patch-module java.base=<jdk>/src/java.base` (so only the listed files are read from
source), `--add-reads java.base=ALL-UNNAMED`, `-XDignore.symbol.file=true`, `-Xmaxerrs 5000`.  It prints
the javac exit, **the number of files checked**, the error and crash counts, and the error keys.

**Before trusting a 0, plant an error** in one file of each package (`Object p = null; p.toString();`),
see it reported, and restore the file.  Two ways the pilot got a meaningless count:
- the list had silently been overwritten with a smaller one (check the printed file count);
- the jar had been built from the shared JDK (rebuild it).

## The loop

Keep a table in `$WORK/NOTES.md`: one row per batch, with files checked, errors, and the delta.  Never
take a step without measuring it.

1. **Port JSpecify's annotations.**
   `scripts/port-jspecify.py <jspecify classes dir> <eisop classes dir> <package dir>...` copies a
   JSpecify line containing `@Nullable` onto the eisop line that matches once nullness annotations are
   stripped.  The simple name is the same, so it only adds the Checker Framework import.  It reports
   the lines it could not place; do those by hand.  They are usually a widened type parameter
   (`<R>` -> `<R extends @Nullable Object>`), a type argument on a field's type, or several identical
   lines (all the `equals(Object)` of nested classes).
2. **Real annotations, from the Javadoc.**  "@return ..., null if ..." is a `@Nullable` return; "null if
   no preference" is a `@Nullable` parameter.  JSpecify often left unmarked the overrides of a method
   it made `@Nullable` (`IsoChronology.resolveDate`); annotate every override that returns null.
3. **Make overrides agree with their supertypes.**  If an interface method's parameter is `@Nullable`,
   so is every implementation's, including anonymous ones.  If it widened a type parameter
   (`TemporalAccessor.query`'s `<R extends @Nullable Object>`), every override takes the same bound, or
   callers through the subclass get type-argument errors.
4. **Narrow, justified suppressions last**, for invariants the checker cannot see:
   ```java
   @CFComment("nullness: resolveDate calls this only after checking fieldValues.containsKey for every field removed here")
   @SuppressWarnings("nullness:unboxing")
   ```
   Use the narrowest key (`nullness:return`, `nullness:unboxing`, `nullness:dereference`,
   `nullness:argument`), on the smallest declaration, always with a `@CFComment`.  Recurring cases in
   `java.time`: `Map.remove` after `containsKey` in another method; objects read back in `readExternal`;
   `query()` returning null for queries chosen by `==`.
5. **Checker false positives** get the same suppression, with "false positive:" in the comment, plus a
   minimized repro for an EISOP issue.  Found so far: a lambda in a `?:` branch does not get its
   target's `@Nullable` type argument (eisop#2310).

## Things that are not annotations

- `@Nullable` on a local or a try-with-resources variable: locals get their nullness from flow, and
  JSpecify mode reports the annotation as `jspecify.unrecognized.location.*`.
- `Map.remove`/`get` are correctly `@Nullable`; do not change library signatures to silence a caller.

## When done

Rebuild, check, plant an error, and record the final row.  Do not commit until the user says so.  The
branch's annotation changes go to eisop/jdk; a Checker Framework bug you found goes to an EISOP issue,
not into the JDK.

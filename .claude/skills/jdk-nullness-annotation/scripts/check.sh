#!/bin/bash
# Type-checks the files in $WORK/TypecheckedList.txt (paths relative to src/java.base/share/classes)
# with the Nullness Checker in JSpecify mode, patching java.base from this eisop/jdk checkout.
# The patch root is src/java.base, not .../share/classes, so only the listed files are read from
# source; every other JDK declaration comes from the annotated JDK inside $WORK/checker.jar, which
# rebuild-checker.sh builds from this checkout.
#   WORK=<dir with checker.jar, checker-qual.jar, TypecheckedList.txt> check.sh [extra javac args]
set -u
WORK=${WORK:?set WORK}
JDK=${JDK:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}
FEATURE=$(sed -n 's/^DEFAULT_VERSION_FEATURE=//p' "$JDK/make/conf/version-numbers.conf")
J=$(/usr/libexec/java_home -v "$FEATURE")
X=(); for p in api code comp file main model parser processing tree util; do X+=(-J--add-exports=jdk.compiler/com.sun.tools.javac.$p=ALL-UNNAMED -J--add-opens=jdk.compiler/com.sun.tools.javac.$p=ALL-UNNAMED); done
rm -rf "$WORK/out"; mkdir -p "$WORK/out"
"$J/bin/javac" "${X[@]}" -d "$WORK/out" \
  -cp "$WORK/checker-qual.jar" -processorpath "$WORK/checker.jar" \
  -processor org.checkerframework.checker.nullness.NullnessChecker -Amode=jspecify \
  --patch-module java.base="$JDK/src/java.base" --add-reads java.base=ALL-UNNAMED \
  -Xmaxerrs 5000 -Xlint:none -Alint=-all -XDignore.symbol.file=true "$@" \
  $(sed "s#^#$JDK/src/java.base/share/classes/#" "$WORK/TypecheckedList.txt") > "$WORK/compile.log" 2>&1
echo "javac $FEATURE exit: $?  files checked: $(grep -c . "$WORK/TypecheckedList.txt")"
echo "errors: $(grep -cE '\.java:[0-9]+: error:' "$WORK/compile.log")  crashes: $(grep -c 'The Checker Framework crashed' "$WORK/compile.log")"
grep -oE '\.java:[0-9]+: error: \[[a-z.]+\]' "$WORK/compile.log" | grep -oE '\[[a-z.]+\]' | sort | uniq -c | sort -rn | head -12

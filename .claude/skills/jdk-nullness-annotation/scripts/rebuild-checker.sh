#!/bin/bash
# Builds checker.jar and checker-qual.jar from the Checker Framework checkout $CF, with the annotated
# JDK taken from this eisop/jdk checkout, and copies them to $WORK.  Run it after every annotation
# change: check.sh reads every unlisted JDK declaration (and the targets of Interface.super calls,
# even listed ones) from the annotated JDK inside checker.jar.
#   CF=<checker-framework checkout> WORK=<dir> rebuild-checker.sh
set -eu
CF=${CF:?set CF}; WORK=${WORK:?set WORK}
JDK=${JDK:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}
mkdir -p "$WORK"
(cd "$CF" && JAVA_HOME=$(/usr/libexec/java_home -v 21) ./gradlew :checker:shadowJar :checker-qual:jar \
  -PannotatedJdkHome="$JDK" --no-configuration-cache --console=plain > "$WORK/build-checker.log" 2>&1)
cp "$CF"/checker/build/libs/checker-*-SNAPSHOT-all.jar "$WORK/checker.jar"
cp "$(ls "$CF"/checker-qual/build/libs/checker-qual-*-SNAPSHOT.jar | grep -v -- '-sources\|-javadoc' | head -1)" "$WORK/checker-qual.jar"
echo "checker.jar from $(git -C "$CF" rev-parse --short HEAD)$(git -C "$CF" diff HEAD --quiet || echo ' (with uncommitted changes)'), annotated JDK from $JDK"

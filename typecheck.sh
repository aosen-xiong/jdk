#!/bin/bash
# Run a Checker Framework checker on complete JDK packages, one file at a time.
# Usage: CHECKERFRAMEWORK=/path/to/checker-framework ./typecheck.sh CHECKER MODULE PACKAGE...
# JAVA_HOME must identify a compiler compatible with this JDK's sources (JDK 17).
set -euo pipefail

if [[ $# -lt 3 ]]; then
    echo "Usage: $0 CHECKER MODULE PACKAGE..." >&2
    exit 2
fi
ROOT=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
CHECKERFRAMEWORK=${CHECKERFRAMEWORK:-"$ROOT/../checker-framework"}
checker=$1
module=$2
shift 2
module_root="$ROOT/src/$module/share/classes"
javac="$CHECKERFRAMEWORK/checker/bin/javac"
qualifiers="$CHECKERFRAMEWORK/checker/dist/checker-qual.jar"
[[ -x "$javac" && -f "$qualifiers" && -d "$module_root" ]] || {
    echo "Build Checker Framework and select a valid JDK module first." >&2
    exit 2
}
if [[ -n ${JAVA_HOME:-} ]]; then
    export PATH="$JAVA_HOME/bin:$PATH"
fi
mkdir -p "$ROOT/build/typecheck"
output=$(mktemp -d "$ROOT/build/typecheck/run.XXXXXX")
echo "Type-checking logs: $output"
{
    git -C "$ROOT" rev-parse HEAD
    git -C "$CHECKERFRAMEWORK" rev-parse HEAD
    java -version
} > "$output/toolchain.log" 2>&1

options=(-processor "$checker" -proc:only -implicit:none -Afilenames
         -AprintVerboseGenerics -Xmaxerrs 5000 -Xmaxwarns 5000 -Werror
         --add-reads "$module=ALL-UNNAMED" -classpath "$qualifiers")
if [[ "$checker" == nullness ]]; then
    options+=(-Amode=jspecify -AwarnUnneededSuppressions)
fi

check_file() {
    local source=$1 patch_roots=$2 fixture=$3 name run status
    name=$(basename "$source" .java)
    run="$output/$package/$name"
    mkdir -p "$run/classes" "$run/generated"
    if [[ "$checker" == nullness ]] && ! tr '\n' ' ' < "$source" |
        grep -E '@AnnotatedFor\([^)]*"nullness"' > /dev/null; then
        echo "Missing nullness opt-in: $source" >&2
        return 1
    fi
    local command=("$javac" "${options[@]}" --patch-module "$module=$patch_roots"
                   -d "$run/classes" -s "$run/generated" "$source")
    printf '%q ' "${command[@]}" > "$run/command.txt"
    printf '\n' >> "$run/command.txt"
    status=0
    "${command[@]}" > "$run/compile.log" 2>&1 || status=$?
    printf '%s\n' "$status" > "$run/exit-status.txt"
    cat "$run/compile.log"
    grep -Fq "is type-checking $source" "$run/compile.log" || return 1
    if grep -Eq 'crashed|Exception in thread|An exception has occurred in the compiler|only showing the first|warning:' "$run/compile.log"; then
        return 1
    fi
    if [[ "$fixture" == no ]]; then
        return "$status"
    fi
    # Contract fixtures use the Checker Framework test suite's expected-error syntax.
    sed -n 's/.*\/\/ :: error: (\([^)]*\)).*/\1/p' "$source" | sort > "$run/expected.txt"
    sed -n 's/.*error: \[\([^]]*\)\].*/\1/p' "$run/compile.log" | sort > "$run/actual.txt"
    sed -n '/error:/ { /error: \[/!p; }' "$run/compile.log" > "$run/compiler-errors.txt"
    [[ ! -s "$run/compiler-errors.txt" ]] || return 1
    if [[ -s "$run/expected.txt" ]]; then
        [[ "$status" == 1 ]] || return 1
    else
        [[ "$status" == 0 ]] || return 1
    fi
    diff -u "$run/expected.txt" "$run/actual.txt"
}

for package in "$@"; do
    package_path=${package//.//}
    package_root="$module_root/$package_path"
    [[ -d "$package_root" ]] || { echo "No package: $package" >&2; exit 2; }
    list="$output/$package.sources"
    find "$package_root" -maxdepth 1 -name '*.java' ! -name package-info.java | sort > "$list"
    [[ -s "$list" ]] || { echo "No source files: $package" >&2; exit 2; }
    while IFS= read -r source; do
        check_file "$source" "$module_root" no
    done < "$list"
    test_root="$ROOT/test/typecheck/$checker/$module"
    if [[ -d "$test_root/$package_path" ]]; then
        for source in "$test_root/$package_path/"*.java; do
            [[ -f "$source" ]] || continue
            check_file "$source" "$test_root:$module_root" yes
        done
    fi
done

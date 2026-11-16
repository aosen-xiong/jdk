"""Run pinned, per-file JDK nullness experiments and retain their evidence."""

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
JDK = HERE.parents[1]
CLEAN = {"clean-without-suppressions"}
OUTPUT = JDK / ".nullness-ci"
CRASH = re.compile(
    r"The Checker Framework crashed|Exception in thread|"
    r"An exception has occurred in the compiler|A fatal error has been detected|"
    r"^\s*(?:Caused by: )?(?:java|com\.sun|org\.checkerframework)"
    r"\.[\w.$]*(?:Exception|Error)(?::|$)",
    re.MULTILINE,
)


def digest(path):
    """Return a file's SHA-256 digest."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    """Write a human-readable JSON artifact."""
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def git(*args):
    """Read Git metadata without invoking a shell."""
    return subprocess.check_output(["git", "-C", str(JDK), *args], text=True).strip()


def classify(log, exit_code, timed_out, source, source_hash, review):
    """Classify completion conservatively; zero diagnostics alone is not clean."""
    keys = Counter(re.findall(r"error: \[([^]]+)\]", log))
    javac_errors = [
        line
        for line in log.splitlines()
        if "error:" in line and not re.search(r"error: \[[^]]+\]", line)
    ]
    visited = any(
        "NullnessNoInitSubchecker is type-checking " + str(source) in line
        for line in log.splitlines()
    )
    result = {
        "diagnostics_by_key": dict(keys),
        "warnings_by_key": dict(Counter(re.findall(r"warning: \[([^]]+)\]", log))),
        "javac_error_lines": javac_errors,
        "visited": visited,
        "crash": bool(CRASH.search(log)),
        "truncated": "only showing the first" in log,
    }
    review_valid = bool(
        review
        and review.get("source_sha256") == source_hash
        and review.get("all_declarations_reviewed") is True
        and review.get("top_level_declarations")
        and review.get("basis")
    )
    result["review_valid"] = review_valid
    if timed_out:
        status = "timed-out"
    elif result["crash"]:
        status = "checker-or-compiler-crashed"
    elif "not recognized by any processor" in log or "Unrecognized mode" in log:
        status = "profile-unsupported"
    elif result["truncated"]:
        status = "incomplete-diagnostics"
    elif javac_errors:
        status = "compiler-blocked"
    elif keys:
        status = "checked-with-diagnostics"
    elif exit_code != 0:
        status = "failed-without-classified-diagnostics"
    elif not visited:
        status = "not-visited"
    elif not review_valid:
        status = "scope-review-required"
    elif not review.get("opted_in"):
        status = "not-opted-in"
    elif "warning:" in log:
        status = "completed-with-warnings"
    elif review.get("suppression_keys"):
        status = "clean-with-suppressions"
    else:
        status = "clean-without-suppressions"
    result["status"] = status
    return result


class Study:
    """A pinned checker/compiler profile and its persistent run directory."""

    def __init__(self, label, audit_suppressions=False, profile_path=None):
        """Validate artifacts and initialize a new immutable experiment directory."""
        self.profile_path = (
            Path(profile_path).resolve() if profile_path else OUTPUT / "profile.json"
        )
        self.profile = json.loads(self.profile_path.read_text())
        self.toolchain = Path(self.profile["toolchain_root"]).resolve()
        config = json.loads((HERE / "config.json").read_text())
        for key, value in config.items():
            if key != "name" and self.profile.get(key) != value:
                raise ValueError(
                    f"Runtime profile differs from the pinned configuration: {key}"
                )
        if audit_suppressions:
            self.profile["name"] += "+suppression-audit"
            self.profile["checker_options"].append("-AwarnUnneededSuppressions")
        self.env = dict(os.environ)
        self.env["JAVA_HOME"] = self.profile["java_home"]
        self.env["PATH"] = self.profile["java_home"] + "/bin:" + self.env["PATH"]
        for variable in (
            "JDK_JAVAC_OPTIONS",
            "JAVA_TOOL_OPTIONS",
            "_JAVA_OPTIONS",
            "CLASSPATH",
        ):
            if self.env.get(variable):
                raise ValueError(
                    f"Unset {variable}: it would change the pinned profile"
                )
        for relative, expected in self.profile["artifacts"].items():
            if digest(HERE / relative) != expected:
                raise ValueError(f"Pinned artifact changed: {relative}")
        version = subprocess.run(
            [self.profile["java_home"] + "/bin/java", "-version"],
            capture_output=True,
            text=True,
            check=True,
        ).stderr.strip()
        if version != self.profile["java_version"]:
            raise ValueError("Compiler runtime differs from the pinned version")
        if git("ls-files", "--others", "--exclude-standard", "--", "src"):
            raise ValueError(
                "Untracked source dependencies must be recorded before running"
            )
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.root = OUTPUT / "runs" / f"{stamp}-{label}-{uuid.uuid4().hex[:8]}"
        self.root.mkdir(parents=True)
        (self.root / "runner.py").write_bytes(Path(__file__).read_bytes())
        (self.root / "manifest.json").write_bytes((HERE / "manifest.json").read_bytes())
        write_json(self.root / "profile.json", self.profile)
        source_diff = git("diff", "--binary", "HEAD", "--", "src")
        (self.root / "source.diff").write_text(source_diff + "\n")
        self.initial_head = git("rev-parse", "HEAD")
        self.initial_diff = source_diff
        write_json(
            self.root / "context.json",
            {
                "jdk_head": self.initial_head,
                "source_status": git("status", "--short", "--", "src"),
                "source_diff_sha256": digest(self.root / "source.diff"),
                "profile": self.profile,
                "profile_path": str(self.profile_path),
                "profile_sha256": digest(self.profile_path),
                "runner_sha256": digest(Path(__file__)),
                "manifest_sha256": digest(HERE / "manifest.json"),
                "java_version": version,
                "os": os.uname().sysname,
                "architecture": os.uname().machine,
            },
        )
        self.checked_roots = set()

    def execute(self, identifier, module, source, review, extra_root=None):
        """Check one source file, preserving inputs, invocation and complete output."""
        run = self.root / identifier
        run.mkdir()
        (run / "classes").mkdir()
        (run / "generated").mkdir()
        root = JDK / "src" / module / "share/classes"
        if root not in self.checked_roots:
            stale = next(root.rglob("*.class"), None)
            if stale:
                raise ValueError(f"Stale class file in patch root: {stale}")
            self.checked_roots.add(root)
        patch_roots = ([extra_root] if extra_root else []) + [root]
        original_hash = digest(source)
        (run / source.name).write_bytes(source.read_bytes())
        write_json(run / "scope-review.json", review)
        source_arg = json.dumps(str(source))
        (run / "sources.args").write_text(source_arg + "\n")
        command = [
            str(self.toolchain / "checker/bin/javac"),
            *self.profile["checker_options"],
            "--patch-module",
            module + "=" + os.pathsep.join(map(str, patch_roots)),
            "--add-reads",
            module + "=ALL-UNNAMED",
            "-classpath",
            str(self.toolchain / "checker/dist/checker-qual.jar"),
            "-d",
            str(run / "classes"),
            "-s",
            str(run / "generated"),
            "@" + str(run / "sources.args"),
        ]
        start = time.monotonic()
        timed_out = False
        with (run / "compile.log").open("w") as output:
            process = subprocess.Popen(
                command,
                cwd=JDK,
                env=self.env,
                stdout=output,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                exit_code = process.wait(timeout=self.profile["timeout_seconds"])
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGKILL)
                exit_code = process.wait()
        log = (run / "compile.log").read_text(errors="replace")
        result = classify(log, exit_code, timed_out, source, original_hash, review)
        if (
            digest(source) != original_hash
            or git("rev-parse", "HEAD") != self.initial_head
            or git("diff", "--binary", "HEAD", "--", "src") != self.initial_diff
        ):
            result["status"] = "inputs-changed-during-run"
        result.update(
            {
                "id": identifier,
                "module": module,
                "source": str(source),
                "source_sha256": original_hash,
                "argv": command,
                "cwd": str(JDK),
                "patch_roots": list(map(str, patch_roots)),
                "environment": {
                    "JAVA_HOME": self.env["JAVA_HOME"],
                    "PATH": self.env["PATH"],
                },
                "exit_code": exit_code,
                "timed_out": timed_out,
                "duration_seconds": round(time.monotonic() - start, 3),
                "log_sha256": digest(run / "compile.log"),
                "sources_args_sha256": digest(run / "sources.args"),
            }
        )
        write_json(run / "result.json", result)
        print(f"{identifier}: {result['status']} (exit {exit_code})", flush=True)
        return result


def preflight(study, modules):
    """Exercise checking, opt-in, and JSpecify location policy in each module."""
    results = []
    fixture_base = study.root / "probe-inputs"
    declaration = '@org.checkerframework.framework.qual.AnnotatedFor("nullness")\n'
    fixtures = {
        "good": (
            declaration
            + "class StudyProbe { Object field; Object get() { return new Object(); } }",
            0,
            None,
        ),
        "bad": (
            declaration + "class StudyProbe { Object get() { return null; } }",
            1,
            "return.type.incompatible",
        ),
        "unmarked": (
            "class StudyProbe { Object get() { return null; } }",
            0,
            None,
        ),
        "location": (
            declaration
            + "class StudyProbe { void get() { @org.checkerframework.checker.nullness.qual.Nullable Object x = null; } }",
            1,
            "jspecify.unrecognized.location.local",
        ),
    }
    if study.profile.get("purity") == "assumed-pure":
        fixtures["purity"] = (
            declaration
            + "class StudyProbe { @org.checkerframework.checker.nullness.qual.Nullable Object field; "
            + "void effect() {} void get() { if (field != null) { effect(); field.toString(); } } }",
            0,
            None,
        )
    if study.profile.get("assertions") == "enabled":
        fixtures["assertions"] = (
            declaration
            + "class StudyProbe { void get(@org.checkerframework.checker.nullness.qual.Nullable Object value) "
            + "{ assert value != null; value.toString(); } }",
            0,
            None,
        )
    for module in modules:
        for name, (body, expected_exit, key) in fixtures.items():
            patch = fixture_base / module / name
            source = patch / "study/nullness/StudyProbe.java"
            source.parent.mkdir(parents=True)
            source.write_text("package study.nullness;\n" + body + "\n")
            review = {
                "source_sha256": digest(source),
                "all_declarations_reviewed": True,
                "top_level_declarations": ["study.nullness.StudyProbe"],
                "opted_in": name != "unmarked",
                "suppression_keys": [],
                "basis": "Generated controlled fixture, with exactly one top-level class.",
            }
            result = study.execute(module + "-" + name, module, source, review, patch)
            expected_status = (
                "checked-with-diagnostics"
                if key
                else "not-opted-in"
                if name == "unmarked"
                else "clean-without-suppressions"
            )
            result["preflight_passed"] = (
                result["exit_code"] == expected_exit
                and result["status"] == expected_status
                and (not key or result["diagnostics_by_key"] == {key: 1})
            )
            results.append(result)
    return results


def validate_manifest(manifest):
    """Require the complete declared package to remain explicitly enrolled."""
    selected = manifest["verified_files"]
    entries = {entry["id"]: entry for entry in manifest["candidates"]}
    if not selected or len(set(selected)) != len(selected):
        raise ValueError("Verified targets must be nonempty and unique")
    if set(selected) != set(entries):
        raise ValueError("The package manifest must account for every candidate")
    package = (
        JDK
        / "src"
        / manifest["module"]
        / "share/classes"
        / manifest["package"].replace(".", "/")
    )
    actual = {
        str(p.relative_to(JDK))
        for p in package.glob("*.java")
        if p.name != "package-info.java"
    }
    declared = {entry["path"] for entry in entries.values()}
    if actual != declared:
        raise ValueError(
            f"Package coverage changed: unlisted={sorted(actual - declared)}, missing={sorted(declared - actual)}"
        )
    if any(entry["module"] != manifest["module"] for entry in entries.values()):
        raise ValueError("Manifest module does not match its package")


def main():
    """Parse a study command and return a nonzero status for incomplete checks."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "preflight"])
    parser.add_argument("--label", default="run")
    parser.add_argument("--ids", nargs="+")
    parser.add_argument("--modules", nargs="+")
    parser.add_argument("--audit-suppressions", action="store_true")
    parser.add_argument(
        "--profile", help="Profile JSON path; defaults to the active profile"
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.label):
        parser.error("label must be alphanumeric, hyphens or underscores")
    study = Study(
        args.label,
        audit_suppressions=args.audit_suppressions,
        profile_path=args.profile,
    )
    print("Evidence: " + str(study.root), flush=True)
    if args.command == "preflight":
        results = preflight(study, args.modules or ["java.xml"])
        passed = all(result["preflight_passed"] for result in results)
    else:
        manifest = json.loads((HERE / "manifest.json").read_text())
        validate_manifest(manifest)
        selected = args.ids if args.ids is not None else manifest["verified_files"]
        if not selected:
            parser.error("No verified targets selected")
        entries = {entry["id"]: entry for entry in manifest["candidates"]}
        unknown = set(selected) - entries.keys()
        if unknown:
            parser.error(f"Unknown target IDs: {sorted(unknown)}")
        reviews = json.loads((HERE / "reviews.json").read_text())
        results = [
            study.execute(
                identifier,
                entries[identifier]["module"],
                JDK / entries[identifier]["path"],
                reviews.get(identifier),
            )
            for identifier in selected
        ]
        passed = all(result["status"] in CLEAN for result in results)
    write_json(
        study.root / "summary.json",
        {
            "passed": passed,
            "command": args.command,
            "counts": dict(Counter(result["status"] for result in results)),
            "results": results,
        },
    )
    print("Summary: " + str(study.root / "summary.json"), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Study setup failed: {error}", file=sys.stderr)
        sys.exit(2)

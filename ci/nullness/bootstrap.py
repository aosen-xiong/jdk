"""Build a pinned Checker Framework distribution and record a portable profile."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def revision(root, expected):
    actual = subprocess.check_output(
        ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
    ).strip()
    if actual != expected:
        raise ValueError(f"Expected {expected} at {root}, found {actual}")
    if subprocess.check_output(
        ["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"],
        text=True,
    ).strip():
        raise ValueError(f"Pinned source has tracked modifications: {root}")


def java_version(home, expected):
    process = subprocess.run(
        [str(home / "bin/java"), "-version"], capture_output=True, text=True, check=True
    )
    version = (process.stderr + process.stdout).strip()
    if expected not in version:
        raise ValueError(f"Expected Java {expected} at {home}: {version}")
    return version


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker-root", type=Path, required=True)
    parser.add_argument("--bundled-jdk-root", type=Path, required=True)
    parser.add_argument("--build-java-home", type=Path, required=True)
    parser.add_argument("--check-java-home", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=ROOT / ".nullness-ci")
    parser.add_argument(
        "--local-runtime",
        action="store_true",
        help="Record a separate local profile with the same Java feature/update releases, instead of the exact Temurin CI builds",
    )
    args = parser.parse_args()
    config = json.loads((HERE / "config.json").read_text())
    checker = args.checker_root.resolve()
    bundled = args.bundled_jdk_root.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    profile_path = output / "profile.json"
    if profile_path.exists():
        raise ValueError(
            "Use a fresh output directory; an existing runtime profile is immutable"
        )
    revision(checker, config["checker_source_commit"])
    revision(bundled, config["bundled_jdk_source_commit"])
    build_home = args.build_java_home.resolve()
    check_home = args.check_java_home.resolve()
    build_version = java_version(
        build_home, "21.0.7" if args.local_runtime else config["build_java_version"]
    )
    check_version = java_version(
        check_home, "17.0.14" if args.local_runtime else config["check_java_version"]
    )
    env = dict(os.environ)
    for variable in (
        "JDK_JAVAC_OPTIONS",
        "JAVA_TOOL_OPTIONS",
        "_JAVA_OPTIONS",
        "CLASSPATH",
    ):
        if env.get(variable):
            raise ValueError(f"Unset {variable}: it changes the pinned experiment")
    env["JAVA_HOME"] = str(build_home)
    env["PATH"] = str(build_home / "bin") + os.pathsep + env["PATH"]
    command = [
        str(checker / "gradlew"),
        ":checker:assembleForJavac",
        "--no-daemon",
        "--max-workers=2",
        "-x",
        ":framework:cloneAnnotatedJdk",
        "-PannotatedJdkHome=" + str(bundled),
        "--console=plain",
    ]
    provenance = {
        "config": config,
        "config_sha256": digest(HERE / "config.json"),
        "checker_root": str(checker),
        "bundled_jdk_root": str(bundled),
        "build_java_home": str(build_home),
        "build_java_version": build_version,
        "check_java_home": str(check_home),
        "check_java_version": check_version,
        "local_runtime": args.local_runtime,
        "build_argv": command,
        "bootstrap_sha256": digest(Path(__file__)),
        "os": os.uname().sysname,
        "architecture": os.uname().machine,
    }
    (output / "build-context.json").write_text(json.dumps(provenance, indent=2) + "\n")
    print(f"Building pinned checker; log: {output / 'build.log'}", flush=True)
    with (output / "build.log").open("w") as log:
        result = subprocess.run(
            command,
            cwd=checker,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=1200,
        )
    provenance["build_exit_code"] = result.returncode
    provenance["build_log_sha256"] = digest(output / "build.log")
    (output / "build-context.json").write_text(json.dumps(provenance, indent=2) + "\n")
    if result.returncode:
        raise ValueError(f"Checker build failed; see {output / 'build.log'}")
    revision(checker, config["checker_source_commit"])
    revision(bundled, config["bundled_jdk_source_commit"])
    with zipfile.ZipFile(checker / "checker/dist/checker.jar") as jar:
        properties = jar.read("git.properties").decode()
        if config["checker_source_commit"] not in properties:
            raise ValueError("Built checker.jar has unexpected Git provenance")
    artifacts = [
        checker / "checker/bin/javac",
        *sorted((checker / "checker/dist").glob("*.jar")),
    ]
    profile = dict(config)
    profile.update(
        name=config["name"] + ("-local-runtime" if args.local_runtime else ""),
        java_home=str(check_home),
        java_version=check_version,
        toolchain_root=str(checker),
        artifacts={str(p): digest(p) for p in artifacts},
        build_context_sha256=digest(output / "build-context.json"),
    )
    profile_path.write_text(json.dumps(profile, indent=2) + "\n")
    print(f"Runtime profile: {profile_path}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"Bootstrap failed: {error}", file=sys.stderr)
        sys.exit(2)

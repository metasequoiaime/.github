#!/usr/bin/env python3
"""Run portable platform regressions against a specified Engine commit.

Read committed Git objects only. Never switch a checkout, rewrite a product lock,
fetch dependencies, or install an input method. Requires initialized Engine
submodules, CMake, and the default Engine development dependencies.
"""

import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


CONSUMERS = {
    "MSIME-Apple": [
        "shared/apple-bridge",
        "platforms/ios/tests/InputSessionAdapterTests.cpp",
    ],
    "MSIME-Linux": [
        "src/InputController.cpp", "src/InputController.h",
        "src/TextTransform.cpp", "src/TextTransform.h",
        "tests/InputControllerTests.cpp",
    ],
}

CMAKE = """cmake_minimum_required(VERSION 3.25)
project(PlatformAdoption LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(METASEQUOIA_IME_BUILD_VOICE OFF CACHE BOOL "" FORCE)
add_subdirectory(engine)
enable_testing()
add_executable(apple_bridge
  MSIME-Apple/shared/apple-bridge/InputSessionAdapter.cpp
  MSIME-Apple/shared/apple-bridge/ShuangpinKeymap.cpp
  MSIME-Apple/platforms/ios/tests/InputSessionAdapterTests.cpp)
target_include_directories(apple_bridge PRIVATE MSIME-Apple/shared/apple-bridge)
target_link_libraries(apple_bridge PRIVATE MetasequoiaIme::Engine)
add_test(NAME apple_bridge COMMAND apple_bridge)
add_executable(linux_controller
  MSIME-Linux/src/InputController.cpp MSIME-Linux/src/TextTransform.cpp
  MSIME-Linux/tests/InputControllerTests.cpp)
target_include_directories(linux_controller PRIVATE MSIME-Linux/src)
target_link_libraries(linux_controller PRIVATE MetasequoiaIme::Engine)
add_test(NAME linux_controller COMMAND linux_controller)
"""


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def resolve(repo, ref):
    return git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}").decode().strip()


def snapshot(repo, commit, destination, paths):
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(git(repo, "archive", commit, *paths))) as archive:
        archive.extractall(destination, filter="data")


def run(command, output, name):
    log = output / f"{name}.log"
    print(f"{name}: {log}", flush=True)
    with log.open("w") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        print("\n".join(log.read_text(errors="replace").splitlines()[-60:]))
        raise subprocess.CalledProcessError(result.returncode, command)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True,
                        help="Parent of the Engine, Apple and Linux repositories")
    parser.add_argument("--engine-ref", required=True,
                        help="Engine commit/ref to test; never changes platform pins")
    parser.add_argument("--platform-ref", default="origin/develop",
                        help="Committed ref to read in both platform repositories")
    parser.add_argument("--prefix-path", help="Optional CMake dependency prefix")
    parser.add_argument("--parallel", type=int, default=4)
    args = parser.parse_args()
    if args.parallel < 1:
        parser.error("--parallel must be positive")

    workspace = args.workspace.resolve()
    engine = workspace / "MSIME-Engine"
    commit = resolve(engine, args.engine_ref)
    output = Path(tempfile.mkdtemp(prefix="msime-adoption-"))
    print(f"Evidence directory: {output}", flush=True)
    evidence = {"engine": commit, "submodules": {}, "consumers": {}, "status": "preparing"}
    evidence_file = output / "evidence.json"
    try:
        # The default C++ engine excludes the data build pipeline and optional Voice.
        excluded = {".github", "dictionary", "helpcode", "voice", "googlepinyinime-rev", "utfcpp"}
        paths = git(engine, "ls-tree", "--name-only", commit).decode().splitlines()
        snapshot(engine, commit, output / "engine", [p for p in paths if p not in excluded])
        for name in ("googlepinyinime-rev", "utfcpp"):
            entry = git(engine, "ls-tree", commit, name).decode().split()
            if len(entry) < 3 or entry[:2] != ["160000", "commit"]:
                raise ValueError(f"Expected Engine submodule: {name}")
            evidence["submodules"][name] = entry[2]
            snapshot(engine / name, entry[2], output / "engine" / name, [])
        for name, paths in CONSUMERS.items():
            repo = workspace / name
            platform_commit = resolve(repo, args.platform_ref)
            evidence["consumers"][name] = platform_commit
            destination = output / name
            snapshot(repo, platform_commit, destination, paths)
            # Preserve relative includes in the original, unmodified test sources.
            (destination / "vendor").mkdir()
            (destination / "vendor" / "MetasequoiaImeEngine").symlink_to(
                output / "engine", target_is_directory=True)
        (output / "CMakeLists.txt").write_text(CMAKE)
        command = ["cmake", "-S", str(output), "-B", str(output / "build"),
                   "-DCMAKE_BUILD_TYPE=Release"]
        if args.prefix_path:
            command.append(f"-DCMAKE_PREFIX_PATH={args.prefix_path}")
        evidence["configure"] = command
        run(command, output, "configure")
        run(["cmake", "--build", str(output / "build"), "--config", "Release",
             "--parallel", str(args.parallel)], output, "build")
        run(["ctest", "--test-dir", str(output / "build"), "-C", "Release",
             "--output-on-failure", "--no-tests=error", "--timeout", "30"], output, "test")
        evidence["status"] = "passed"
        print((output / "test.log").read_text())
    except (subprocess.CalledProcessError, OSError, ValueError, tarfile.TarError) as error:
        evidence["status"] = "failed"
        evidence["error"] = str(error)
        print(f"Probe failed: {error}")
        return 1
    finally:
        evidence_file.write_text(json.dumps(evidence, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

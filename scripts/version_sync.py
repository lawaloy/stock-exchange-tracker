#!/usr/bin/env python3
"""
Single source of truth: setup.cfg [metadata] version.

  python scripts/version_sync.py check   # exit 1 if dashboard files disagree
  python scripts/version_sync.py sync    # rewrite them from setup.cfg
"""
from __future__ import annotations

import argparse
import configparser
import json
import re
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_setup_version(root: Path) -> str:
    cfg_path = root / "setup.cfg"
    if not cfg_path.is_file():
        raise FileNotFoundError(f"Missing {cfg_path}")
    cfg = configparser.ConfigParser()
    cfg.read(cfg_path, encoding="utf-8")
    if "metadata" not in cfg or "version" not in cfg["metadata"]:
        raise ValueError("setup.cfg missing [metadata] version")
    v = cfg["metadata"]["version"].strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", v):
        raise ValueError(f"Invalid semver in setup.cfg: {v!r}")
    return v


def read_package_json_version(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return str(data.get("version", "")).strip()


def read_lock_root_versions(path: Path) -> tuple[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    top = str(data.get("version", "")).strip()
    inner = ""
    packages = data.get("packages") or {}
    if "" in packages and isinstance(packages[""], dict):
        inner = str(packages[""].get("version", "")).strip()
    return top, inner


def read_main_py_versions(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    fastapi = re.search(
        r'title="MarketHelm API",\s*\n\s*description="[^"]+",\s*\n\s*version="(\d+\.\d+\.\d+)"',
        text,
    )
    root_json = re.search(
        r'"service": "MarketHelm API",\s*\n\s*"version": "(\d+\.\d+\.\d+)"',
        text,
    )
    if not fastapi or not root_json:
        raise ValueError(
            f"Could not find version markers in {path}. "
            "Expected FastAPI(...) MarketHelm API block and root() JSON version."
        )
    return fastapi.group(1), root_json.group(1)


def check(root: Path) -> list[str]:
    want = read_setup_version(root)
    errors: list[str] = []

    pj = root / "dashboard" / "frontend" / "package.json"
    got = read_package_json_version(pj)
    if got != want:
        errors.append(f"{pj.relative_to(root)}: version is {got!r}, setup.cfg has {want!r}")

    lock = root / "dashboard" / "frontend" / "package-lock.json"
    top, inner = read_lock_root_versions(lock)
    if top != want:
        errors.append(f"{lock.relative_to(root)} root version: {top!r} != {want!r}")
    if inner != want:
        errors.append(f'{lock.relative_to(root)} packages[""] version: {inner!r} != {want!r}')

    main_py = root / "dashboard" / "backend" / "main.py"
    fa, rj = read_main_py_versions(main_py)
    if fa != want:
        errors.append(f"{main_py.relative_to(root)} FastAPI version: {fa!r} != {want!r}")
    if rj != want:
        errors.append(f"{main_py.relative_to(root)} root JSON version: {rj!r} != {want!r}")

    return errors


def sync_package_json(path: Path, version: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def sync_package_lock(path: Path, version: str) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = version
    if "packages" in data and "" in data["packages"] and isinstance(data["packages"][""], dict):
        data["packages"][""]["version"] = version
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")


def sync_main_py(path: Path, version: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, n1 = re.subn(
        r'(title="MarketHelm API",\s*\n\s*description="[^"]+",\s*\n\s*version=")(\d+\.\d+\.\d+)(")',
        rf"\g<1>{version}\3",
        text,
        count=1,
    )
    if n1 != 1:
        raise ValueError(f"Expected 1 FastAPI version replace in {path}, got {n1}")
    new_text, n2 = re.subn(
        r'("service": "MarketHelm API",\s*\n\s*"version": ")(\d+\.\d+\.\d+)(")',
        rf"\g<1>{version}\3",
        new_text,
        count=1,
    )
    if n2 != 1:
        raise ValueError(f"Expected 1 root JSON version replace in {path}, got {n2}")
    path.write_text(new_text, encoding="utf-8", newline="\n")


def cmd_check(root: Path) -> int:
    errors = check(root)
    if errors:
        print("Version mismatch (canonical: setup.cfg [metadata] version):\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nRun: python scripts/version_sync.py sync", file=sys.stderr)
        return 1
    print(f"OK: all tracked files match setup.cfg version {read_setup_version(root)!r}")
    return 0


def cmd_sync(root: Path) -> int:
    version = read_setup_version(root)
    sync_package_json(root / "dashboard" / "frontend" / "package.json", version)
    sync_package_lock(root / "dashboard" / "frontend" / "package-lock.json", version)
    sync_main_py(root / "dashboard" / "backend" / "main.py", version)
    print(f"Synced dashboard files to {version!r} from setup.cfg")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="Verify dashboard versions match setup.cfg")
    sub.add_parser("sync", help="Write setup.cfg version into dashboard files")
    args = parser.parse_args()
    root = repo_root()
    if args.cmd == "check":
        return cmd_check(root)
    if args.cmd == "sync":
        return cmd_sync(root)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

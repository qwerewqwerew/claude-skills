"""Copy selected skills from a central checkout. Python 3.10+, standard library."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
import uuid

REPO = Path(__file__).resolve().parents[1]
IGNORED = {"__pycache__", "node_modules", ".git", ".DS_Store"}
MARKER = ".central-skill.json"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def linked(path):
    if path.is_symlink():
        return True
    if os.name == "nt" and path.exists():
        return bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    return False


def snapshot(root):
    """Hash content and relative names; refuse links to external files."""
    result = {}
    for base, dirs, files in os.walk(root, followlinks=False):
        base = Path(base)
        for name in dirs + files:
            if linked(base / name):
                raise ValueError(f"Link/junction is not supported: {base / name}")
        dirs[:] = sorted(d for d in dirs if d not in IGNORED)
        for name in sorted(files):
            if name in IGNORED or name == MARKER or name.endswith((".pyc", ".pyo")):
                continue
            path = base / name
            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def plan(profile, target, allow_candidates=False):
    catalog = read(REPO / "catalog.json")["skills"]
    names = read(profile)["skills"]
    if not isinstance(names, list) or not names:
        raise ValueError("Profile must contain a nonempty skills list")
    if any(not isinstance(n, str) or not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", n) for n in names):
        raise ValueError("Invalid skill name")
    if len(set(names)) != len(names):
        raise ValueError("Duplicate skill names")
    if target == REPO or target in REPO.parents or REPO in target.parents:
        raise ValueError("Installation target must be outside the repository")
    rows = []
    for name in names:
        entry = catalog[name]
        if entry["status"] != "selected" and not allow_candidates:
            raise ValueError(f"Candidate requires --allow-candidates: {name}")
        source = (REPO / entry["path"]).resolve()
        if REPO not in source.parents or not (source / "SKILL.md").is_file():
            raise ValueError(f"Invalid skill source: {name}")
        expected = snapshot(source)
        destination = target / name
        action = "install"
        previous = None
        if linked(destination):
            raise ValueError(f"Existing link/junction: {destination}")
        if destination.exists():
            if not destination.is_dir() or not (destination / MARKER).is_file():
                raise ValueError(f"Unmanaged installation; compare and move manually first: {destination}")
            marker = read(destination / MARKER)
            if marker.get("repository") != "qwerewqwerew/claude-skills" or marker.get("skill") != name:
                raise ValueError(f"Foreign installation: {destination}")
            previous = snapshot(destination)
            if previous != marker["files"]:
                raise ValueError(f"Local edits detected; preserve and review: {destination}")
            action = "unchanged" if previous == expected else "update"
        rows.append((name, source, destination, expected, previous, action))
    return rows


def apply(rows, target):
    """Stage and verify everything before replacing any managed installation."""
    target.parent.mkdir(parents=True, exist_ok=True)
    backup = target.parent / ("skill-central-backup-" + uuid.uuid4().hex)
    changed = []
    with tempfile.TemporaryDirectory(prefix="skill-central-stage-", dir=target.parent) as temp:
        stage = Path(temp)
        for name, source, destination, expected, previous, action in rows:
            if action == "unchanged":
                continue
            prepared = stage / name
            prepared.mkdir()
            for relative in expected:
                out = prepared / relative
                out.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / relative, out)
            if snapshot(prepared) != expected:
                raise ValueError(f"Source changed while copying: {name}")
            (prepared / MARKER).write_text(json.dumps({
                "repository": "qwerewqwerew/claude-skills", "skill": name,
                "files": expected
            }, indent=2) + "\n", encoding="utf-8")
        target.mkdir(parents=True, exist_ok=True)
        try:
            for name, source, destination, expected, previous, action in rows:
                if action == "unchanged":
                    continue
                if linked(destination) or (previous is None and destination.exists()):
                    raise ValueError(f"Destination changed: {name}")
                if previous is not None and snapshot(destination) != previous:
                    raise ValueError(f"Destination changed: {name}")
                saved = None
                if previous is not None:
                    backup.mkdir(exist_ok=True)
                    saved = backup / name
                    destination.rename(saved)
                changed.append((destination, saved))
                (stage / name).rename(destination)
                if snapshot(destination) != expected:
                    raise ValueError(f"Copy verification failed: {name}")
        except BaseException:
            for destination, saved in reversed(changed):
                if destination.exists():
                    destination.rename(stage / ("failed-" + uuid.uuid4().hex))
                if saved is not None:
                    saved.rename(destination)
            raise
    if backup.exists():
        print(f"Previous copies retained: {backup}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--target", type=Path, required=True,
                        help="Explicit skill directory for this device/application")
    parser.add_argument("--apply", action="store_true", help="Default: preview only")
    parser.add_argument("--allow-candidates", action="store_true")
    args = parser.parse_args()
    target = args.target.expanduser().resolve()
    rows = plan(args.profile, target, args.allow_candidates)
    for name, source, destination, expected, previous, action in rows:
        print(f"{action}: {name} -> {destination}")
    if args.apply:
        apply(rows, target)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, TypeError) as error:
        raise SystemExit(f"Stopped: {error}")

#!/usr/bin/env python3
"""
Sync shared scripts between execution/ (golden copies) and workspace skill roots.

Reads metadata.shared_scripts from each skill's SKILL.md frontmatter and syncs files
between execution/ and the selected skill root's scripts/ directory. Uses SHA-256
checksums to skip identical files.

Usage:
    ~/Documents/Workspace/.venv/bin/python execution/_sync_to_skills.py --forward
    ~/Documents/Workspace/.venv/bin/python execution/_sync_to_skills.py --forward --root claude
    ~/Documents/Workspace/.venv/bin/python execution/_sync_to_skills.py --reverse --root agents
    ~/Documents/Workspace/.venv/bin/python execution/_sync_to_skills.py --forward --dry-run
    ~/Documents/Workspace/.venv/bin/python execution/_sync_to_skills.py --forward --skill classify-emails

Reference: tools/claude_code.md (if exists)
"""
import argparse
import hashlib
import os
import re
import shutil
import sys
from pathlib import Path


SKILL_ROOTS = {
    "agents": Path(".agents") / "skills",
    "claude": Path(".claude") / "skills",
}


def selected_skill_roots(workspace_root, root_filter="both"):
    """Return configured workspace skill roots that exist."""
    labels = list(SKILL_ROOTS) if root_filter == "both" else [root_filter]
    roots = []
    for label in labels:
        skills_root = workspace_root / SKILL_ROOTS[label]
        if skills_root.exists():
            roots.append((label, skills_root))
    return roots


def parse_frontmatter(skill_md_path):
    """Extract metadata from SKILL.md YAML frontmatter using regex."""
    with open(skill_md_path, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return {}

    fm_text = match.group(1)
    result = {"metadata": {}}

    for key in ["name", "description", "disable-model-invocation", "allowed-tools", "argument-hint"]:
        pattern = rf"^{re.escape(key)}:\s*(.+)$"
        m = re.search(pattern, fm_text, re.MULTILINE)
        if m:
            result[key] = m.group(1).strip().strip("\"'")

    meta_match = re.search(r"^metadata:\s*\n((?:\s{2,}\S.*\n?)*)", fm_text, re.MULTILINE)
    if meta_match:
        meta_block = meta_match.group(1)
        for line in meta_block.split("\n"):
            line = line.strip()
            if not line:
                continue
            kv = re.match(r"(\w[\w_]*):\s*(.*)", line)
            if kv:
                key = kv.group(1)
                val = kv.group(2).strip()
                if val.startswith("[") and val.endswith("]"):
                    items = val[1:-1].split(",")
                    result["metadata"][key] = [
                        i.strip().strip("\"'") for i in items if i.strip()
                    ]
                else:
                    result["metadata"][key] = val.strip("\"'")

    return result


def file_checksum(filepath):
    """Compute SHA-256 checksum."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def dir_checksum(dirpath):
    """Compute combined checksum for a directory (sorted file list)."""
    h = hashlib.sha256()
    for root, dirs, files in sorted(os.walk(dirpath)):
        dirs.sort()
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, dirpath)
            h.update(rel.encode())
            h.update(file_checksum(fpath).encode())
    return h.hexdigest()


def discover_skills(skills_root, root_label, skill_filter=None):
    """Find all skills with SKILL.md and parse their frontmatter."""
    skills = []
    if not skills_root.exists():
        return skills

    for entry in sorted(skills_root.iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        if skill_filter and entry.name != skill_filter:
            continue

        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md)
        shared = fm.get("metadata", {}).get("shared_scripts", [])
        if isinstance(shared, str):
            shared = [shared] if shared else []

        skills.append({
            "root": root_label,
            "name": entry.name,
            "path": entry,
            "skill_md": skill_md,
            "shared_scripts": shared,
            "frontmatter": fm,
        })

    return skills


def discover_selected_skills(workspace_root, root_filter="both", skill_filter=None):
    """Discover skills across the selected runtime roots."""
    skills = []
    for root_label, skills_root in selected_skill_roots(workspace_root, root_filter):
        skills.extend(discover_skills(skills_root, root_label, skill_filter))
    return skills


def sync_forward(workspace_root, dry_run=False, skill_filter=None, root_filter="both"):
    """Copy shared scripts from execution/ -> selected skill roots."""
    execution_dir = workspace_root / "execution"

    skills = discover_selected_skills(workspace_root, root_filter, skill_filter)
    if not skills:
        print("No skills found to sync.")
        return {"synced": 0, "skipped": 0, "errors": []}

    synced = 0
    skipped = 0
    errors = []

    for info in sorted(skills, key=lambda i: (i["root"], i["name"])):
        root_label = info["root"]
        skill_name = info["name"]
        shared = info["shared_scripts"]
        if not shared:
            continue

        scripts_dir = info["path"] / "scripts"
        display_name = f"{root_label}/{skill_name}"

        for script_ref in shared:
            src = execution_dir / script_ref
            dst = scripts_dir / Path(script_ref).name

            if "/" in script_ref and (execution_dir / script_ref.split("/")[0]).is_dir():
                module_name = script_ref.split("/")[0]
                src_dir = execution_dir / module_name
                dst_dir = scripts_dir / module_name

                if not src_dir.exists():
                    errors.append(f"  [{display_name}] Missing module: {module_name}/")
                    continue

                if dst_dir.exists() and dir_checksum(src_dir) == dir_checksum(dst_dir):
                    skipped += 1
                    continue

                if dry_run:
                    print(f"  [DRY] {display_name}: would copy {module_name}/ -> scripts/{module_name}/")
                    synced += 1
                else:
                    scripts_dir.mkdir(parents=True, exist_ok=True)
                    if dst_dir.exists():
                        shutil.rmtree(dst_dir)
                    shutil.copytree(src_dir, dst_dir)
                    print(f"  [SYNC] {display_name}: {module_name}/ -> scripts/{module_name}/")
                    synced += 1
                continue

            if not src.exists():
                errors.append(f"  [{display_name}] Missing script: {script_ref}")
                continue

            if dst.exists() and file_checksum(src) == file_checksum(dst):
                skipped += 1
                continue

            if dry_run:
                action = "overwrite" if dst.exists() else "copy"
                print(f"  [DRY] {display_name}: would {action} {script_ref} -> scripts/{dst.name}")
                synced += 1
            else:
                scripts_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"  [SYNC] {display_name}: {script_ref} -> scripts/{dst.name}")
                synced += 1

    return {"synced": synced, "skipped": skipped, "errors": errors}


def sync_reverse(workspace_root, dry_run=False, skill_filter=None, root_filter="claude"):
    """Copy scripts from one selected skill root -> execution/."""
    execution_dir = workspace_root / "execution"

    skills = discover_selected_skills(workspace_root, root_filter, skill_filter)
    if not skills:
        print("No skills found to sync.")
        return {"synced": 0, "skipped": 0, "errors": []}

    synced = 0
    skipped = 0
    errors = []

    for info in sorted(skills, key=lambda i: (i["root"], i["name"])):
        root_label = info["root"]
        skill_name = info["name"]
        shared = info["shared_scripts"]
        if not shared:
            continue

        scripts_dir = info["path"] / "scripts"
        display_name = f"{root_label}/{skill_name}"

        for script_ref in shared:
            dst = execution_dir / script_ref

            if "/" in script_ref and (execution_dir / script_ref.split("/")[0]).is_dir():
                module_name = script_ref.split("/")[0]
                src = scripts_dir / module_name
                dst = execution_dir / module_name

                if not src.exists():
                    continue
                if not dst.exists():
                    errors.append(f"  [{display_name}] Golden module missing: execution/{module_name}/")
                    continue
                if dir_checksum(src) == dir_checksum(dst):
                    skipped += 1
                    continue

                if dry_run:
                    print(f"  [DRY] {display_name}: would update execution/{module_name}/ from scripts/{module_name}/")
                    synced += 1
                else:
                    shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"  [SYNC] {display_name}: scripts/{module_name}/ -> execution/{module_name}/")
                    synced += 1
                continue

            src = scripts_dir / Path(script_ref).name

            if not src.exists():
                continue

            if not dst.exists():
                errors.append(f"  [{display_name}] Golden copy missing: execution/{script_ref}")
                continue

            if file_checksum(src) == file_checksum(dst):
                skipped += 1
                continue

            if dry_run:
                print(f"  [DRY] {display_name}: would update execution/{script_ref} from scripts/{src.name}")
                synced += 1
            else:
                shutil.copy2(src, dst)
                print(f"  [SYNC] {display_name}: scripts/{src.name} -> execution/{script_ref}")
                synced += 1

    return {"synced": synced, "skipped": skipped, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Sync shared scripts between execution/ and skills")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--forward", action="store_true", help="execution/ -> skills")
    group.add_argument("--reverse", action="store_true", help="skills -> execution/")
    parser.add_argument("--root", choices=["both", "agents", "claude"], default="both",
                        help="Skill root to sync. Forward default: both. Reverse requires agents or claude.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--skill", type=str, help="Sync only a specific skill")
    args = parser.parse_args()

    if args.reverse and args.root == "both":
        parser.error("--reverse requires --root agents or --root claude to choose the source skill root")

    workspace_root = Path(__file__).parent.parent

    direction = "execution/ -> skills" if args.forward else f"{args.root} skills -> execution/"
    print(f"{'[DRY RUN] ' if args.dry_run else ''}Syncing {direction}...")
    print(f"  Root: {args.root}")
    if args.skill:
        print(f"  Filtering: {args.skill}")
    print()

    if args.forward:
        result = sync_forward(workspace_root, args.dry_run, args.skill, args.root)
    else:
        result = sync_reverse(workspace_root, args.dry_run, args.skill, args.root)

    print()
    print(f"Done: {result['synced']} synced, {result['skipped']} unchanged")
    if result["errors"]:
        print(f"\nWarnings ({len(result['errors'])}):")
        for err in result["errors"]:
            print(err)
        sys.exit(1)


if __name__ == "__main__":
    main()

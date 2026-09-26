#!/usr/bin/env python
"""Cold-copy format_lab to Drive as one tar per top-level folder, md5-verified, resumable.

Why tarballs (2026-09-20): the lab is 13 GB in 59,726 files; a per-file Drive upload spent ten
minutes on 0.2 GB of tiny bench logs. One archive per folder is a dozen API calls instead of
sixty thousand. Destination: Shorts / Testing & Experiments / "Format Lab Source (2026-08 lab,
archived 2026-09-20)". Re-run to resume; a folder whose archive is already verified is skipped.
Local deletion of format_lab is a separate, explicit step after every archive reads back.

  ~/Documents/Workspace/.venv/bin/python workflow_versions/one-offs/2026-09-20-format_lab_cold_copy.py [--staging DIR]
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
F = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(F / "pipeline/deliver"))
import push_run_to_drive as d
from googleapiclient.http import MediaFileUpload
PARENT = "1iWa8eggC7iY1yTPreaMVGnJgMBgA2Lvc"   # Shorts / Testing & Experiments
NAME = "Format Lab Source (2026-08 lab, archived 2026-09-20)"

def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--staging", default=str(F / ".format_lab_archive_staging")); a = ap.parse_args()
    staging = Path(a.staging); staging.mkdir(parents=True, exist_ok=True)
    receipt = staging / "receipt.json"; done = json.loads(receipt.read_text()) if receipt.exists() else {}
    lab = F / "format_lab"
    s = d.svc(); folder, _ = d.find_or_create(s, NAME, PARENT)
    entries = sorted(p for p in lab.iterdir() if not p.name.startswith("."))
    for p in entries:
        tar = staging / (p.name + ".tar")
        if done.get(tar.name, {}).get("verified"): print("skip (verified)", tar.name); continue
        if not tar.exists():
            subprocess.run(["tar", "-cf", str(tar), "-C", str(lab), "--exclude", "__pycache__", "--exclude", "*/venv/*", p.name], check=True)
        m = md5(tar)
        fid, _ = d.find_or_create(s, tar.name, folder, folder=False)
        media = MediaFileUpload(str(tar), resumable=True, chunksize=64 * 1024 * 1024)
        if fid:
            cur = s.files().get(fileId=fid, fields="md5Checksum", supportsAllDrives=True).execute()
            if cur.get("md5Checksum") != m:
                s.files().update(fileId=fid, media_body=media, fields="id", supportsAllDrives=True).execute()
        else:
            fid = s.files().create(body={"name": tar.name, "parents": [folder]}, media_body=media, fields="id", supportsAllDrives=True).execute()["id"]
        fresh = s.files().get(fileId=fid, fields="md5Checksum,size", supportsAllDrives=True).execute()
        ok = fresh.get("md5Checksum") == m and int(fresh.get("size", -1)) == tar.stat().st_size
        done[tar.name] = {"id": fid, "md5": m, "bytes": tar.stat().st_size, "verified": ok, "source": str(p)}
        receipt.write_text(json.dumps(done, indent=1))
        print(("ok  " if ok else "BAD ") + f"{tar.stat().st_size/1e9:.2f} GB  {tar.name}", flush=True)
        if ok: tar.unlink()
    n = sum(v["verified"] for v in done.values())
    print(f"DONE {n}/{len(entries)} archives verified on Drive; receipt {receipt}")
    print("format_lab may be deleted locally" if n == len(entries) else "NOT complete: re-run to resume")

if __name__ == "__main__":
    main()

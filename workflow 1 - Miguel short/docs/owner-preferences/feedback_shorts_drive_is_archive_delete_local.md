---
name: feedback_shorts_drive_is_archive_delete_local
description: "Shorts retention: Google Drive is the archive; a published package's local copy is deleted automatically at the end of every publish batch (standing authorization 2026-09-19); Partially Published stays local"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 8d388668-a29a-48be-998b-e8df70b57f3f
  modified: 2026-09-19T05:58:17.430Z
---

Miguel, 2026-09-07: "we keep everything in Google Drive usually. For all of the ones that are ready to publish, everything should be in Google Drive except for the raw videos. For the finished videos what we do is we upload them and then once they're uploaded we delete them from local."

Miguel, 2026-09-19, after 96 GB of already-archived packages had piled up under `~/Movies/Shorts Factory`: "we shouldn't have to be doing this man. by the end of the workflow you should always delete the local copies once they're in drive." He asked to keep `Partially Published/` (the ten August YouTube-only shorts) locally.

**Why:** the MacBook is not the archive; 30+ GB per batch fills the disk, Drive already holds the verified copy, and leaving retirement to a separate confirmation step meant it never ran (found twice: 78 GB on 2026-09-12, 96 GB on 2026-09-19).
**How to apply:** this is a STANDING AUTHORIZATION, no per-batch confirmation. `pipeline/publish/publish_batch.py --write` ends every batch with `close_out`: for each package published on all three platforms (scheduled = published, see [[feedback_publish_only_after_explicit_batch_go]]) it re-pushes the package to Drive (tracking files revised in place) and runs `retire_local.py --write`, which refuses unless every local byte is verified on Drive, then deletes the redundant `~/Movies` raw. `--close-out-only` runs the pass on an old batch. Never leave a published package local. Keep `Partially Published/` until Miguel says otherwise; `Revisions/` and `Format Lab/` are not Drive copies and are his call. See [[project_fable5_video_factory]].

## Index notes (moved from MEMORY.md 2026-09-23)

- ends with close_out (Drive re-push + retire_local + raw); Partially Published stays local

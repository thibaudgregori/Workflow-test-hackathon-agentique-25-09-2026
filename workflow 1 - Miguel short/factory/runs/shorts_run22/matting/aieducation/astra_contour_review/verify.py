"""Read-only contour comparison; writes review evidence in this directory."""
from pathlib import Path
import hashlib
import json

import cv2
import numpy as np
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent
SESSION = OUT.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polygon(points):
    image = Image.new("L", (1440, 900))
    ImageDraw.Draw(image).polygon([tuple(p) for p in points], fill=255)
    return np.asarray(image) > 0


def rectangle(box):
    x0, y0, x1, y1 = box
    region = np.zeros((900, 1440), dtype=bool)
    region[y0:y1, x0:x1] = True
    return region


old = np.asarray(Image.open(SESSION / "selection.mask.png.pre_astra").convert("L"))
new = np.asarray(Image.open(SESSION / "selection.mask.png").convert("L"))
assert set(np.unique(old)) == {0, 255}
assert set(np.unique(new)) == {0, 255}
removed = new < old
added = new > old
changed = new != old
edits = json.loads((OUT / "edits.json").read_text())
approved = json.loads((SESSION / "selection.json").read_text())
validated = json.loads((OUT / "validate.json").read_text())
assert approved == validated
assert approved["edits"] == edits
assert Path(approved["mask"]) == SESSION / "selection.mask.png"
assert approved["mask_sha256"] == sha(SESSION / "selection.mask.png")
assert approved["base_mask_sha256"] == sha(SESSION / "selection.mask.png.pre_astra")

union = np.zeros_like(removed)
per_polygon = []
for edit in edits:
    region = polygon(edit["points"])
    per_polygon.append({**edit, "removed_pixels": int((removed & region & ~union).sum()),
                        "old_selected_pixels": int(((old > 0) & region).sum()),
                        "new_selected_pixels": int(((new > 0) & region).sum())})
    union |= region
assert not np.any(changed & ~union)
assert not np.any(added)
assert all(item["new_selected_pixels"] == 0 for item in per_polygon)

# This envelope was traced from source pixels at 8x before comparison.
# It includes the left ear and facial edge; it is not a full-width head row band.
head_envelope = [
    [548, 225], [548, 242], [542, 244], [536, 246], [532, 250],
    [530, 255], [529, 264], [529, 275], [531, 282], [534, 291],
    [536, 300], [538, 309], [540, 320], [542, 328], [545, 337],
    [548, 344], [550, 350], [553, 354], [557, 359], [562, 364],
    [567, 368], [569, 372], [571, 380], [574, 389], [900, 389], [900, 225]
]
regions = {
    "cap_and_hair": {"box_half_open": [547, 0, 900, 250]},
    "head_face_and_both_ears": {"polygon": head_envelope},
    "lower_face_neck_shoulders_and_hands_full_width": {"box_half_open": [0, 389, 1440, 900]},
    "shoulder_arrival_full_width": {"box_half_open": [0, 460, 1440, 580]},
    "left_hand": {"box_half_open": [320, 610, 665, 900]},
    "right_hand": {"box_half_open": [860, 570, 1065, 900]},
}
for item in regions.values():
    region = polygon(item["polygon"]) if "polygon" in item else rectangle(item["box_half_open"])
    item.update(old_selected_pixels=int(((old > 0) & region).sum()),
                new_selected_pixels=int(((new > 0) & region).sum()),
                removed_pixels=int((removed & region).sum()),
                changed_pixels=int((changed & region).sum()))
    assert item["removed_pixels"] == item["changed_pixels"] == 0

furniture = {
    "left_chair_below_ear": [[505, 400], [565, 400], [585, 439], [585, 460], [565, 478], [550, 479], [529, 493], [505, 502]],
    "left_chair_at_shoulder_arrival": [[445, 529], [448, 516], [461, 507], [490, 504], [489, 508], [471, 518], [458, 525]],
    "right_chair_at_shoulder_arrival": [[935, 502], [958, 507], [974, 519], [982, 540], [983, 549], [960, 539], [942, 527], [935, 520]],
}
furniture_stats = {}
for name, points in furniture.items():
    region = polygon(points)
    furniture_stats[name] = {"polygon": points, "region_pixels": int(region.sum()),
                             "old_selected_pixels": int(((old > 0) & region).sum()),
                             "new_selected_pixels": int(((new > 0) & region).sum())}
    assert furniture_stats[name]["new_selected_pixels"] == 0

manifest = json.loads((OUT / "before_hashes.json").read_text())
changed_existing = [name for name, digest in manifest.items() if sha(SESSION / name) != digest]
assert sorted(changed_existing) == ["selection.json", "selection.mask.png"]
assert sha(SESSION / "selection.json.pre_astra") == "573542135e2ab1d81cbacb30f3c5e5572db5e8a235ea028c951f769eaf9a0af0"
ys, xs = np.where(removed)
report = {
    "selection": str(SESSION / "selection.json"), "status": approved["status"],
    "validation": "PASS", "coordinate_system": "1440x900 plate; x right, y down; polygon vertices inclusive",
    "mask_sha256_before": sha(SESSION / "selection.mask.png.pre_astra"),
    "mask_sha256_after": sha(SESSION / "selection.mask.png"),
    "removed_pixels": int(removed.sum()), "added_pixels": int(added.sum()),
    "changed_bbox_inclusive": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
    "polygons": per_polygon, "protected_anatomy_regions": regions,
    "furniture_regions": furniture_stats, "changed_preexisting_files": changed_existing,
    "other_preexisting_files_sha256_unchanged": len(manifest) - len(changed_existing),
    "scope": "Local first-frame contour approval only. No network, tracking, GPU, ship or alpha-video modification. Temporal repair remains untested.",
    "band_interpretation": "The removed chair shares y233-388 with the head. Zero-loss claims refer to source-traced anatomy regions, not all pixels in those horizontal rows.",
}
(OUT / "verification.json").write_text(json.dumps(report, indent=2) + "\n")

source = np.asarray(Image.open(SESSION / "selection.frame.png").convert("RGB"))
for name, mask in [("before", old), ("after", new)]:
    overlay = source.copy()
    contours, _ = cv2.findContours((mask > 0).astype("uint8"), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(overlay, contours, -1, (0, 255, 80), 1)
    Image.fromarray(overlay).crop((485, 210, 615, 405)).resize((780, 1170), Image.Resampling.NEAREST).save(OUT / f"{name}_ear_contour_6x.png")
    if name == "after":
        Image.fromarray(overlay).save(OUT / "after_full_contour.png")
        cream = np.full_like(source, (246, 241, 229))
        cream[mask > 0] = source[mask > 0]
        Image.fromarray(cream).save(OUT / "after_first_frame_preview.png")
diff_overlay = source.copy()
diff_overlay[removed] = (255, 0, 100)
Image.fromarray(diff_overlay).crop((485, 210, 615, 405)).resize((780, 1170), Image.Resampling.NEAREST).save(OUT / "removed_pixels_6x.png")
region_overlay = Image.fromarray(source.copy())
draw = ImageDraw.Draw(region_overlay)
draw.line([tuple(p) for p in head_envelope] + [tuple(head_envelope[0])], fill=(0, 230, 255), width=1)
for points in furniture.values():
    draw.line([tuple(p) for p in points] + [tuple(points[0])], fill=(255, 210, 0), width=1)
region_overlay.crop((420, 210, 1010, 580)).resize((1180, 740), Image.Resampling.NEAREST).save(OUT / "verification_regions_2x.png")
print(json.dumps({key: report[key] for key in ["validation", "removed_pixels", "added_pixels", "changed_bbox_inclusive", "mask_sha256_before", "mask_sha256_after", "other_preexisting_files_sha256_unchanged"]}, indent=2))
print(json.dumps({name: item["removed_pixels"] for name, item in regions.items()}, indent=2))
print(json.dumps(furniture_stats, indent=2))

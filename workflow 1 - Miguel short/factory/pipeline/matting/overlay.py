#!/usr/bin/env python
"""Paint the selection mask over frame zero so a reviewer (Astra, Miguel) can judge the outline.

    overlay.py <session dir> [--mask <png>] [--out <png>]
Writes <session>/selection.overlay.png (full frame, green fill + red contour) and
<session>/selection.overlay_head.png (a zoom on the head and shoulders). Prints both paths.
"""
import argparse
from pathlib import Path
import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("session", type=Path)
    ap.add_argument("--mask", type=Path, default=None, help="mask png (default: selection.mask.png, else prompts/kf_00000.png)")
    ap.add_argument("--out", type=Path, default=None)
    a = ap.parse_args()
    s = a.session
    frame = s / "selection.frame.png"
    if not frame.exists():
        raise SystemExit(f"no {frame}; run selection.py prepare first")
    mask_path = a.mask or (s / "selection.mask.png" if (s / "selection.mask.png").exists() else s / "prompts/kf_00000.png")
    f = cv2.imread(str(frame)); m = cv2.imread(str(mask_path), 0)
    if m.shape[:2] != f.shape[:2]:
        m = cv2.resize(m, (f.shape[1], f.shape[0]), interpolation=cv2.INTER_NEAREST)
    mask = m > 127
    over = f.copy(); over[mask] = (0.55 * over[mask] + 0.45 * np.array([0, 200, 0])).astype(np.uint8)
    cnts, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(over, cnts, -1, (0, 0, 255), 2)
    out = a.out or (s / "selection.overlay.png"); cv2.imwrite(str(out), over)
    ys, xs = np.where(mask)
    if len(ys):
        y0 = max(int(ys.min()) - 40, 0); y1 = min(y0 + 460, f.shape[0]); x0 = max(int(xs.mean()) - 380, 0); x1 = min(x0 + 760, f.shape[1])
        head = out.with_name(out.stem + "_head.png"); cv2.imwrite(str(head), over[y0:y1, x0:x1]); print(head)
    print(out); print(f"mask {mask_path} coverage {mask.mean():.3f}")


if __name__ == "__main__":
    main()

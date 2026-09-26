from pathlib import Path
import sys
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'pipeline/matting'))
from matte_review import frame_at, composite, caption, grid

out = Path(__file__).resolve().parent
session = out.parents[1] / 'matting/deepseekprices'
tiles = []
for f in [600, 605, 609, 610, 611, 615, 620, 625]:
    source = frame_at(session / 'plate_display_1386x990.mp4', 1386, 990, f, False)
    comp = composite(frame_at(session / 'matte_deepseekprices_v5_cut.webm', 1386, 990, f, True))
    pair = np.concatenate([source[:, 153:1233], comp[:, 153:1233]], axis=1)
    tiles.append(caption(Image.fromarray(pair).resize((810, 371)), f'f{f} {f/25:.2f}s source | delivered crop composite'))
grid(tiles, 2).save(out / 'hand_delivery_window.jpg', quality=92)

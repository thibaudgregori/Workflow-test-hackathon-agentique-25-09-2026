from pathlib import Path
import sys
import json
import hashlib
from PIL import Image, ImageDraw

F = Path('/Users/migle/Documents/Workspace/projects/personal/content/shorts-factory')
sys.path.insert(0, str(F / 'pipeline/matting'))
from matte_review import frame_at, composite

R = F / 'runs/shorts_run24'
M = R / 'matting/primeagent'
O = R / 'review/astra_primeagent'
sheet = Image.new('RGB', (1496, 3 * 515), '#ffffff')
draw = ImageDraw.Draw(sheet)
for row, idx in enumerate((1045, 1050, 1055)):
    source = Image.fromarray(frame_at(M / 'plate_display_1496x990.mp4', 1496, 990, idx, False))
    cut = Image.fromarray(composite(frame_at(M / 'matte_primeagent_v5_cut.webm', 1496, 990, idx, True)))
    sheet.paste(source.resize((748, 495)), (0, row * 515 + 20))
    sheet.paste(cut.resize((748, 495)), (748, row * 515 + 20))
    draw.text((5, row * 515 + 3), f'Frame {idx}, {idx/25:.2f}s: source | installed SAM2 matte', fill='black')
sheet.save(O / 'tail_source_composite.jpg', quality=95)
ship = json.loads((R / 'prep/stages/primeagent.ship.json').read_text())
for layer in ('cut', 'rim', 'alpha'):
    p = M / f'matte_primeagent_v5_{layer}.webm'
    assert hashlib.sha256(p.read_bytes()).hexdigest() == ship['keys'][f'{layer}_sha256']
print('All three installed hashes match the fresh ship marker.')

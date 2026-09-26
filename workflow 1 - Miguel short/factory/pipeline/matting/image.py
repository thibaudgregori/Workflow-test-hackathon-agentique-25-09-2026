"""The pinned MatAnyone2 Modal image, extracted from the outline lab on 2026-09-20.

Production matting (`pipeline/matting/modal_app.py`) used to load this definition straight out of
the outline lab's modal_app.py (now `references/labs/outline-lab-2026-09-05/`), a dated experiment folder. The definition is the same; only the
home changed. Weights are baked in from MODEL_CACHE at deploy time and `model-lock.json` pins them.
"""
from pathlib import Path
import modal

HERE = Path(__file__).resolve().parent
FACTORY = HERE.parents[1]
MODE = 'matanyone2'
# the weights the image bakes in (moved from output/shorts-outline-lab/2026-09-05/models on 2026-09-20)
MODEL_CACHE = FACTORY / 'pipeline/models/outline' if modal.is_local() else Path('/opt/models')

if modal.is_local():
    image = (modal.Image.debian_slim(python_version='3.11')
     .apt_install('git', 'ffmpeg', 'libgl1', 'libglib2.0-0')
     .pip_install('torch==2.8.0', 'torchvision==0.23.0', 'numpy<3', 'opencv-python-headless', 'pillow', 'tqdm', 'hydra-core', 'iopath', 'einops', 'scipy', 'imageio', 'huggingface_hub==0.36.2', 'safetensors', 'kornia', 'timm', 'transformers==4.57.1', 'requests', 'psutil')
     .run_commands('git clone https://github.com/pq-yang/MatAnyone2.git /opt/MatAnyone2 && cd /opt/MatAnyone2 && git checkout 0079197acd6d16a741f71558809c06c586c579e0',
                   'git clone https://github.com/FudanCVL/SAM2Matting.git /opt/SAM2Matting && cd /opt/SAM2Matting && git checkout 73dd721d77b56749248aefe5e8824d7f61b9d13c')
     .env({'PYTHONPATH': '/opt/MatAnyone2:/opt/SAM2Matting', 'OMP_NUM_THREADS': '2', 'HF_HUB_OFFLINE': '1'})
     .add_local_file(HERE / 'model-lock.json', '/opt/model-lock.json', copy=True)
     .add_local_dir(MODEL_CACHE / MODE, '/opt/models/' + MODE, copy=True)
     .run_commands('python -c "from matanyone2 import MatAnyone2; from sam2.build_sam import build_sam2matting_video_predictor; from transformers import VitMatteForImageMatting; print(1)"'))
else:
    image = modal.Image.debian_slim()

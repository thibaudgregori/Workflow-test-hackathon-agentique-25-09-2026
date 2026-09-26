"""Validate returned frames, hashes and narrow consistency diagnostics."""
from pathlib import Path
import json,subprocess,hashlib
from run_test import OUT
p=OUT/'auto-model-benchmark';summary=[];seen={};validation=[]
for mode in ['birefnet','modnet','mediapipe']:
 d=json.loads((p/mode/'r1/metrics.json').read_text());assert d['local_worker_matches'];raw=[r for r in d['results'] if r['variant']=='raw'];summary.append(dict(model=mode,seed_times=' / '.join(f"{r['seed_seconds']:.3f}" for r in raw),model_load_seconds=d['model_load_seconds'],function_seconds=d['function_seconds'],estimated_compute_usd=d['estimated_compute_usd'],conservative_elapsed_estimate_usd=d['conservative_elapsed_estimate_usd'],client_wall_seconds=d['client_wall_seconds'],face_pixels_added=[r['added_face_pixels'] for r in d['results'] if r['variant']=='faceguard'],face_minimum=[min((s['face_core_retained'] for s in r['qa']['face_samples'] if s['face_core_retained'] is not None),default=None) for r in raw]))
 for r in d['results']:
  root=p/mode/'r1'/r['video']/r['variant'];mask=root/'mask.png';assert hashlib.sha256(mask.read_bytes()).hexdigest()==r['mask_sha256'];alpha=root/'alpha.mkv';sha=hashlib.sha256(alpha.read_bytes()).hexdigest()
  if sha not in seen:
   q=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','stream=width,height,nb_read_frames,r_frame_rate','-of','json',str(alpha)]))['streams'][0];seen[sha]=q
  q=seen[sha];assert int(q['nb_read_frames'])==r['frames']==r['qa']['frames'];assert [q['width'],q['height']]==r['source_size'];assert q['r_frame_rate']=='25/1';validation.append(dict(model=mode,video=r['video'],variant=r['variant'],sha256=sha,**q))
(p/'validation.json').write_text(json.dumps({'streams':validation,'unique_alpha_outputs':len(seen),'unique_frames':sum(int(v['nb_read_frames']) for v in seen.values())},indent=2));(p/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2));print('Validated',len(validation),'streams,',len(seen),'unique outputs')

"""Download public, pinned weights during the image build; verify file hashes."""
from pathlib import Path
import hashlib,json,requests,os
from concurrent.futures import ThreadPoolExecutor

def install():
    specs=json.loads(Path(os.environ.get('MODEL_LOCK','/opt/model-lock.json')).read_text())
    jobs=[]
    for name,item in specs.items():
        dest=Path(os.environ.get('MODEL_ROOT','/opt/models'))/name;dest.mkdir(parents=True,exist_ok=True)
        for entry in item['files']:jobs.append((name,item,dest,entry))
    def fetch(job):
            name,item,dest,entry=job
            path=entry['path']; target=dest/Path(path).name
            url=f"https://huggingface.co/{item['repo']}/resolve/{item['revision']}/{path}"
            r=requests.get(url,stream=True,timeout=60);r.raise_for_status()
            with target.open('wb') as f:
                for block in r.iter_content(1024*1024): f.write(block)
            data=target.read_bytes()
            assert len(data)==entry['size'],path
            if 'lfs' in entry: assert hashlib.sha256(data).hexdigest()==entry['lfs']['oid'],path
            else: assert hashlib.sha1(f'blob {len(data)}\0'.encode()+data).hexdigest()==entry['oid'],path
            print('VERIFIED',name,path,flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(fetch,jobs))

if __name__=='__main__':install()

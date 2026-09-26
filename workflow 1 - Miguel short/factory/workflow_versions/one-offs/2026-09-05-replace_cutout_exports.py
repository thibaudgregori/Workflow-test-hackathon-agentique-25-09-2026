"""Revise already archived TikTok exports in place; plan first, explicit --apply.

Preserves Drive IDs, permissions, previous binary revisions and local backups.
Only approved remakes in the supplied inventory are eligible.
"""
import argparse, concurrent.futures, hashlib, json, os, shutil
from pathlib import Path
from googleapiclient.http import MediaFileUpload, MediaInMemoryUpload
from push_run_to_drive import svc, SHORTS_CONTAINER

WS=Path.home()/'Documents/Workspace'
FACTORY=Path(__file__).resolve().parents[2]
OUT=WS/'output/shorts-tiktok-remake/2026-09-05/drive-replacement'
INVENTORY=WS/'output/shorts-unpublished-audit/2026-09-05/delivery-inventory.json'
REMAKE=FACTORY/'shorts_tiktok_remake_20260905'
FIELDS='id,name,parents,mimeType,ownedByMe,trashed,size,md5Checksum,version,headRevisionId,webViewLink,appProperties'
def read(p): return json.loads(Path(p).read_text())
def save(p,d):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def hashfile(p,alg='sha256'):
 h=hashlib.new(alg)
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def get(s,fid):return s.files().get(fileId=fid,fields=FIELDS,supportsAllDrives=True).execute(num_retries=3)
def upload(s,fid,path=None,data=None):
 media=MediaFileUpload(str(path),mimetype='video/mp4',resumable=True,chunksize=8*1024*1024) if path else MediaInMemoryUpload(data,mimetype='application/json',resumable=True)
 req=s.files().update(fileId=fid,media_body=media,keepRevisionForever=True,fields=FIELDS,supportsAllDrives=True)
 result=None
 while result is None: _,result=req.next_chunk(num_retries=3)
 return result

def plan_one(item,pkg):
 s=svc();d=read(pkg/'Publishing/package.json');dm=read(pkg/'Publishing/drive_manifest.json')
 assert d['short_id']==dm['short_id']==item['notion_id']
 folder=get(s,dm['folder_id']);assert folder['ownedByMe'] and not folder['trashed']
 assert folder.get('appProperties',{}).get('short_id')==d['short_id']
 parent=get(s,folder['parents'][0]);assert parent['parents']==[SHORTS_CONTAINER] and parent['name']=='Ready to Publish'
 files={x['path']:x for x in dm['files']};video=get(s,files['Exports/TikTok.mp4']['id'])
 exportdir=get(s,video['parents'][0]);assert exportdir['name']=='Exports' and exportdir['parents']==[folder['id']]
 assert video['name']=='TikTok.mp4' and video['ownedByMe'] and not video['trashed']
 manifest=get(s,files['Publishing/package.json']['id']);pub=get(s,manifest['parents'][0])
 assert pub['name']=='Publishing' and pub['parents']==[folder['id']]
 remote_package=json.loads(s.files().get_media(fileId=manifest['id']).execute())
 assert remote_package['short_id']==d['short_id']
 new=OUT.parent/'tiktok'/f"{item['id']}_cutout.mp4";sha=hashfile(new)
 final=read(REMAKE/'review'/f"final_{item['id']}_cutout.json")
 assert final['verdict']=='PASS' and final['mp4_sha256']==sha
 old=pkg/'Exports/TikTok.mp4';assert hashfile(old,'md5')==video['md5Checksum']
 assert hashfile(old)==d['files']['Exports/TikTok.mp4']==remote_package['files']['Exports/TikTok.mp4']
 return {'id':item['id'],'short_id':d['short_id'],'package':str(pkg),'new':str(new),'sha256':sha,'md5':hashfile(new,'md5'),'size':new.stat().st_size,'folder':folder,'video':video,'manifest':manifest,'remote_package':remote_package}

def apply_one(row):
 receipt=OUT/'receipts'/f"{row['id']}.json"
 if receipt.exists():return read(receipt)
 s=svc();fresh=get(s,row['video']['id']);assert fresh['version']==row['video']['version'],'Remote changed since plan'
 assert hashfile(row['new'])==row['sha256']
 pkg=Path(row['package']);backup=OUT/'previous'/row['id'];backup.mkdir(parents=True,exist_ok=True)
 for name in ['package.json','drive_manifest.json']:
  target=backup/name
  if not target.exists():shutil.copy2(pkg/'Publishing'/name,target)
 old=pkg/'Exports/TikTok.mp4';oldbackup=backup/'TikTok.mp4'
 if not oldbackup.exists():os.link(old,oldbackup)
 save(backup/'remote-package.json',row['remote_package'])
 # Pin old Drive revisions before writing. No existing file/revision is deleted.
 for meta in [fresh,row['manifest']]:
  assert meta.get('headRevisionId')
  s.revisions().update(fileId=meta['id'],revisionId=meta['headRevisionId'],body={'keepForever':True}).execute(num_retries=3)
 upload(s,fresh['id'],path=row['new']);after=get(s,fresh['id'])
 assert after['md5Checksum']==row['md5'] and int(after['size'])==row['size'] and after['parents']==fresh['parents']
 current=get(s,row['manifest']['id']);assert current['md5Checksum']==row['manifest']['md5Checksum'],'Package changed concurrently'
 revision={'export':'Exports/TikTok.mp4','sha256':row['sha256'],'previous_sha256':row['remote_package']['files']['Exports/TikTok.mp4'],'source_run':REMAKE.name,'recording_id':row['id'],'note':'Approved cutout export revision. Existing source/project archives retained as historical originals; remake source remains in source_run.'}
 remote=dict(row['remote_package']);remote['files']=dict(remote['files']);remote['files']['Exports/TikTok.mp4']=row['sha256'];remote.setdefault('export_revisions',[]).append(revision)
 data=(json.dumps(remote,indent=2)+'\n').encode();upload(s,current['id'],data=data);pm=get(s,current['id']);assert pm['md5Checksum']==hashlib.md5(data).hexdigest()
 temp=old.with_name('TikTok.remake-upload-verified.mp4');shutil.copy2(row['new'],temp);os.replace(temp,old)
 local=read(pkg/'Publishing/package.json');local['files']['Exports/TikTok.mp4']=row['sha256'];local.setdefault('export_revisions',[]).append(revision);save(pkg/'Publishing/package.json',local)
 dm=read(pkg/'Publishing/drive_manifest.json')
 for entry in dm['files']:
  if entry['path']=='Exports/TikTok.mp4':entry['md5']=row['md5']
  if entry['path']=='Publishing/package.json':entry['md5']=pm['md5Checksum']
 save(pkg/'Publishing/drive_manifest.json',dm)
 result={'id':row['id'],'file_id':after['id'],'url':after['webViewLink'],'verified':True,'md5':row['md5'],'size':row['size'],'previous_revision':fresh['headRevisionId'],'current_revision':after['headRevisionId'],'local_sha256':hashfile(old)}
 assert result['local_sha256']==row['sha256'];save(receipt,result);print(json.dumps(result),flush=True);return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--apply',action='store_true');a=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
 if not a.apply:
  inventory=read(INVENTORY);pkgs={}
  for p in (Path.home()/'Movies/Shorts Factory/Ready to Publish').glob('*/Publishing/package.json'):
   d=read(p);key=d.get('internal_source',{}).get('recording_id')
   if key in {x['id'] for x in inventory}:assert key not in pkgs;pkgs[key]=p.parent.parent
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
   rows=list(pool.map(lambda x:plan_one(x,pkgs[x['id']]),inventory))
  save(OUT/'plan.json',rows);print(json.dumps({'matched':len(rows),'different':sum(x['md5']!=x['video']['md5Checksum'] for x in rows),'bytes':sum(x['size'] for x in rows)}))
 else:
  rows=read(OUT/'plan.json')
  with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(apply_one,rows))
  s=svc()
  for row in rows:
   fresh=get(s,row['video']['id']);assert fresh['md5Checksum']==row['md5'] and int(fresh['size'])==row['size']
  save(OUT/'verified.json',{'count':len(results),'all_verified':True,'results':results})
if __name__=='__main__':main()

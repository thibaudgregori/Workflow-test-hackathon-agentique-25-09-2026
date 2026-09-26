"""Send the approved experiment media to Miguel's verified WhatsApp self-chat.

Persist each send immediately and verify the exact downloaded attachment, so a
rerun verifies an uncertain send instead of duplicating it.
"""
import argparse,hashlib,json,mimetypes,os,time
from pathlib import Path
import requests
from dotenv import load_dotenv

ROOT=Path(__file__).resolve().parents[6]
OUT=ROOT/'output/shorts-outline-lab/2026-09-05'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--manifest',type=Path,default=OUT/'whatsapp/manifest.json');parser.add_argument('--receipts',type=Path,default=OUT/'whatsapp');args=parser.parse_args();args.receipts.mkdir(parents=True,exist_ok=True)
    load_dotenv(ROOT/'.env')
    base=os.environ['UNIPILE_BASE_URL'].rstrip('/')+'/api/v1'
    aid=os.environ['UNIPILE_ACCOUNT_ID_WHATSAPP']
    expected=json.loads((OUT/'whatsapp/identity.json').read_text())
    cid=expected['chat']['id']
    session=requests.Session()
    session.headers.update({'X-API-KEY':os.environ['UNIPILE_API_KEY'],'Accept':'application/json'})
    def get(route,**kwargs):
        r=session.get(base+route,timeout=120,**kwargs);r.raise_for_status();return r
    account=get('/accounts/'+aid).json();chat=get('/chats/'+cid).json()
    assert aid==expected['account_id'] and account['type']=='WHATSAPP'
    assert chat['account_id']==aid and chat['provider_id']==expected['chat']['provider_id']
    manifest=json.loads(args.manifest.read_text())
    for entry in manifest:
        path=OUT/entry['file'];blob=path.read_bytes();sha=hashlib.sha256(blob).hexdigest()
        receipt=args.receipts/f'{path.stem}-receipt.json'
        mime=mimetypes.guess_type(path.name)[0]
        if receipt.exists():
            record=json.loads(receipt.read_text());assert record['sha256']==sha
        else:
            record={'file':entry['file'],'sha256':sha,'bytes':len(blob),'state':'dispatching'}
            receipt.write_text(json.dumps(record,indent=2))
            with path.open('rb') as fh:
                r=session.post(base+'/chats/'+cid+'/messages',data={'account_id':aid,'text':entry['caption']},files={'attachments':(path.name,fh,mime)},timeout=120)
            r.raise_for_status();record.update(message_id=r.json()['message_id'],state='sent')
            receipt.write_text(json.dumps(record,indent=2))
        if 'message_id' not in record:raise RuntimeError('Uncertain prior send; inspect self-chat before any retry')
        mid=record['message_id'];message=None
        for attempt in range(5):
            cursor=None
            for page in range(5):
                params={'limit':100}
                if cursor:params['cursor']=cursor
                payload=get('/chats/'+cid+'/messages',params=params).json()
                message=next((x for x in payload.get('items',[]) if x['id']==mid),None)
                if message:break
                cursor=payload.get('cursor')
                if not cursor:break
            if message and message.get('attachments'):break
            time.sleep(2)
        assert message and message.get('attachments'), 'Exact sent message missing attachment'
        attachment=message['attachments'][0]
        assert attachment.get('unavailable') is False and attachment['mimetype']==mime
        remote=get('/messages/'+mid+'/attachments/'+attachment['id']).content
        assert hashlib.sha256(remote).hexdigest()==sha, 'Downloaded attachment differs'
        record.update(state='verified',attachment_id=attachment['id'],mimetype=mime,download_sha256=hashlib.sha256(remote).hexdigest(),verified_at=time.time())
        receipt.write_text(json.dumps(record,indent=2))
        print('VERIFIED',path.name,mid,flush=True)
        time.sleep(1)

if __name__=='__main__':main()

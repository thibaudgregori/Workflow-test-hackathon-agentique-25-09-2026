"""Refresh searchable library metadata, origin mappings and checksums."""
from pathlib import Path
from collections import defaultdict,Counter
import hashlib,json,os
from asset_library import WORKSPACE as W,ASSETS as A


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()


def main():
    catalog=A/'catalog';catalog.mkdir(exist_ok=True)
    mapping=json.loads((catalog/'source-map.json').read_text())
    origins=defaultdict(list);roles=defaultdict(set)
    for row in mapping['sources']:
        target=(W/row['canonical']).resolve()
        if not target.is_file():raise FileNotFoundError(target)
        row['canonical']=str(target.relative_to(W));origins[target].append(row['path']);roles[target].add(row['decision'])
    (catalog/'source-map.json').write_text(json.dumps(mapping,indent=2))
    bank=json.loads((A/'images/miguel-photo-bank/manifest.json').read_text());inactive=set(bank['photos'])-set(bank['active_poses'])
    rows=[];seen=set()
    for root,dirs,names in os.walk(A,followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(root)/d).is_symlink() and d not in {'catalog','__pycache__'}]
        for name in sorted(names):
            p=Path(root)/name
            if p.is_symlink() or name in {'.DS_Store','MANIFEST.sha256','README.md'}:continue
            rel=p.relative_to(A);parts=rel.parts
            if parts[0] not in {'audio','videos','images','logos','fonts','models','documents','templates','brand','written','manuals'}:continue
            e=p.suffix.lower()
            if parts[0] in {'images','audio','videos','logos','fonts','models'} and e in {'.json','.csv','.txt','.md','.py'}:continue
            status='reference' if 'references' in parts or roles[p]&{'third-party-reference','style-reference','thumbnail-reference','product-reference'} else 'available'
            if parts[0]=='images' and 'miguel-photo-bank' in parts:
                if any(n in parts or p.stem==n or p.stem.startswith(n+'-') for n in inactive):status='inactive'
                elif any(n.startswith('selections-') for n in parts):status='historical'
                else:status='approved'
            if p.name=='bed_split.mp3' and parts[:3]==('audio','music','shorts-factory'):status='historical'
            if p.name=='bed_split_v2.mp3' and parts[:3]==('audio','music','shorts-factory'):status='approved'
            rows.append({'path':str(p.relative_to(W)),'type':parts[0],'status':status,'bytes':p.stat().st_size,'sha256':digest(p),'sources':sorted(set(origins[p])),'usage':'Reference material: inspect provenance and suitability before production.' if status=='reference' else 'Use within the owning brand and approved workflow; preserve original provenance.'})
    (catalog/'index.json').write_text(json.dumps({'assets':rows,'counts':dict(Counter(r['type'] for r in rows))},indent=2))
    for category in sorted({r['type'] for r in rows}):
        subset=[r for r in rows if r['type']==category]
        lines=[f'# {category.capitalize()} library', '',f'{len(subset)} indexed files. Status separates approved assets, references and historical material.','', '| Asset | Status |', '|---|---|']
        for r in subset:
            path=Path(r['path']);lines.append(f'| [{path.name}](../../{path.relative_to("assets").as_posix()}) | {r["status"]} |')
        # From assets/catalog the target is one parent level up, not two.
        (catalog/f'{category}.md').write_text('\n'.join(lines).replace('](../../','](../')+'\n')
    checks=[]
    for root,dirs,names in os.walk(A,followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(root)/d).is_symlink()]
        for name in names:
            p=Path(root)/name
            if p.is_symlink() or name in {'.DS_Store','MANIFEST.sha256'}:continue
            checks.append(f'{digest(p)}  {p.relative_to(W)}')
    (A/'MANIFEST.sha256').write_text('\n'.join(sorted(checks))+'\n')
    print(json.dumps({'indexed':len(rows),'types':dict(Counter(r['type'] for r in rows)),'source_aliases':len(mapping['sources'])}))

if __name__=='__main__':main()

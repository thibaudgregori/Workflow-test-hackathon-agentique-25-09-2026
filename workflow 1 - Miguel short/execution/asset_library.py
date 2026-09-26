"""Find canonical media and resolve legacy source names without reading project copies."""
from functools import lru_cache
from pathlib import Path
import argparse
import json

WORKSPACE=Path(__file__).resolve().parents[1]
ASSETS=WORKSPACE/'assets'

@lru_cache(maxsize=1)
def source_map():
    return {r['path']:r for r in json.loads((ASSETS/'catalog/source-map.json').read_text())['sources']}


def resolve_source(source):
    """Treat a historical path as an identity; return only its canonical asset."""
    source=Path(source).expanduser()
    if not source.is_absolute():source=WORKSPACE/source
    relative=source.relative_to(WORKSPACE).as_posix()
    if relative.startswith('assets/'):
        target=source.resolve()
    else:
        entry=source_map().get(relative)
        if entry is None:raise FileNotFoundError(f'Asset is not registered in the central library: {relative}')
        target=(WORKSPACE/entry['canonical']).resolve()
    if not target.is_relative_to(ASSETS.resolve()) or not target.is_file():
        raise FileNotFoundError(f'Canonical asset missing: {target}')
    return target


def source_files(directory,suffix='.mp3'):
    directory=Path(directory)
    if not directory.is_absolute():directory=WORKSPACE/directory
    prefix=directory.relative_to(WORKSPACE).as_posix()+'/'
    return [(Path(key).name,resolve_source(key)) for key in sorted(source_map())
            if key.startswith(prefix) and '/' not in key[len(prefix):] and key.endswith(suffix)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query',nargs='?',default='')
    parser.add_argument('--type',choices=['audio','videos','images','logos','fonts','models','documents','templates'])
    parser.add_argument('--limit',type=int,default=30)
    parser.add_argument('--resolve',type=Path)
    parser.add_argument('--full',action='store_true',help='Include every historical source path')
    args=parser.parse_args()
    if args.resolve:print(resolve_source(args.resolve));return
    rows=json.loads((ASSETS/'catalog/index.json').read_text())['assets']
    terms=args.query.casefold().split();result=[]
    for r in rows:
        if args.type and r['type']!=args.type:continue
        if r.get('status') in {'inactive','historical'}:continue
        hay=' '.join([r['path'],*r.get('sources',[])]).casefold()
        if all(t in hay for t in terms):result.append(r)
    shown=result[:args.limit]
    if not args.full:
        shown=[{**r,'source_count':len(r.get('sources',[])),'sources':r.get('sources',[])[:3]} for r in shown]
    print(json.dumps({'matches':len(result),'assets':shown},indent=2))

if __name__=='__main__':main()

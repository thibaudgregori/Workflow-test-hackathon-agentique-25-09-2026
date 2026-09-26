"""Production adapter for the existing prep stage markers and cost ledger."""
from pathlib import Path
import json, sys, time
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from selection import validate
from client import execute


def finish_package(pkg, run, row, *, await_display, mark, selection_timeout=1800):
    session=Path(pkg['session']);vid=pkg['id'];st=pkg['stages']
    if st.get('plate',{}).get('status') not in ('ok','reused'):
        mark(pkg,'track',{'status':'error','error':'No valid prepared plate'});return
    plate=Path(st['plate']['plate']);source=Path(st['cut']['master']);crop=session/'plate.json'
    selection=Path(row.get('selection') or session/'selection.json')
    start=time.monotonic()
    mark(pkg,'selection',{'status':'needs_visual_review','selection':str(selection),'plate':str(plate),
        'source':str(source),'crop':str(crop),'initial_mask':st.get('prompt0',{}).get('prompt_png')})
    while True:
        try:validate(selection,plate,source,crop);break
        except (ValueError,FileNotFoundError,json.JSONDecodeError) as e:
            if time.monotonic()-start>selection_timeout:
                mark(pkg,'track',{'status':'error','error':'Reviewed selection required: '+str(e)});return
            time.sleep(2)
    # THE CHAIR AUDIT (run 24, `claudesessions`) — a reviewed selection is a
    # SENTENCE about the chair until something measures it.  That one signed
    # "the chair is outside; no edits needed" over a mask that still held 6,822
    # px of the right headrest wing, and MatAnyone, which is prompted with this
    # mask and nothing else, propagated the wedge through all 531 frames.
    # EVERY selection marker keeps its inputs (run 26, 2026-09-23): a later re-stamp dropped
    # plate/source/crop/initial_mask and the next outline review could not start.
    inputs={'plate':str(plate),'source':str(source),'crop':str(crop),'initial_mask':st.get('prompt0',{}).get('prompt_png')}
    from chair_audit import audit_selection
    audit=audit_selection(selection,plate,source,crop)
    if audit['verdict'] in ('refuse','hold'):
        mark(pkg,'selection',{'status':'error','selection':str(selection),**inputs,'chair_audit':audit,
            'error':'Chair audit '+audit['verdict']+': '+audit.get('why','')})
        mark(pkg,'track',{'status':'REFUSED','error':'Chair audit '+audit['verdict']+': '+audit.get('why','')})
        return
    if audit.get('healed'):
        validate(selection,plate,source,crop)
    mark(pkg,'selection',{'status':'ok','selection':str(selection),**inputs,'chair_audit':audit,
        'chair_audit_verdict':audit['verdict'],'chair_audit_leak_px':audit.get('leak_px'),
        'chair_audit_carve_px':audit.get('carve_px'),'chair_audit_healed':bool(audit.get('healed')),
        'chair_audit_mask_sha256':audit.get('mask_sha256'),
        'wall_s':time.monotonic()-start})
    display=await_display(vid,pkg)
    if not display:
        mark(pkg,'ship',{'status':'error','error':'Missing display plate'});return
    mark(pkg,'track',{'status':'running','backend':'matanyone2'})
    try:
        result=execute(plate,source,crop,selection,display,session,name=vid,
            resolution=int(row.get('matting_resolution',1024)))
        track=result['track'];ship=result['ship']
        mark(pkg,'track',{'status':'ok','backend':'matanyone2','model':'MatAnyone 2','alpha':str(session/'alpha_v1.mkv'),
            'track_seconds':track['function_seconds'],'cost_usd':track['estimated_compute_usd'],
            'review_status':'needs_final_visual_review','wall_s':track['client_wall_seconds']})
        mark(pkg,'ship',{'status':'ok','backend':'matanyone2',**ship,'headroom':result['headroom'],'ship_seconds':ship['seconds'],'wall_s':ship['client_wall_seconds'],
            'cost_usd':ship['estimated_compute_usd'],'review_status':'needs_final_visual_review'})
        import costs
        for stage,rec in [('track',track),('ship',ship)]:
            costs.safe_record(run,'modal',stage,rec['estimated_compute_usd'],video=vid,
                note='MatAnyone 2 '+stage+'; runtime estimate, not invoice',ref=result['key']+':'+stage)
    except Exception as e:
        mark(pkg,'track',{'status':'error','backend':'matanyone2','error':str(e)})
        mark(pkg,'ship',{'status':'error','error':'Matting/export incomplete: '+str(e)})

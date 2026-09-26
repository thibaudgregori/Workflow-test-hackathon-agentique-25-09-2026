# Split chassis

`build_hyperframes_r2.py` is the split format's reference generator: STANDARD.md names it as the
chassis and its `.scappill` caption rule is canonical (`pipeline/captions.py`, LAW on pills). The
daily workflow does NOT execute it; each recording's split lane is authored per video from the plan
(`gen/<id>_split_gen.py` via `pipeline/captions.py` and `pipeline/pointing_cues.py`). It stays here
as the executable definition of the format, with its July inputs frozen under `source/`
(`hyperframes_r2/`: the twenty July projects; `assets/`: the July face plates and UI captures).
Music and SFX resolve from the Workspace library (`assets/audio/{music,sfx}/shorts-factory/`).
Moved out of `pipeline/` on 2026-09-20 (NOTHING PERMANENT LIVES IN A RUN, and no July prototype
lives beside a live tool).

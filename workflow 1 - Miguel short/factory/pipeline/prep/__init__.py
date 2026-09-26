"""THE PREP STAGE — everything a daily builder used to do by hand before it
could design anything, done once, in parallel, for the whole batch, with no LLM
anywhere in the loop.

    prep_batch.py   the orchestrator: one thread per recording, Modal tracking
                    every recording at once, a prep package per video
    cutlib.py       take detection + the 4K cut master + the tight transcript
    platelib.py     plate measure/build, and the OVER-WIDE plate BY DEFAULT
    promptlib.py    the BiRefNet frame-0 silhouette and the MEASURED wing cut
    sourcelib.py    the X source post behind a pointing cue: fetch + card render
    birefnet_master_sweep.py
                    the master-space silhouette sweep (runs in the bake-off venv)

Nothing here decides anything a model would have to judge.  Every number it
writes is measured off the raw, the master, the plate or the API payload, and
every choice it makes is recorded with the measurement that forced it.
"""

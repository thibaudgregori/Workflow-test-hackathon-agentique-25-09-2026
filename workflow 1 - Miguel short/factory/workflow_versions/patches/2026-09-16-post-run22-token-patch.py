#!/usr/bin/env python
"""THE POLLING PATCH - apply to the live workflow AFTER run 22 closes.

MEASURED ON RUN 21 (2 recordings, 25 agents, 548,238,707 cache-read tokens):

  stage                        cacheRead    turns   bash   polls
  cutout:grokemail retry     231,727,254      625    523     415   <- 42% of the run
  whiteboard:codexdetail      46,496,772      162     90       8
  repair:grokemail cutout     38,217,394      194    101      37
  ...
  TOTAL POLLING TURNS ~ 177,147,441 tokens = 32% OF THE ENTIRE RUN

The runaway agent ran the SAME TWO COMMANDS 385 times:
    225x  tail -4 shorts_run21/gen/_rc_grokemail_cutout.log; date +%H:%M:%S
    160x  tail -6 shorts_run21/gen/_rc_grokemail_cutout.log; date +%H:%M:%S

Its tool results were TINY - median 135 characters, 517 KB across the whole
agent. The context was not big because of output; it was big because of TURNS.
Each turn re-reads the whole conversation, so cost grows with the SQUARE of the
turn count: 133 turns cost 29M, 625 turns cost 232M - 4.7x the turns, 8x the
tokens. Every `tail -4` cost roughly 370,000 tokens to learn 135 characters.

The agent never even tried a foreground call: its first render was already
`nohup ... &`, then it polled. The GATES have had the right rule since
2026-09-08 ("Never a monitor, never a background loop, never a foreground
sleep") and cost 300 KB each. The lane authors were never given it.

usage: python post_run_token_patch.py   (idempotent; asserts each anchor)
"""
import pathlib, shutil, datetime as dt

W = pathlib.Path.home() / 'Documents/Workspace/.claude/workflows/daily-shorts.js'
assert W.is_file(), W
stamp = dt.datetime.now().strftime('%Y-%m-%d-%H%M')
shutil.copy2(W, W.with_name(f'daily-shorts.js.bak-{stamp}'))
s = W.read_text()

def rep(old, new, tag):
    global s
    assert old in s, f'MISSING [{tag}]'
    # check only the text being ADDED: an anchor may legitimately contain a
    # backtick (it is matching real JS), but a replacement may never introduce one.
    added = new.replace(old, '')
    assert '`' not in added, f'BACKTICK IN ADDED TEXT [{tag}] - it ends the template literal'
    s = s.replace(old, new, 1)

NOPOLL = (
 "\nONE CALL, NOT THREE HUNDRED. THIS IS THE SINGLE BIGGEST COST IN THE FACTORY "
 "(measured on run 21, 2026-09-15). Run render_and_check in the FOREGROUND, as ONE Bash "
 "call, with an explicit timeout of 900000 ms. It takes about two to three minutes and it "
 "prints its own result. DO NOT launch it with nohup and DO NOT tail its log in a loop: "
 "run 21's cutout retry did exactly that - 385 repeats of the same two tail commands over "
 "625 turns - and burned 231,727,254 tokens, 42 percent of that entire run, to read a "
 "median of 135 characters per call. Every turn re-reads your whole context, so cost grows "
 "with the SQUARE of your turn count. If you ever background a long command, wait for it "
 "with ONE blocking call (until [ -s <file> ]; do sleep 15; done) inside a SINGLE Bash "
 "invocation with a long timeout - never a sequence of separate checks. IF YOU FIND "
 "YOURSELF RUNNING THE SAME COMMAND A SECOND TIME TO SEE IF SOMETHING FINISHED, STOP: you "
 "are in the pattern this rule exists to prevent. Keep your whole lane under ~80 turns.\n"
)

# 1. the three lane authors
rep(" It submits the render AND STARTS ITS qc_pass AND ITS GEMINI WATCHER THE MOMENT THE FILE LANDS.",
    NOPOLL + " It submits the render AND STARTS ITS qc_pass AND ITS GEMINI WATCHER THE MOMENT THE FILE LANDS.",
    'lane author no-poll')

# 2. the repair agent (37 of its 101 shell calls were polls)
rep("const REPAIR = (v, what, detail) => `You are the REPAIR AGENT for recording \"${v.id}\" in today's daily shorts run, and you get ONE round.",
    "const REPAIR = (v, what, detail) => `You are the REPAIR AGENT for recording \"${v.id}\" in today's daily shorts run, and you get ONE round."
    + NOPOLL.replace('render_and_check', 'any long command').replace('your whole lane', 'your whole repair'),
    'repair no-poll')

W.write_text(s)
print('daily-shorts.js patched; backup', W.with_name(f'daily-shorts.js.bak-{stamp}').name)

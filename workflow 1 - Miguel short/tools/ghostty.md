# Tool: Ghostty

> **Last Updated**: 2026-09-23 (restructured and condensed; G4/G8 marked legacy in favor of herdr)
> **Docs verified**: 2026-09-23: Ghostty 1.3.1 stable still installed; GitHub milestone 1.3.2 still open (2 open / 120 closed), no newer stable release. RAM findings 2026-08-23 to 08-31.
> **Type**: Local macOS terminal; AppleScript API (`/Applications/Ghostty.app/Contents/Resources/Ghostty.sdef`)

Miguel's terminal. Agent sessions and pane grids are managed by **herdr** (`herdr pane split`, `herdr agent start`), not by Ghostty splits.

---

## 1. What to use for what

| Job | Use | Why / notes |
|---|---|---|
| Agent sessions, pane grids | herdr | Never Ghostty AppleScript splits for agent layouts. |
| Launch Ghostty with arguments | `open -na Ghostty.app --args ...` (`--initial-command=...`, `--window-save-state=never`) | `ghostty +new-window` is unsupported on macOS. |
| Script an already running Ghostty | Native AppleScript: `new window`, `new tab`, `split <terminal> direction right|left|down|up`, `perform action "<action>" on <terminal>`, `focus`, `input text`, `send key` | Never `System Events` keystrokes (Accessibility; fails from Raycast with `Operation not permitted`). |
| Real keybindings | `ghostty +list-keybinds` | `super` = Command. Custom: `super+ctrl+f` float on top, `super+e` equalize, `super+alt+arrows` move between splits. |
| Legacy Raycast G4/G8 grids | `~/bin/raycast/g8.sh` → `~/bin/ghostty-8pane` (and `-4pane`) → `open -na Ghostty --args --window-save-state=never --initial-command="$HOME/bin/ghostty-8pane-internal"` | The internal helper runs the AppleScript splits from inside Ghostty, then `exec "${SHELL:-/bin/zsh}" -l`. |

## 2. Rules for every job

- **RAM leak (1.3.1)**: a single high-churn agent pane can drive the shared Ghostty process to 100 GB+ and freeze or reboot the Mac, while other panes are innocent. Screenshots made it worse early on but are not required (text-only session `59c366b9` reproduced it). No terminal-wide launch flag is a confirmed fix; do not add accessibility, flat-output, alternate-screen or other Claude rendering flags without Miguel's approval.
- Screenshots: cap at 1800 px (`max_dim=1800`); never `Read` Playwright `deviceScaleFactor: 2` or full-page retina captures; keep originals on disk; Playwright MCP runs with `--image-responses omit`.
- Never resume a Claude session that was active during an image-related crash: start fresh from the repo and a text-only handoff.
- If growth returns: stop that one session and capture `footprint -p $(pgrep -x ghostty)` (hundreds of 512 MB `MALLOC_LARGE_REUSABLE` regions = this bug) before changing anything global. Do not move unrelated herdr panes.
- Config: `~/.config/ghostty/config` and `~/Library/Application Support/com.mitchellh.ghostty/config` are the same inode; edit one. Keep `macos-applescript = true`, `image-storage-limit = 0` (secondary defense; does not stop the text-only leak). If TUI-only work still climbs, remove `background-blur-radius` (currently 20).
- macOS 27 (2026-09-23): 1.3.1 draws a broken tab bar with `macos-titlebar-style = tabs` (fixed on tip; v1.4 expected ~early Oct 2026 per maintainer on issue #13001). Community workaround `native` did not fix Miguel's glitch on 2026-09-23 and was reverted; config stays `tabs`. Real fix is tip or stable 1.4.

## 3. RAM leak evidence (for when a fix ships)

- It is Ghostty's Metal renderer, not herdr (~136 MB) or the browser harness. Matches upstream reports of 80-267 GB `MALLOC_LARGE_REUSABLE` leaks with Claude Code TUIs (discussions #11827, #13374). 1.3.0 fixed an older PageList leak.
- Restoring 17 agent panes stayed near 400 MB; five or more parallel herdr sessions can be healthy. `"tui": "fullscreen"` was already set during the 2026-08-31 reproduction, so it is not a fix.
- Upgrade only to a stable release that passes a local stress test (nightly is not a confirmed fix).

## 4. Troubleshooting a Raycast launch

1. Remove `System Events` / `keystroke` usage; use native `split` / `perform action`.
2. Raycast should only run `open -na Ghostty --args --window-save-state=never --initial-command=...`; the AppleScript runs inside Ghostty.
3. Verify pane counts across all windows (not just `front window`):

```bash
osascript -e 'tell application "Ghostty"
  set rows to {}
  repeat with w in windows
    set end of rows to ((id of w) & " | terminals=" & (count terminals of w))
  end repeat
  return rows
end tell'
```

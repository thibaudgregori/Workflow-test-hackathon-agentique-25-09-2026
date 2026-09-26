Here is an exhaustive, forensic motion-design breakdown of the video, engineered for pixel-perfect reconstruction on a 576x1024 (9:16) canvas.

### 1. SCENE TIMELINE
*Frame layout relies on a split-screen system. When split, Top Half (Y: 0-540) is a dark void `#141414` containing a central off-white 3D UI card. Bottom Half (Y: 540-1024) is the live-action speaker. Captions sit exactly on the horizon line at Y: 560.*

* **00:00.000 – 00:02.800 | Scene 0: Intro** (Split Screen). Central card scales in. Claude logo, "CLAUDE - FREE PLAN", "EVERYTHING $0" appear. 
* **00:02.800 – 00:04.600 | Speaker Fullscreen.** 
* **00:04.600 – 00:11.800 | Scene 1: Memory** (Split Screen). Card header "01 Memory". Settings UI block slides in. Toggle flips. Three staggered pills pop in: "preferences", "projects", "conversations".
* **00:11.800 – 00:13.200 | Speaker Fullscreen.**
* **00:13.200 – 00:18.200 | Scene 2: Web Search** (Split Screen). Card header "02 Web Search". Data sources UI slides in. Three staggered source links pop in.
* **00:18.200 – 00:20.000 | Speaker Fullscreen.**
* **00:20.000 – 00:25.000 | Scene 3: Projects** (Split Screen). Card header "03 Projects". Complex Project UI mockup (image asset) slides up.
* **00:25.000 – 00:27.200 | Speaker Fullscreen.**
* **00:27.200 – 00:32.000 | Scene 4: Extended Thinking** (Split Screen). Card header "04 Extended Thinking". Dark UI block slides in. 3 bullet points type out sequentially. Green checkmark pill pops in.
* **00:32.000 – 00:33.400 | Speaker Fullscreen.**
* **00:33.400 – 00:40.400 | Scene 5: Connectors** (Split Screen). Card header "05 Connectors". Chat UI block slides in. Google, Microsoft, Slack, and Notion app icons pop in sequentially next to a `+` button. Toggles appear.
* **00:40.400 – 00:47.400 | Scene 6: Outro Models** (Split Screen). Claude logo centered. "Sonnet 4.6" pill pops in. "Opus" pill pops in. Text "one of the BEST AI models available right now" fades in below.
* **00:47.400 – 00:50.000 | Speaker Fullscreen / Call to Action.** Massive glitch "FREE" text flashes over the video at 00:48.400.

### 2. TYPOGRAPHY
* **Brand Serif (Claude UI & Headers):** *Reckless* or *Ogg* (Editorial Serif). Used for Claude logo, Feature titles (Bold, Hex: `#1E1E1E`), "EVERYTHING" (Uppercase, Bold). 
* **Number Accents:** Same Serif, but Italic, Heavy weight. Used for "01" through "05", and "$0". Color: `#D97757`.
* **Micro/UI Copy:** *Inter* or *Roboto* (Clean Sans-Serif). Used for "CLAUDE - FREE PLAN" (Tracking +250, Uppercase, 12px relative to 576w), UI button text, bullet points.
* **Captions:** *Proxima Nova* or *Montserrat* (Bold Sans-Serif). White, tightly tracked, sentence case (no ending punctuation unless a comma/period concludes a full thought).
* **Glitch "FREE":** *Impact* or heavy *Helvetica Black*. All caps, max weight, stretched vertically by ~110%.

### 3. COLOR PALETTE
* **Canvas Dark Void:** `#141414` (Deep charcoal, top half background)
* **Main UI Card:** `#F9F8F6` (Warm off-white)
* **Text Dark:** `#1E1E1E` (Near black for readability)
* **Claude Orange Accent:** `#D97757` (Used for asterisks, numbers, "$0", and the word "BEST")
* **Caption Background:** `#7E57C2` (Vibrant purple)
* **Caption Text:** `#FFFFFF` (Pure white)
* **Dark UI Element (Thinking Box):** `#1A1A1A`
* **Success Green:** `#6A9B75` (Checkmark and pill border)
* **UI Pill Background (Gray):** `#EAE8E3`

### 4. ANIMATION FORENSICS
* **Main UI Card Container:** Starts at Y: 300 (anchor center). Width: 480px, Height: ~440px. Corner radius: 16px. 
  * *Entrance (00:00.000):* Scale 0% -> 100%. Duration: 600ms. Easing: Spring (Overshoot 1.1x, low friction).
* **Headers ("01 Memory"):**
  * *Entrance:* Y-position translation (slides up 30px) + Opacity (0% to 100%). Duration: 400ms. Easing: Cubic Out `(0.16, 1, 0.3, 1)`. Number and Title animate simultaneously.
* **Nested UI Blocks (Settings, Chat Mockups):**
  * *Entrance:* Slides up 50px into position, fades opacity 0->100. Duration: 500ms. Easing: Smooth Ease-Out.
* **UI Micro-Interactions:**
  * *Toggles (e.g., 00:07.600):* Circle translates X by 20px over 150ms. Background fades gray to pale yellow/blue.
  * *Pills/Tags (e.g., "preferences", "source 1"):* Pop-in animation. Scale 80% -> 100%, Opacity 0->100. Duration: 250ms with slight spring. Staggered by 150ms per pill.
  * *Typing (00:28.400):* Bullet points fade in instantly block-by-block, simulating LLM generation speed. 
* **Outro Glitch "FREE" (00:48.400):**
  * Spans 90% of screen width. Hard cut in. Has chromatic aberration: Red channel shifted -10px X, Cyan channel shifted +10px X. Holds for 600ms, flickering opacity by 10% on every frame, then hard cut out.

### 5. CAPTIONS
* **Style:** Solid background box (`#7E57C2`) with 8px corner radius. Padding is 10px Top/Bottom, 16px Left/Right. Text is pure white, no drop shadow.
* **Position:** Fixed horizontally centered. Vertical anchor at Y: 560 (straddling the line between the top graphics and bottom video).
* **Animation:** Zero motion. Hard cuts only. Text updates in chunks of 2-4 words, perfectly synced to the voiceover transients.
* **Timing Map Examples:**
  * 00:00.000: "Claude just gave away"
  * 00:01.000: "almost everything"
  * 00:02.000: "for free,"
  * *Note: The caption box dynamically resizes horizontally to wrap the exact width of the current text chunk, but the height remains fixed.*

### 6. TRANSITIONS
* **Split to Fullscreen (and vice versa):** 0ms hard cuts. No wipes, no crossfades.
* When cutting back to the Split Screen (e.g., 00:04.600), the central UI Card `#F9F8F6` is *already present* at 100% scale. Only the internal contents (Numbers, Text, Mockups) animate in. The initial card pop only happens at 00:00.000.
* The speaker video simply changes scale/position instantly on the cuts (from filling the 576x1024 canvas to being cropped into the Y:540-1024 lower region).

### 7. AUDIO
* **Music:** Lo-fi jazzy hip-hop beat. Approx 85 BPM. Muted Rhodes chords, laid-back snare. Ducked by -15dB under the voiceover.
* **Voiceover:** Aggressively edited ("jump cut" style). Zero breaths. Dead air between phrases is removed to maintain a relentless, high-retention TikTok pace.
* **Sound Effects (Crucial for impact):**
  * *Low Whoosh:* Plays at 00:00.000 on main card pop.
  * *High-pitched Pop/Click:* Plays whenever a text pill or source link appears (e.g., 00:08.800, 00:16.400, 00:41.400).
  * *Digital Click:* Plays exactly when UI toggle switches flip (00:07.600).
  * *Success Ding:* Soft chime plays when the green "reasoned" checkmark appears at 00:30.800.

### 8. LAYOUT SYSTEM
* **Safe Areas:** Top 100px and bottom 150px are left visually empty of critical text to account for TikTok/Shorts platform UI overlays (likes, comments, profile pic).
* **Main Card Margins:** X: 48px left and right. This leaves exactly a 480px width for the card on the 576px canvas.
* **Hierarchy:** The live-action video is on the bottom layer (Z=0). The top-half dark void and card are on Z=1. The Captions are on the absolute top layer (Z=2) to overlap the seam between the two visual zones.

### 9. PACING RULES
* The graphics are purely reactive to the audio. An animation *never* anticipates the speaker. The moment the speaker pronounces the first syllable of a feature (e.g., "Mem-" in Memory at 00:05.000), the corresponding visual text slides up. 
* Internal UI elements (like toggle switches flipping or bullet points appearing) are delayed by 500-800ms *after* the initial section title appears, ensuring the viewer's eye reads the header first, then drops down to watch the UI interaction.
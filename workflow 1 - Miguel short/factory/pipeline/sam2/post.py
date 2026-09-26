"""Spatial cleanup + the sub-pixel trim polish + the cream die-cut rim.

Vendored, deliberately, out of two lab files so this package has NO import path
back into the format lab (archived on Drive under Testing & Experiments):

  `keep_largest`, `fill_holes`   <- `_shared/matte_bakeoff/mb_post.py`
  `denub` .. `rim_alpha`         <- `_shared/sam2/sam2_smooth.py`
  `border_bleed`                 <- `_shared/sam2/frame0fix/ship.py`
  `roughness`                    <- `_shared/sam2/sam2_smooth.py`

PARAMETERS ARE FROZEN.  UP 2 / SIGMA_HI 4.0 / MORPH_K 2 / FEATHER 0.55 / rim
7 px dilated in 2x space / cream #FFFDF9 are the values Miguel approved on the
round-6 DEFINITIVE cutout.  They are not knobs; changing one changes the look of
every cutout short ever made and invalidates `cutout*_envelope.json`.

WHY THE S-CURVE IS NOT HERE.  Rounds 1 and 2 ran BiRefNet per frame and their
dominant failure was not "chair kept" but "chair kept at alpha 0.2-0.6" — a
translucent smear, uglier than a hard mistake — so a steep S-curve forced every
pixel to commit.  SAM2 emits calibrated logits; the equivalent is a straight
sigmoid > 0.5.  (Its INTERIOR does carry a dithered 0.6-0.95 texture from
upsampling the low-res mask, which is why the alpha is binary-cored and soft
only at the boundary.)

WHY THE CHAIR EXCLUSION MASK IS NOT HERE.  Round 2 subtracted a static 58,499 px
region from every frame.  His hand goes there: on the worst sampled frames the
region was eating 1,328-2,372 px that the plate's own colour says is 92-100 %
skin, against at most 191 px of genuine chair.  A prompted negative costs
nothing and does not amputate anything.  (`_shared/SAM2.md` §6.)
"""
from __future__ import annotations

import cv2
import numpy as np

UP = 2                 # supersample factor for the sub-pixel threshold
SIGMA_HI = 4.0         # Gaussian sigma in 2x pixels == 2.0 native px
MORPH_K = 2            # native-resolution open/close radius, px
FEATHER = 0.55         # final Gaussian on the 1x alpha, px
RIM_PX = 7             # cream die-cut rim, native px
CREAM_BGR = (249, 253, 255)      # #FFFDF9
BLEED = 8              # border bleed, px, on three edges


# --------------------------------------------------------------- spatial
def keep_largest(m):
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), 8)
    if n <= 2:
        return m
    k = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    return lab == k


def fill_holes(m):
    """Fill interior holes only.

    Border-safe: flooding from (0,0) alone would misclassify any background
    pocket enclosed between the subject and a frame edge (e.g. under a raised
    arm against the left border) as an interior hole and fill it with chair.
    Padding a 1 px background ring first guarantees every border-touching
    background region is reached from the single seed.
    """
    h, w = m.shape
    inv = (~m).astype(np.uint8) * 255
    pad = np.zeros((h + 2, w + 2), np.uint8)
    pad[1:-1, 1:-1] = inv
    pad[0, :] = pad[-1, :] = pad[:, 0] = pad[:, -1] = 255
    ff = np.zeros((h + 4, w + 4), np.uint8)
    cv2.floodFill(pad, ff, (0, 0), 0)
    return m | (pad[1:-1, 1:-1] > 0)


def border_bleed(b, k=BLEED):
    """The outer k px of LEFT, RIGHT and BOTTOM inherit the nearest interior line.

    SAM2 attenuates its mask into the frame border; BiRefNet does not.  Measured
    on the hermesinfinite plate, ON pixels on row 899: BiRefNet 1072, SAM2 raw 0.
    His chest genuinely runs off the bottom of the plate, so a mask that fades
    out over the last five rows is an upsampling artifact, not a statement about
    the subject.  Left alone it opens a transparent strip under him AND the 7 px
    rim then draws a cream line across the bottom, turning the die-cut into a
    floating sticker.

    Where the interior line is OFF — which is most of the left and right edge —
    the OR changes nothing, so this cannot invent subject anywhere.  Measured
    cost on frame 0: +3,636 px, all inside y in [858, 899].

    The TOP edge is deliberately excluded: his cap sits mid-frame and must stay
    honest.
    """
    b = b.copy()
    b[:, :k] |= b[:, k:k + 1]
    b[:, -k:] |= b[:, -k - 1:-k]
    b[-k:, :] |= b[-k - 1:-k, :]
    return b


def spatial(gray):
    """Raw SAM2 alpha frame (uint8) -> cleaned float32 binary."""
    b = gray > 127
    b = fill_holes(keep_largest(b))
    return border_bleed(b).astype(np.float32)


# ------------------------------------------------------------- trim polish
def ell(k):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * k + 1, 2 * k + 1))


def denub(b, k=MORPH_K):
    """Open then close: drop nubs smaller than k, fill notches smaller than k.

    Blur+threshold alone leaves isolated 1 px nubs and 1-2 px notches (they
    survive because they are locally more than half the window), and those are
    exactly what reads as noise.
    """
    if k <= 0:
        return b
    u = b.astype(np.uint8)
    u = cv2.morphologyEx(u, cv2.MORPH_OPEN, ell(k))
    u = cv2.morphologyEx(u, cv2.MORPH_CLOSE, ell(k))
    return u > 0


def smooth_binary(b, sigma_hi=SIGMA_HI, up=UP):
    """bool mask -> bool mask, contour low-passed on a HALF-PIXEL lattice.

    Upsampling before the blur is what makes it sub-pixel: thresholding at 2x
    places the boundary on a half-pixel lattice, and INTER_AREA back to 1x turns
    that into a genuine 1 px anti-aliased edge (levels 0, .25, .5, .75, 1)
    instead of a blurred hard one.
    """
    h, w = b.shape
    u = cv2.resize(b.astype(np.float32), (w * up, h * up),
                   interpolation=cv2.INTER_NEAREST)
    u = cv2.GaussianBlur(u, (0, 0), sigma_hi)
    return u > 0.5


def to_alpha(b_hi, shape, feather=FEATHER):
    h, w = shape
    a = cv2.resize(b_hi.astype(np.float32), (w, h),
                   interpolation=cv2.INTER_AREA)
    if feather > 0:
        a = cv2.GaussianBlur(a, (0, 0), feather)
    return np.clip(a, 0, 1)


def polish(b, sigma_hi=SIGMA_HI, morph_k=MORPH_K, feather=FEATHER, up=UP):
    """The approved edge treatment.  Returns (alpha_1x, smoothed_hi_binary).

    SIGMA_HI was chosen by eye at 10x on the brim notch, the ear and the
    shoulder over frames 400 and 1100: at 2.0 the stairs are still legible, at
    3.0 faint, at 4.0 gone WITH THE BRIM NOTCH STILL A SQUARE CORNER, at 5.0 the
    notch begins to bevel, at 6.0 it is a blob.  Miguel is bald, so there is no
    fine organic texture on this trim to protect and the smoothing can be harder
    than a haired subject would allow; the two features that DID constrain sigma
    are the cap brim corner (a real hard corner) and the ear contour, and both
    survive at 4.0.  Bounded cost, measured: the largest connected group of
    pixels that changes anywhere in the frame is 9 px in a 5x3 box.
    """
    b = denub(b, morph_k)
    hi = smooth_binary(b, sigma_hi, up)
    return to_alpha(hi, b.shape, feather), hi


def rim_alpha(hi, shape, rim_px=RIM_PX, sigma_hi=SIGMA_HI, up=UP,
              feather=FEATHER):
    """The cream rim, dilated FROM the smoothed silhouette, in 2x space.

    v1 dilated the 1x float alpha with an ellipse kernel, so the rim inherited
    both the staircase and the kernel's own facets — a smooth silhouette with a
    stepped rim would have been pointless.  Doing it at 2x and running the same
    low-pass afterwards gives a rim whose outline is as smooth as the silhouette
    it offsets.
    """
    d = cv2.dilate(hi.astype(np.uint8), ell(rim_px * up)) > 0
    d = cv2.GaussianBlur(d.astype(np.float32), (0, 0), sigma_hi) > 0.5
    return to_alpha(d, shape, feather)


# ----------------------------------------------------------------- metric
# the head: cap crown to jaw, both ears.  Reported separately because torso and
# shoulders are black-on-white and SAM2 already cut them cleanly, so a
# whole-contour average is dominated by runs that were never the complaint.
HEAD_BOX = (270, 140, 810, 620)


def roughness(alpha, win=9, region=None, sub=4):
    """How far the trim sits from a locally smooth version of itself, px.

    MEASURED ON THE ALPHA, never on a thresholded copy.  That distinction is the
    whole measurement: the gain is sub-pixel, so re-quantising to whole pixels
    before measuring throws away exactly what is being tested — doing it the
    wrong way once reported -12.8 % for a change that is unmissable at 10x.

    So the iso-0.5 line is recovered at `sub`x with a bicubic resample and the
    coordinates divided back down.  Then walk it, run a `win`-tap circular
    moving average, and report the mean distance from each point to its own
    smoothed position.  A whole-pixel staircase sits far off its local mean; a
    genuine curve sits close to it.  Scale-free, orientation-free, and it does
    not reward simply making the silhouette smaller.

    Perimeter was tried first and rejected: an 8-connected staircase and a
    45-degree line have nearly the same arc length, so it moved 1 % for a change
    that moves this metric by more than a third.
    """
    a = alpha.astype(np.float32)
    h, w = a.shape
    big = cv2.resize(a, (w * sub, h * sub), interpolation=cv2.INTER_CUBIC)
    c, _ = cv2.findContours((big > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
    if not c:
        return float("nan"), 0
    c = max(c, key=cv2.contourArea).squeeze().astype(np.float64) / sub
    keep = None
    if region:
        x0, y0, x1, y1 = region
        keep = ((c[:, 0] >= x0) & (c[:, 0] < x1) &
                (c[:, 1] >= y0) & (c[:, 1] < y1))
    k = np.ones(win) / win
    pad = np.vstack([c[-win:], c, c[:win]])
    sm = np.stack([np.convolve(pad[:, i], k, mode="same") for i in (0, 1)], 1)
    sm = sm[win:-win]
    dev = np.hypot(*(c - sm).T)
    if keep is not None:
        dev, c = dev[keep], c[keep]
    return float(dev.mean()), len(c)

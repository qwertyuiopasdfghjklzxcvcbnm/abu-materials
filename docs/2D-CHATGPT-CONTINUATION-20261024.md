# 2D material review — Claude to ChatGPT continuation (2026-10-24)

## Original/source work

- Remote: `qwertyuiopasdfghjklzxcvcbnm/abu-materials`
- Pulled from: `claude/abu-2d-skill` at `f668ccacd8390fc8785483b9a419fd33bb54a64e`
- Continued on **local-only** branch: `chatgpt/abu-2d-continuation`
- Source original JPG archive (not checked into Git): `restored/2D-media.zip`
- Source archive SHA256: `161cce2c4419b9a8a57b9da9e16d286d45dab1cb767880ca3721299cd4170b67`
- Original zip release: `abu-2d-source-20261023`

## State of review

- Claude branch had sealed B01–B08 / **1–512**; those are retained, not visually re-reviewed.
- ChatGPT with Chat On Steroids Core.view_image *individually* opened the original full-resolution JPG files and recorded **B09 / 513–576**, all 64 files. The entries show `session='ChatGPT COS continuation 2026-10-24'` and the actual tool used; batch groups G0065 through G0081.
- Batch B09 sealed via `tools/checkpoint.py B09`. Sealed B09 SHA256: `aae258608c3acbf84056331390461817bbaa0b0d7f485fb14aaae5e5572255ce`.
- ChatGPT additionally **individually opened all B10 / 577–640** full-original JPEGs and recorded observations in groups G0082 through G0097, without redoing prior sealed batches. Batch B10 sealed via `tools/checkpoint.py B10`, SHA256 `297a96a567a0fc507ca77a64ce1bc741d391e36a7a16e179dd607dda2f1133c8`.
- ChatGPT subsequently **individually opened all B11 / 641–704** full-original JPEGs, writing independent per-image observations in groups G0098 through G0113. Batch B11 sealed via `tools/checkpoint.py B11`, SHA256 `a26c7d0995360be842c2c13c332fdc6788ca901dbcbbbb53f9487091e6ba85d2`.
- Total structurally closed: **704/3281**, 11/51 batches. Next unreviewed image is **705** (B12 = 705–768).
- Verified with `py -3 tools/validate.py --check-media`: PASS; 704/704 record-to-inventory checks, all relevant original JPG SHA256s (directly extracted or from the media ZIP), sealed-batch hashes, and linked ledger.
- The validator *does not* prove an image was actually looked at. For B09–B11 individual full-JPG view calls were actually made and recorded; for original Claude's B01–B08 only structural/provenance checks were done here.

## Observed source content and epistemic notes

All B09 frames are from slide 9, `Market Inertia: 80% Chance of More of the Same Behavior`, featuring a strongly declining candlestick path, a late price floor and partial bullish retracement. Three bullets emphasize that recent trend behavior is predictive context, not merely the shape of an individual candlestick.

Frame 529 begins a new red overlaid explanatory sentence, `Bear trend, so lower prices more likely than higher prices`, which becomes strong red by frame 532. The presenter blue halo in most frames moves from post-low rally bars backwards to earlier bear-trend bars and the first sideways consolidation. New entries record specific visible pointer positions and distinguish overlays from actual chart bars. They do **not** infer trading performance, a guaranteed 80% measured conditional frequency, or a price reversal entry setup from these stills alone.

B10 starts on the same Slide 9; frame 581 adds a green caution `Don't look to buy minor reversals`. Frames 586–590 crossfade into Slide 10 `Inertia In Trends: 80% Rule` (yellow text `80% Rule`). Its left statement becomes fully legible: `In trends, 80% of reversals fail`. Frames 596–605 progressively overlay the red line `Minor reversals become bear flags` and **four distinct pink/red rectangular areas** marking attempted countertrend reversals in the existing bear trend. Later frames show the blue speaker pointer moving around these annotations and the preceding/downstream bear bars. These frames provide qualitative teaching examples, not independently measured reversal failure rates. The red shapes are after-the-fact illustrative overlays, not evidence they were visible live before a trade.

B11 contains Slide 10 throughout. The presenter blue pointer travels backward and forward among the four already red-boxed small bounce attempts and subsequent black bearish continuation candles; the screen's bars and red flags are static, not new price ticks. Frame 686 and 703 have no blue cursor. Frame 704 introduces a faint **green** new overlay near the late low: `Bulls finally` is legible as the opening, but the remainder is not yet sufficiently clear; a pale-green short mark and upward-diagonal arrow also begin fading in below the low-to-rebound region. **Next B12 must read subsequent original images to transcribe this newly introduced text**, rather than guessing from the first fade-in frame.

## How to continue

1. Open `docs/2D-METHOD.md` and `tools/review_lib.py` before recording.
2. Run `py -3 tools/extract_batch.py B12`; it extracts/verifies 64 JPGs in `restored/zip/高清原始分辨率/`.
3. Use `Core.view_image` for **each** full JPG in ascending order, record specific visually grounded changes with `tools/record.py`, setting session and read_via correctly; do not call `record.py` before the actual image is opened.
4. Once every 705–768 record exists, run `py -3 tools/checkpoint.py B12` (only once); then `py -3 tools/validate.py --check-media`.
5. Keep the same independent local continuation branch unless explicitly asked to push elsewhere. Do not overwrite Claude's branch, original media, or completed existing B batches.

## Restrictions and notices

- No final 2D Skill has been produced from this incomplete review; 2577 stills remain.
- The GitHub repository appears **public** even though the README says private/plan-only, and its media ZIP is accessible from its public release. Treat public exposure as a separate issue to be addressed if intended to be confidential.
- `restored/` contains a large original ZIP, extracted JPGs, and transient group input JSONL files, deliberately ignored by Git and not published. The durable Git-tracked evidence consists of B09–B11 JSONL, progress and ledger plus scripts and this note.

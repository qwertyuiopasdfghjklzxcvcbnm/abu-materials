# 2D per-image review protocol

How the evidence under `evidence/2D/` was produced, and how to resume or audit it.

## 1. Sources and integrity

| Item | Value | How it was checked |
|---|---|---|
| Release | `abu-2d-source-20261023` | GitHub API: both assets `state=uploaded` |
| `2D.mp4` | 145,568,572 B, SHA256 `dc13f6af…8d29` | local `sha256sum` = README = API digest |
| `2D-media.zip` | 479,930,912 B, SHA256 `161cce2c…0b67` | local `sha256sum` = README = API digest = `frames/2D-media.zip.sha256` |
| Video | 1920×1080 H.264, 30 fps, 1711.33 s, 51,338 frames | `ffprobe` (`inventory/video_probe.json`) |
| ZIP | 3281 JPG = 3229 keyframes + 48 exact video frames + 4 contact sheets | `tools/build_inventory.py` |
| Subtitles | 498 EN + 498 ZH cues, identical timings | full read; see `subtitles/` |

The media live in `restored/` (gitignored) and are never committed. `inventory/zip_manifest.jsonl` holds one row per JPG with its SHA256, bytes, pixel size, kind, keyframe id/time (`course-audit/kept_manifest.json`) and active subtitle cue indices. All 36 `preview-frames/` samples match the ZIP byte for byte. 10 keyframes are byte-identical to one of the exact video frames. Both copies are still reviewed separately.

Timestamp check (`tools/verify_timestamps.py` → `inventory/timestamp_check.json`): 164 keyframes (every 25th id plus the 36 samples) and all 48 exact frames were decoded from the video at their recorded time and compared after 160×90 grayscale downscaling. All 164 keyframes match best at their recorded time (mean absolute difference: median 0.058, max 0.978 on a 0–255 scale). The 48 exact frames have a maximum difference of 0.18.

## 2. Review order and batches

Images are reviewed in manifest `seq` order:
- seq 1–3229: keyframes `frame_000001…003229` (video order)
- seq 3230–3277: 48 exact frames (time order)
- seq 3278–3281: 4 contact sheets

Batches B01–B50 hold 64 images each and B51 holds the last 81, so every batch is within 50–100 images. A batch is closed with `tools/checkpoint.py`, then committed and pushed to `claude/abu-2d-skill`.

## 3. Per-image procedure

1. **Open the original.** Open `restored/zip/<path>` with the Read tool: the full original JPG, one Read call per image. Never use thumbnails, contact sheets made for the purpose, video summaries or subtitle search as a substitute. Up to 8 consecutive images are opened in one step (a *view group*).
2. **Record before moving on.** The records for a view group are written with `tools/record.py --group Gnnnn` in the same step that opens the next group. Each record is therefore composed before the next images are seen. `read: true` is written only by `record.py`, only for images in the group just viewed. The script refuses gaps, repeats and out-of-order images.
3. **Zoom when needed.** If bar labels, small text or thin lines cannot be read at the size the Read tool shows, cut a native-resolution crop with `tools/crop.py` (written to the scratchpad, not the repo) and open it. Record the box under `crop`.
4. **Let scripts fill the facts.** SHA256, bytes, pixel size, timestamp, cue indices, batch and UTC record time are added by `record.py`, never typed by hand.

### Hand-written keys (input to `record.py`)

| Key | Meaning |
|---|---|
| `f` | file name (required) |
| `sc` | scene: `title`, `chart`, `chart_ind` (chart with indicators), `line_chart`, `ad`, `text`, `blank`, `transition`, `contact_sheet`, `other` |
| `ch` | chart id `Cnn`, required for chart scenes. Same price bars keep the same id; different bars get a new id, numbered in order of first appearance |
| `see` | what is visible. On the first frame of a chart, give checkable details (title/symbol/timeframe text, price-axis labels). On later frames, say what changed versus the previous frame |
| `mk` | counts of annotations visible in this frame (on-screen state, not just new marks), e.g. `{"blue_line": 2, "blue_circle": 1}`. Allowed keys are in `tools/review_lib.py`. `pointer` is the presenter's small blue ring cursor, not a drawn mark. Lines that are part of the charting software (moving average, prior-high step lines) are described in `see`, not counted |
| `bars` | bar labels or numbers readable on the chart |
| `fail` | the frame shows a failed setup or counter-example (what failed, where) |
| `pp` | `{"ref": bar/area, "pre": what was knowable at the reference bar using only bars to its left, "post": what followed}` |
| `cf` | confidence `h`/`m`/`l` |
| `flag` | reason a human should look (ambiguous, unreadable, conflicts with the subtitles) |
| `crop` | list of `[x, y, w, h]` boxes that were opened |
| `rev` | revision note if a record supersedes an earlier one |

`see`, `mk` and `bars` hold only what is in the pixels. `fail` and `pp` are interpretations and may use the lecture; the cue indices that `record.py` attaches tie them to what was said at that moment.

## 4. Honesty rules

- An image counts as reviewed only if it was opened with Read in this process. Coverage is measured from the batch files, never assumed.
- The subtitles were read in full **before** the image review started, so no "blind" image-first pass is claimed. The separation is enforced by keys instead: visual keys versus interpretation keys.
- The audio was not listened to. Spoken content comes from the EN subtitle file, and translation issues are in `subtitles/term_audit.jsonl`.
- The 4 contact sheets are reviewed as images, but they are never used as evidence for any single frame.

## 5. Resume and audit

- **Resume:** read `frames/progress.json` (`next_seq`, `next_file`). Check that `ledger.jsonl` ends at the batch before. Continue with `record.py`, and close each batch with `checkpoint.py`.
- **Audit:** `python3 tools/validate.py` re-checks coverage (3281 records, once each), SHA256 against the files, the ledger hash chain and the record schema.

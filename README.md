# Abu 2D original material — plan only (private)

This is a newly created private repository containing one course, Abu 2D. The previous materials repository has been deleted. No earlier Git history is reused.

**Current authorization is planning only. Claude Code must NOT create or modify any Skill, run media extraction, or commit any changes without a new user instruction.**

Included:

- source-original/2D-en.srt and source-original/2D-ch.srt: full English and Chinese course subtitles
- course-audit/: existing 2D still-frame index, reports and metadata
- assets/manifest.json: SHA256 and part list for original full 2D.mp4 and image-only 2D-media.zip
- assets/2D-original-video/part-*.bin: exact-byte lossless parts of complete original video
- assets/2D-hd-frames/part-*.bin: exact-byte lossless parts of high-definition original JPG archive
- restore_2d_assets.py: verifies all part SHA256s and reassembles into restored/2D.mp4 and restored/2D-media.zip
- PLAN_ONLY_CLAUDE.md: request for a design/verification plan, with no execution

Binary parts are stored directly in Git, NOT Git LFS. Each part is no larger than 32 MiB. After explicit user authorization, Python 3.12+ can reconstruct the byte-for-byte original MP4 and image-only ZIP using restore_2d_assets.py. This is not recomposing clips; it is restoring the original MP4 exactly.

Always use the highest available model and thinking capability to discuss an evidence-based plan first, then wait for approval.
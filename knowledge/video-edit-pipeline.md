# Local video edit pipeline (talking-head, fast-cut style)

Turns a raw selfie-style vlog into a captioned, punched-in, jump-cut edit with a hook card, chapter cards and animated cutaways, using only local tools. Script: `tools/build_edit.py`.

## Tools
- **ffmpeg** with `ass`/`subtitles` filters and the platform hardware encoder (`h264_videotoolbox` on macOS). Note: some static ffmpeg builds ship a broken `drawtext`; use ASS subtitles for all text.
- **whisper.cpp** (`brew install whisper-cpp`) with `ggml-small.en.bin` for transcription. `-ml 1 -sow` gives one word per segment, but the words are stamped back to back: pauses are not in the transcript.
- **Pauses** come from `silencedetect` on the audio (noise −30 dB, minimum 0.25 s). A continuous talker yields about 5% removable air; the pace comes from the cuts themselves, the zoom changes and the captions, not from shortening.
- **Scene changes**: `-hwaccel` decode, `fps=2`, `select=gt(scene,0.45)`. Software decode of 1080p60 HEVC crawls.
- Fonts: Impact and Arial Black from the system supplemental fonts.

## Recipe
1. Cut every pause ≥ 0.25 s with 0.06 s lead and 0.10 s tail; drop whole-word fillers.
2. Per cut, a punch-in from a fixed pattern (1.0, 1.10, 1.0, 1.06, 1.14, 1.0, 1.08) via crop and scale, face-biased 40% from the top.
3. Captions: three words per line, uppercase, the live word yellow, the rest white, heavy outline, bottom center.
4. Hook card, first 3.8 s, centered. Chapter cards 2.4 s at scene changes.
5. Cutaways: public-domain artwork (Wikimedia Commons API, filter by license) with a slow push-in, the source line fading in, a credit in the corner; overlaid with alpha fades at the spoken line; the speaker's audio continues.
6. Encode segments at 12 Mbps, concat, burn captions and overlays at 14 Mbps.

## What needs the user
Music and sound effects (no local assets), a content trim that removes their own words, and any paid AI clip generation (check the API key answers before promising it).

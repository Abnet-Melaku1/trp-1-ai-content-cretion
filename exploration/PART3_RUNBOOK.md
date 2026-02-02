# Part 3: Content Generation — Runbook

Use these commands from the **project root** (where `pyproject.toml` is).  
**Note:** The CLI requires `--prompt` even when using `--style`; when you pass both, the preset’s prompt is used for generation. Use a short placeholder like `"jazz"` or the preset name for `--prompt` when using `--style`.

---

## 3.1 Instrumental music (Audio #1)

**Using preset (jazz):**
```bash
uv run ai-content music --prompt "jazz" --style jazz --provider lyria --duration 30
```

**Or custom prompt only:**
```bash
uv run ai-content music --prompt "Smooth jazz fusion, walking bass, brushed drums, mellow saxophone" --provider lyria --duration 30 --bpm 95
```

- Note the **output path** printed when it succeeds (e.g. under `output/music/`).
- Confirm the file exists and plays. This is **audio file #1**.

---

## 3.2 Second audio (Audio #2) — different style or provider

**Option A — Different preset, same provider (Lyria):**
```bash
uv run ai-content music --prompt "ambient" --style ambient --provider lyria --duration 30
```

**Option B — MiniMax (if you have AIMLAPI key):**
```bash
uv run ai-content music --prompt "Lo-fi hip-hop, chill study beats" --provider minimax --duration 30
```

- Note output path. This is **audio file #2**.

---

## 3.3 Music with vocals (optional — AIMLAPI only)

1. Create a lyrics file, e.g. `my_lyrics.txt`:
   ```
   [Verse]
   Walking through the rain, thinking of your name...

   [Chorus]
   Every day I miss you more...
   ```

2. Run:
   ```bash
   uv run ai-content music --prompt "Lo-fi R&B, emotional and smooth" --provider minimax --lyrics my_lyrics.txt --duration 30
   ```

3. MiniMax may return a job ID; use `uv run ai-content music-status <id> --output path/to/save.mp3` to poll and download when ready.

---

## 3.4 Video (Video #1)

**Using preset (nature):**
```bash
uv run ai-content video --prompt "nature" --style nature --provider veo --duration 5
```

**Or custom prompt:**
```bash
uv run ai-content video --prompt "A lion walking through savanna grass at golden hour, cinematic" --provider veo --aspect 16:9 --duration 5
```

- Note output path (e.g. under `output/video/`). This is **video file #1**.

---

## 3.5 Bonus: Combine into music video (FFmpeg)

1. Install FFmpeg if needed; ensure it’s on your PATH.
2. Replace paths below with your actual **video file** and **audio file**:

   ```bash
   ffmpeg -i output/video/your_video.mp4 -i output/music/your_music.wav -c:v copy -c:a aac -shortest output/music_video.mp4
   ```

3. Confirm `output/music_video.mp4` plays. This is your **combined music video**.

---

## 3.6 Generation log (for SUBMISSION.md)

Fill in `exploration/GENERATION_LOG.md` (or copy into SUBMISSION.md) with:

- Exact command for each generation
- Prompt (or preset name) used and why
- Output file path, size, duration
- Any errors and how you fixed them

You can use the template in `exploration/GENERATION_LOG.md` if you created it.

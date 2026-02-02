# TRP 1 - AI Content Generation Challenge — Submission

**Candidate:** [Your Name]  
**Date:** [Submission Date]

---

## 1. Environment Setup Documentation

**APIs configured:**
- **Google Gemini** (`GEMINI_API_KEY`) — used for Lyria (music) and Veo (video). Note: I had to use my friend’s credit card to enable/billing for the Gemini API.
- **AIMLAPI** (`AIMLAPI_KEY`) — optional, for MiniMax music with vocals.
- **Kling** (`KLINGAI_API_KEY`, `KLINGAI_SECRET_KEY`) — optional; used when Veo had issues. Note: nested settings don’t load from `.env`; credentials must be in the shell environment (e.g. `export KLINGAI_API_KEY=...` then run the command).

**Issues during setup:**
- CLI requires `--prompt` even when using `--style`; use a short placeholder (e.g. `"jazz"`) when using presets.
- Kling: auth failed when keys were only in `.env`; nested `KlingSettings` does not load from `.env`; fixed by exporting vars before running.

**How resolved:**
- Used `uv run ai-content music --prompt "jazz" --style jazz --provider lyria --duration 30` (and similar for video).
- For Kling: ran from project root after `export KLINGAI_API_KEY=...` and `export KLINGAI_SECRET_KEY=...`.

---

## 2. Codebase Understanding

- **Architecture:** See `exploration/ARCHITECTURE.md` for package structure, provider registry, and pipeline roles.
- **Provider system:** See `exploration/PROVIDERS.md`. Music: Lyria (instrumental, realtime), MiniMax (vocals/lyrics). Video: Veo (Gemini), Kling (direct API). Registration via `@ProviderRegistry.register_*`; CLI and pipelines use `ProviderRegistry.get_*()`.
- **Pipeline orchestration:** `pipelines/base` defines `PipelineResult` and `PipelineConfig`; `MusicPipeline` and `VideoPipeline` orchestrate presets + providers; `FullContentPipeline` runs music → image → video → merge (e.g. FFmpeg) with optional upload.

---

## 3. Generation Log

**Audio #1 (instrumental):**
- Command: `uv run ai-content music --prompt "jazz" --style jazz --provider lyria --duration 30`
- Prompt/preset: jazz
- Provider: lyria
- Output: `exports/lyria_20260202_123656.wav` (5.13 MB, 30s)

**Audio #2:**
- Command: [e.g. `uv run ai-content music --prompt "lofi" --style lofi --provider lyria --duration 30`]
- Output: [your second audio file path and size/duration]

**Video #1:**
- Command: [e.g. `uv run ai-content video --prompt "nature" --style nature --provider veo --duration 5` or abstract/ocean/urban if nature was RAI-filtered]
- Output: [your video file path and size/duration, or note if not generated]

**Bonus (music video):**
- [If you combined audio + video with FFmpeg, paste the command and output path.]

---

## 4. Challenges & Solutions

- **Veo API (google-genai):** Library uses `GenerateVideosConfig` and `generate_videos` (plural), not `GenerateVideoConfig` / `generate_video`. Fixed in `veo.py`. `person_generation` was rejected by the API; omitted from config.
- **Veo response:** Sometimes `video_bytes` was `None`; added fallback to `client.aio.files.download(file=video.video)` and optional URI fetch.
- **Veo “No video in response”:** Response had empty `generated_videos` with `rai_media_filtered_count` / `rai_media_filtered_reasons` — content filtered by safety policy. Tried alternative prompts (e.g. abstract, ocean, urban) to avoid RAI filter.
- **Kling:** 429 with 0 usage in dashboard — likely access/entitlement, not quota. Auth failed until keys were in shell environment (not only `.env`).
- **Lyria ambient:** One run returned 0 chunks (“No audio data received”); tried another preset (e.g. lofi/cinematic) for second audio.

---

## 5. Insights & Learnings

- Presets are strong starting points; CLI still requires `--prompt` when using `--style`, which is easy to miss.
- Provider registry pattern keeps adding providers simple; Veo/Kling differences (API shape, auth, LRO vs sync) required careful handling.
- RAI filtering can empty `generated_videos`; checking `rai_media_filtered_*` gives a clear explanation.
- Nested pydantic-settings (e.g. Kling) loading only from `os.environ` was surprising; documenting export step helps.

---

## 6. Links

- **YouTube video(s):** https://youtu.be/Z0yS4b-1wYs
- **GitHub repo:** https://github.com/Abnet-Melaku1/trp-1-ai-content-cretion

---

## Submission Checklist

- [x] `.env` configured (not committed)
- [x] `exploration/ARCHITECTURE.md`
- [x] `exploration/PROVIDERS.md`
- [x] `exploration/PRESETS.md`
- [ ] At least 2 generated audio files
- [ ] At least 1 generated video file (or documented attempt)
- [x] `SUBMISSION.md` (this file — fill in [placeholders])
- [x] YouTube link(s) in section 6
- [x] GitHub repo link in section 6

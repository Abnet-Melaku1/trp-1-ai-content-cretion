# Preset Catalog

Pre-configured prompts and settings in `src/ai_content/presets/`. The CLI and pipelines use these via `--style <name>` (e.g. `music --style jazz`, `video --style nature`). When a style is used, the preset’s prompt and BPM/aspect ratio override or supply the generation parameters.

---

## Music Presets

All presets live in `presets/music.py`. Each has: **name**, **prompt** (multi-line style description), **bpm**, **mood**, **tags**.

| Preset ID | BPM | Mood | Tags (summary) |
|-----------|-----|------|----------------|
| jazz | 95 | nostalgic | smooth, fusion, sophisticated |
| blues | 72 | soulful | delta, raw, authentic |
| ethiopian-jazz | 85 | mystical | ethio-jazz, modal, african |
| cinematic | 100 | epic | orchestral, film-score, triumphant |
| electronic | 128 | euphoric | house, edm, festival |
| ambient | 60 | peaceful | ambient, meditative, eno |
| lofi | 85 | relaxed | lofi, chill, study |
| rnb | 90 | sultry | rnb, neo-soul, modern |
| salsa | 180 | fiery | salsa, latin, cuban |
| bachata | 130 | romantic | bachata, latin, dominican |
| kizomba | 95 | sensual | kizomba, zouk, african |

**CLI:** Use with `--style <preset-id>`, e.g. `--style jazz`, `--style ethiopian-jazz`. You still need to pass `--prompt` (any placeholder) because the CLI requires it; the preset’s prompt is used for generation when style is set.

---

## Video Presets

All presets live in `presets/video.py`. Each has: **name**, **prompt** (scene description), **aspect_ratio**, **duration** (seconds), **style_keywords**.

| Preset ID | Aspect Ratio | Duration | Style keywords (summary) |
|-----------|--------------|----------|---------------------------|
| nature | 16:9 | 5 s | documentary, wildlife, golden-hour |
| urban | 21:9 | 5 s | cyberpunk, urban, neon |
| space | 16:9 | 5 s | sci-fi, space, contemplative |
| abstract | 1:1 | 5 s | abstract, commercial, satisfying |
| ocean | 16:9 | 5 s | ocean, underwater, paradise |
| fantasy | 21:9 | 5 s | fantasy, dragon, epic |
| portrait | 9:16 | 5 s | portrait, fashion, beauty |

**CLI:** Use with `--style <preset-id>`, e.g. `--style nature`, `--style portrait`. Same as music: `--prompt` is required by the CLI; the preset’s prompt is used when style is set.

---

## How to Add a New Preset

**Music:**

1. In `src/ai_content/presets/music.py`, define a new `MusicPreset` instance (name, prompt, bpm, mood, tags).
2. Add it to the list inside `MUSIC_PRESETS` (the dict built from that list). No separate “registry” file; the single dict is the registry.

**Video:**

1. In `src/ai_content/presets/video.py`, define a new `VideoPreset` instance (name, prompt, aspect_ratio, duration, style_keywords).
2. Add it to the list inside `VIDEO_PRESETS`. Same pattern as music.

**Usage:** After adding, `uv run ai-content list-presets` will show the new preset, and `--style <new-name>` will work for `music` or `video`.

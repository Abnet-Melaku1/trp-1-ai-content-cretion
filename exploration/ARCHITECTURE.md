# Codebase Architecture

Understanding of the `ai-content` package structure and how components fit together.

---

## Package Structure (`src/ai_content/`)

| Module | Purpose |
|--------|---------|
| **core/** | Protocols, registry, result types, exceptions. Defines interfaces (MusicProvider, VideoProvider, ImageProvider) and the singleton ProviderRegistry. |
| **config/** | Pydantic settings and config loading. Loads API keys and provider options from environment and YAML. |
| **providers/** | Provider implementations. Subpackages: `google/` (Lyria, Veo, Imagen), `aimlapi/` (MiniMax), `kling/` (Kling direct). |
| **presets/** | Pre-configured prompts and settings. `music.py` and `video.py` define presets; `get_preset` / `list_presets` are used by CLI and pipelines. |
| **pipelines/** | Orchestration layer. Coordinates providers and presets for multi-step workflows (music-only, video-only, or full music-video). |
| **cli/** | Typer CLI. Entry point is `main.py`; commands call pipelines or providers and print results. |
| **integrations/** | External services: archive, media handling, YouTube upload. |
| **utils/** | Helpers: file paths, lyrics parsing, retries. |

**Import flow:** `cli` → uses `pipelines` and providers via registry → `providers` and `pipelines` use `core` + `config` + `presets`.

---

## How Providers Are Organized

- **Registration:** Each provider class is registered with a decorator, e.g. `@ProviderRegistry.register_music("lyria")`, `@ProviderRegistry.register_video("veo")`, `@ProviderRegistry.register_image("imagen")`.
- **Discovery:** `ProviderRegistry.list_*_providers()` and `get_*()` return names and instances. The CLI and pipelines use these; no hardcoding of provider lists in CLI.
- **Location:** One module per provider (or per API family): `google/lyria.py`, `google/veo.py`, `google/imagen.py`, `aimlapi/minimax.py`, `kling/direct.py`. Importing `ai_content.providers` triggers registration.

---

## Purpose of `pipelines/`

- **base.py:** Defines `PipelineResult` (aggregates outputs, errors, timing) and `PipelineConfig` (paths, options). Shared by all pipelines.
- **music.py:** `MusicPipeline` — workflows like “performance-first” (instrumental then lyrics), “lyrics-first”, “reference-based” style transfer. Uses presets and `ProviderRegistry.get_music()`.
- **video.py:** `VideoPipeline` — text-to-video and image-to-video workflows. Uses presets and `ProviderRegistry.get_video()`.
- **full.py:** `FullContentPipeline` — end-to-end: music + (optional) image + video + merge (e.g. FFmpeg). Can upload to YouTube. Composes `MusicPipeline` and `VideoPipeline`.

Pipelines do not replace the CLI; they are used by examples and programmatic callers. The CLI mainly calls providers directly (with preset resolution in the command handlers).

---

## CLI Commands (Summary)

- **music** — Generate music. Requires `--prompt` (or use `--style` preset; CLI still needs a placeholder prompt; preset overrides prompt/BPM in logic). Options: `--provider`, `--style`, `--duration`, `--bpm`, `--lyrics`, `--reference-url`, `--output`, `--force`.
- **video** — Generate video. Requires `--prompt` (or use `--style` preset). Options: `--provider`, `--style`, `--aspect`, `--duration`, `--image`, `--output`.
- **list-providers** — List music, video, and image provider names.
- **list-presets** — List music and video presets with short descriptions.
- **music-status** — Check MiniMax job status by generation ID; optional `--output` to download.
- **jobs** — List tracked jobs (optional filters: `--status`, `--provider`, `--limit`).
- **jobs-stats** — Summary counts by status/provider/type.
- **jobs-sync** — Sync pending job status from API; optional `--download` for completed jobs.

---

## Key Design Points

1. **Protocols over inheritance:** Providers implement `Protocol` interfaces (`MusicProvider`, etc.) and register by name; no single base class.
2. **Result object:** Providers return `GenerationResult` (success, file_path, error, metadata) instead of raising for expected failures.
3. **Async-first:** Provider `generate()` methods are async; CLI runs them via `asyncio.run()`.
4. **Presets override prompt:** When `--style` is used, the CLI/pipeline loads the preset and uses its `prompt` (and BPM or aspect ratio); the user-supplied prompt is only required by the CLI signature when not using style-only flow.

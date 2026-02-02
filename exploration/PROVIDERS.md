# Provider Capabilities Summary

Overview of available providers and their differences, derived from `src/ai_content/providers/` and `core/provider.py`.

---

## Music Providers

| Provider | Registered as | Vocals / Lyrics | Realtime | Reference Audio | Notes |
|----------|----------------|-----------------|----------|-----------------|--------|
| **Lyria** | `lyria` | No (instrumental only) | Yes | No | Google; WebSocket streaming; BPM/temperature control. |
| **MiniMax** | `minimax` | Yes (lyrics + structure tags) | No | Yes | Via AIMLAPI; style transfer from reference URL; async polling. |

- **Lyria:** Best for instrumental music; real-time streaming; no lyrics. Config: `GEMINI_API_KEY`.
- **MiniMax:** Only music provider that supports vocals/lyrics and reference-audio style transfer. Config: `AIMLAPI_KEY`. Job status can be checked with `ai-content music-status <id>`.

---

## Video Providers

| Provider | Registered as | Image-to-Video | Max Duration | Notes |
|----------|----------------|----------------|--------------|--------|
| **Veo** | `veo` | Yes (first_frame_url) | 8 s | Google; fast (~30 s typical); text or image-to-video. |
| **Kling** | `kling` | Yes | 10 s | KlingAI direct; JWT auth; higher quality; 5–14 min wait. |

- **Veo:** Default for challenge; no Kling credentials needed. Config: `GEMINI_API_KEY`.
- **Kling:** Requires Kling API key + secret; not required for the challenge.

---

## Image Providers

| Provider | Registered as | Notes |
|----------|----------------|--------|
| **Imagen** | `imagen` | Google; used by full pipeline for keyframe generation. Config: `GEMINI_API_KEY`. |

---

## Quick Reference

- **Vocals/lyrics:** MiniMax only.
- **Image-to-video:** Veo and Kling both support it (`first_frame_url` / first-frame image).
- **Instrumental only:** Lyria.
- **No Kling needed for challenge:** Gemini (Lyria, Veo, Imagen) and/or AIMLAPI (MiniMax) are sufficient.

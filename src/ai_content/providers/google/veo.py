"""
Google Veo video provider.

Uses async polling for video generation.
"""

import asyncio
import logging
from datetime import datetime, timezone
from pathlib import Path

from ai_content.core.registry import ProviderRegistry
from ai_content.core.result import GenerationResult
from ai_content.core.exceptions import (
    ProviderError,
    AuthenticationError,
    TimeoutError,
)
from ai_content.config import get_settings

logger = logging.getLogger(__name__)


@ProviderRegistry.register_video("veo")
class GoogleVeoProvider:
    """
    Google Veo 3.1 video provider.

    Features:
        - Text-to-video generation
        - Image-to-video (with first frame)
        - Multiple aspect ratios
        - Fast generation (~30 seconds typical)

    Example:
        >>> provider = GoogleVeoProvider()
        >>> result = await provider.generate(
        ...     "Dragon soaring over mountains",
        ...     aspect_ratio="16:9",
        ... )
    """

    name = "veo"
    supports_image_to_video = True
    max_duration_seconds = 8

    def __init__(self):
        self.settings = get_settings().google
        self._client = None

    def _get_client(self):
        """Lazy-load the Google GenAI client."""
        if self._client is None:
            try:
                from google import genai

                api_key = self.settings.api_key
                if not api_key:
                    raise AuthenticationError("veo")
                self._client = genai.Client(api_key=api_key)
            except ImportError:
                raise ProviderError(
                    "veo",
                    "google-genai package not installed. Run: pip install google-genai",
                )
        return self._client

    async def generate(
        self,
        prompt: str,
        *,
        aspect_ratio: str = "16:9",
        duration_seconds: int = 5,
        first_frame_url: str | None = None,
        output_path: str | None = None,
        use_fast_model: bool = False,
        person_generation: str = "allow_adult",
    ) -> GenerationResult:
        """
        Generate video using Veo 3.1.

        Args:
            prompt: Scene description
            aspect_ratio: "16:9", "9:16", or "1:1"
            duration_seconds: Currently ignored (model determines)
            first_frame_url: Optional image URL to animate
            output_path: Where to save the video
            use_fast_model: Use faster but lower quality model
            person_generation: "allow_adult" or "dont_allow"
        """
        from google.genai import types

        client = self._get_client()

        model = (
            self.settings.video_fast_model
            if use_fast_model
            else self.settings.video_model
        )

        logger.info(f"🎬 Veo: Generating video ({aspect_ratio})")
        logger.debug(f"   Prompt: {prompt[:50]}...")
        logger.debug(f"   Model: {model}")

        try:
            # Build config (google-genai uses GenerateVideosConfig; omit person_generation - API rejects it)
            config = types.GenerateVideosConfig(aspect_ratio=aspect_ratio)

            # Generate
            if first_frame_url:
                # Image-to-video
                image_data = await self._fetch_image(first_frame_url)
                image = types.Image(image_bytes=image_data)
                operation = await client.aio.models.generate_videos(
                    model=model,
                    prompt=prompt,
                    image=image,
                    config=config,
                )
            else:
                # Text-to-video
                operation = await client.aio.models.generate_videos(
                    model=model,
                    prompt=prompt,
                    config=config,
                )

            # Poll until complete
            logger.info("   Waiting for generation...")
            while not operation.done:
                await asyncio.sleep(5)
                operation = await client.aio.operations.get(operation)

            # One more fetch after done (API may lag populating response)
            operation = await client.aio.operations.get(operation)

            # Check for API error (operation can be done but failed)
            if getattr(operation, "error", None):
                err_msg = str(operation.error) if operation.error else "Operation failed"
                logger.error(f"   Veo operation error: {err_msg}")
                return GenerationResult(
                    success=False,
                    provider=self.name,
                    content_type="video",
                    error=err_msg,
                )

            # Response may be in .response or .result
            response = getattr(operation, "response", None) or getattr(operation, "result", None)
            generated = getattr(response, "generated_videos", None) if response else None
            # generated_videos can be empty when RAI (content policy) filtered the output
            if not generated or len(generated) == 0:
                rai_count = getattr(response, "rai_media_filtered_count", None) if response else None
                rai_reasons = getattr(response, "rai_media_filtered_reasons", None) if response else None
                err_parts = ["No video in response"]
                if rai_count is not None and rai_count > 0:
                    err_parts.append("content likely filtered by safety policy (RAI)")
                    if rai_reasons:
                        err_parts.append(f"reasons={rai_reasons}")
                elif getattr(operation, "error", None):
                    err_parts.append(str(operation.error))
                err_detail = "; ".join(str(p) for p in err_parts)
                logger.warning(f"   Veo: {err_detail}")
                return GenerationResult(
                    success=False,
                    provider=self.name,
                    content_type="video",
                    error=err_detail,
                )

            # Get video data (API may return bytes inline or via File reference)
            video = generated[0]
            video_data = video.video.video_bytes
            if video_data is None:
                try:
                    video_data = await client.aio.files.download(file=video.video)
                except Exception:
                    uri = getattr(video.video, "uri", None)
                    if uri and isinstance(uri, str) and uri.startswith("http"):
                        import httpx
                        async with httpx.AsyncClient(timeout=120.0) as http_client:
                            resp = await http_client.get(uri)
                            resp.raise_for_status()
                            video_data = resp.content
                    else:
                        video_data = None
            if not video_data:
                return GenerationResult(
                    success=False,
                    provider=self.name,
                    content_type="video",
                    error="No video data in response",
                )

            # Save
            if output_path:
                file_path = Path(output_path)
            else:
                output_dir = get_settings().output_dir
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                file_path = output_dir / f"veo_{timestamp}.mp4"

            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_bytes(video_data)

            logger.info(f"✅ Veo: Saved to {file_path}")

            return GenerationResult(
                success=True,
                provider=self.name,
                content_type="video",
                file_path=file_path,
                data=video_data,
                metadata={
                    "aspect_ratio": aspect_ratio,
                    "model": model,
                    "prompt": prompt,
                },
            )

        except Exception as e:
            logger.error(f"Veo generation failed: {e}")
            return GenerationResult(
                success=False,
                provider=self.name,
                content_type="video",
                error=str(e),
            )

    async def _fetch_image(self, url: str) -> bytes:
        """Fetch image data from URL."""
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content

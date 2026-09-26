# Instagram and TikTok cover handoff

Verified 7 September 2026 against Zernio platform docs and live OpenAPI. Recheck these fields when implementing a publishing integration; this skill generates files only.

**Shared master:** 1080 × 1920, 9:16, JPEG or PNG. The design and resolution work for both platforms, so there is no need to render two different compositions. The 1080 × 1440 centre crop is a review of Instagram's 3:4 profile tile, not a second image that must be uploaded.

**Instagram Reels:** Zernio recommends 1080 × 1920 for `platformSpecificData.instagramThumbnail` (alias `reelCover`). A supplied cover takes priority over `thumbOffset`. Its `MediaItem.instagramThumbnail` is another documented placement, with higher precedence. Use a publicly accessible image URL only during an authorized publication/attachment operation.

**TikTok:** Zernio's current platform page documents top-level `tiktokSettings.video_cover_image_url`, which overrides `video_cover_timestamp_ms`. Its OpenAPI also documents `TikTokPlatformData.videoCoverImageUrl`, overriding `videoCoverTimestampMs`. Match the SDK/API shape being used instead of mixing snake_case and camelCase locations. Zernio implements a custom image by adding one frame to the start of the video; the native TikTok Content Posting API primarily selects a video frame by timestamp. Do not silently modify an existing delivered video file or label the adapted upload byte-identical to it.

Rendering approval is not publishing approval. Keep exact platform/account/post identity and crop review in the publishing workflow. A local three-column grid is a mockup, not proof of the live account's final crop or app overlays.

Sources:

- https://docs.zernio.com/platforms/instagram — custom cover field recommends 1080 × 1920.
- https://docs.zernio.com/platforms/tiktok — 9:16 and 1080 × 1920; snake_case cover-image field.
- https://docs.zernio.com/api/openapi — YAML; `TikTokPlatformData.videoCoverImageUrl` describes the added cover frame.
- https://developers.tiktok.com/doc/content-posting-api-reference-direct-post — native cover timestamp.
- https://buffer.com/library/instagram-image-size — Instagram profile grid uses 3:4.

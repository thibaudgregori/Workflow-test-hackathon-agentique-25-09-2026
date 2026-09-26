# OpenAI Ads through Zernio

Official docs: https://docs.zernio.com/platforms/openai-ads

## Connection

`POST /v1/connect/openai-ads/credentials` accepts one ChatGPT Ads Manager API key and one `profileId`. One key maps to exactly one ad account and has full campaign write access; OpenAI does not provide a read-only key scope. Never print or persist the raw key outside approved secret storage.

## Supported shape

- Standalone campaign -> ad group -> image chat-card ad.
- Performance sync, pause/resume, budget updates, location targeting, bid caps, pixels, and server-side conversions.
- Budgets are lifetime-only and require an end date. Minimum documented budget is $1.
- Creative is a static image with title 3-50 characters, body up to 100 characters, and destination URL. Video is unsupported.
- Targeting is location-only: country, region, or DMA. Age, gender, interests, and ROAS bidding are rejected.
- Goals: traffic, awareness, or conversions. Conversion optimization requires an active conversion event setting.
- OpenAI-side limits documented by Zernio: 600 requests/min per endpoint, 1,200/min overall, 1,000 conversion events per batch.

## Lifecycle differences

OpenAI Ads has no delete API. Zernio cancellation archives the ad, ad group, and campaign; archive is terminal.

## Tracking and conversions

- Creating `/v1/accounts/{accountId}/tracking-tags` provisions a pixel and API key. It is not idempotent, OpenAI pixels cannot be deleted, and Zernio allows one managed pixel per ad account. Never auto-retry.
- Send events through `/v1/ads/conversions` using a destination from `/v1/accounts/{accountId}/conversion-destinations`.
- Keep stable `eventId` values. Zernio hashes email identifiers and converts monetary values to the minor units OpenAI expects.
- One invalid event can fail an entire OpenAI batch. Validate every row, then reconcile the batch result before retrying only the failed work.


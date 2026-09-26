# Ads operations

Zernio covers Meta, Google Ads, TikTok Ads, LinkedIn Ads, Pinterest Ads, X Ads, and OpenAI Ads.

## Endpoint families

| Area | Representative paths |
|---|---|
| Object tree | `/v1/ads`, `/v1/ads/campaigns`, `/v1/ads/ad-sets/{id}`, `/v1/ads/{id}`, `/v1/ads/tree`, `/v1/ads/timeline` |
| Creation/status | `/v1/ads/create`, `/v1/ads/boost`, campaign/ad/ad-set status endpoints, duplicate endpoints |
| Preview/analytics | `/v1/ads/preview`, `/v1/ads/{id}/preview`, `/v1/ads/{id}/analytics`, campaign analytics |
| Insights | `/v1/ads/insights`, async insight reports, search terms, keywords, local-services leads |
| Creative library | images, creatives, catalogs, product sets |
| Targeting | interests, targeting search, reach estimate, bid pricing, supply forecast |
| Audiences | list/create/read/update/delete, member upload |
| Lead gen | lead forms, form leads, test leads |
| Tracking/conversions | tracking tags, destinations, conversions, adjustments, quality |
| Messaging ads | click-to-message, click-to-call, legacy CTWA |
| Account ops | finance, activity log, DSA defaults/recommendations, labels, studies, value rules, high-demand periods |

Use the live OpenAPI for exact methods and schemas.

## High-risk invariants

- Audience creation is not idempotent. Never blindly repeat it after a timeout.
- Meta value-rule updates are full replacement, not patch: GET first, preserve IDs for retained rules/criteria, and remember array order is evaluation order.
- Deleting an audience or creative can remove it from the underlying platform. Verify exact IDs and dependencies.
- Meta custom audience uploads support up to 10,000 users per request; identifiers are hashed server-side. Do not upload fields beyond the approved matching purpose.
- Conversion batching is platform-specific. A malformed event can fail a whole batch; preserve event IDs and reconcile partial results.
- EU DSA beneficiary/payor values are legal disclosures. Never guess them; read defaults/recommendations and obtain the user's chosen entities.
- Reach/forecast/keyword/preview endpoints are preferred before a spend-changing create.

## Readback

After a mutation, read both the Zernio object and, where returned, its platform object/status. For async reports or syncs, poll only according to the documented status/Retry-After values and stop on terminal failure.


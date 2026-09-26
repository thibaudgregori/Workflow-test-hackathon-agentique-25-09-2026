# Webhooks

Official docs: https://docs.zernio.com/webhooks

## Delivery contract

- Success is any `2xx` returned within 5 seconds.
- Failures retry with exponential backoff for up to 7 attempts; the final failure moves to a dead-letter queue.
- Delivery is at least once. Deduplicate with `payload.id` / `X-Zernio-Event-Id` before processing.
- Acknowledge after durably accepting the event, then do expensive work asynchronously.

## Signature verification

When a secret is configured, `X-Zernio-Signature` is the lowercase hex HMAC-SHA256 of the raw request body keyed by the webhook secret. Compute from raw bytes and compare in constant time before parsing/processing. Reject unsigned or mismatched deliveries.

## Routing

Subscribe only to events the application handles. Major event families cover posts, inbox activity, account connections, ads/leads, calls, WhatsApp, and phone-number lifecycle.

For multi-tenant routing:

- Post events: map each platform entry's `accountId`.
- Account events: use `profileId` and `accountId`.
- Inbox/call events: map the included account ID.

## Configuration safety

List existing settings first. Adding/updating/deleting a webhook endpoint or changing its secret/events is an external write requiring confirmation. Afterward, use the official test endpoint and read webhook logs; never log the secret or raw sensitive payloads.


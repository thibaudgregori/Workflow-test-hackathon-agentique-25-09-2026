# Messaging core

Official inbox docs: https://docs.zernio.com/messages/list-inbox-conversations

## Main endpoint families

| Area | Operations |
|---|---|
| Conversations | list, search, get, create, archive/activate, mark read |
| Messages | list, send, react/unreact, typing indicator, resolve expiring attachments |
| Comments/reviews | list, reply, private reply, moderate where the platform permits |
| Contacts | list/search, create, bulk create, update, tag, custom fields |
| Media | direct authenticated upload for message attachments |

Use the live OpenAPI for exact schemas. Endpoint names evolve faster than this routing reference.

## Context and identity

- Fetch full message history before drafting or classifying. Instagram/Facebook pre-connect replay can add older conversations asynchronously; repeat sweeps when mirroring a newly connected account.
- Resolve records by exact IDs, not display names. A contact can have multiple platform channels.
- Search covers stored WhatsApp, SMS, Telegram, Facebook, Instagram, Twitter/X, and Reddit messages; Bluesky conversations are fetched live and are not text-searchable.
- Instagram/Facebook attachment URLs expire. Store the message ID or `refreshUrl`, then resolve a fresh URL when needed.

## Sending safeguards

- `POST /v1/inbox/conversations/{conversationId}/messages` supports an `Idempotency-Key`. Reusing the same key/body replays the response; the same key with a different body returns `422`; an in-flight duplicate returns `409`. Keys are retained for 24 hours.
- WhatsApp may require an approved template when the 24-hour customer-service window is closed.
- Creating a new conversation can reach a recipient with no existing thread only where the platform supports it and the exact recipient identifier is valid.
- A typing indicator can have side effects: on WhatsApp it may mark the referenced inbound message read. Treat it as a write.
- Marking a conversation read can send WhatsApp blue ticks. Do not call it during a read-only audit.

## Pagination and delivery

Paginate every list until completion. After a send, re-read the message/conversation and delivery state. Keep failed recipients and error details; never turn a partial result into a blanket success.


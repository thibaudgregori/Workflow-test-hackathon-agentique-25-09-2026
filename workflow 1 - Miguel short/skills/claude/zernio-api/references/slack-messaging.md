# Slack messaging

Official docs: https://docs.zernio.com/platforms/slack

- One connected Slack account represents one selected channel. Connect another account for another channel; there is no per-message channel override.
- Ingested inbox events are DMs, bot mentions, replies in participating threads, and the bot's own messages. Ordinary channel chatter is not mirrored.
- Contacts, Sequences, and Workflows are DM-only. Channel mentions need an external webhook-driven agent.
- Find eligible members with `GET /v1/accounts/{accountId}/slack-members?query=...`; use the returned opaque member ID as `participantId` when starting a DM.
- Reply inside a thread using `replyTo`. Other bots do not trigger automations/webhooks, which prevents loops.
- Private channels require `/invite @Zernio`. Older connections may need reconnecting once for new inbox scopes.
- Slack does not expose public message analytics. Do not infer zero engagement from Zernio's zero metrics.

Confirm before posting, starting a DM, replying, editing, deleting, reconnecting, or changing default identity settings.


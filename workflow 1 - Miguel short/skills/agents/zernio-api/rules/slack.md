# Slack

Official docs: https://docs.zernio.com/platforms/slack

## Publishing contract

- Create Slack posts through `POST /v1/posts` with `platform: "slack"`.
- One connected Slack account represents one channel. Do not send `platformSpecificData.channelId`; it returns `400`.
- Content limit is 40,000 characters. Slack silently truncates beyond that. Editing is limited to 4,000 characters.
- Up to 10 files can be attached. Zernio-side scheduling is supported; public message analytics are not.
- Optional fields: `threadTs`, `unfurlLinks`, `unfurlMedia`, `username`, and `iconUrl`.

## Connection

1. `GET /v1/connect/slack?profileId=...` starts OAuth.
2. The user authorizes a workspace and chooses a channel.
3. `POST /v1/connect/slack` saves the channel account.

Headless mode returns a short-lived `pendingDataToken`. To add another channel from the same workspace, pass an existing Slack `accountId` and select another channel without repeating OAuth.

Public channels can be joined during connection. A member must run `/invite @Zernio` before a private channel is selectable. Workspaces connected before Slack inbox support may need one reconnect to grant the newer history scopes.

## Inbox and DMs

Zernio ingests direct messages to the bot, channel messages that mention it, replies in threads the bot participates in, and the bot's own messages. It deliberately does not mirror ordinary channel chatter.

- Reply with `POST /v1/inbox/conversations/{conversationId}/messages`; pass `replyTo` for a thread reply.
- Find DM recipients with `GET /v1/accounts/{accountId}/slack-members?query=...`, then create a conversation using the member's opaque Slack ID as `participantId`.
- Contacts, Sequences, and Workflows apply to DMs only. Channel mentions require your own webhook-driven agent logic.
- Other bots may appear as context but do not trigger automations or webhooks, preventing loops.

## Read-before-write checks

Before publishing or messaging, re-read the exact Slack account, connected channel, and health. Before a DM, resolve the exact member ID. Confirm immediately before sending, editing, deleting, or reconnecting.

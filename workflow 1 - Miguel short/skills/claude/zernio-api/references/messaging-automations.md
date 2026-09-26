# Broadcasts, sequences, and comment automations

Official docs: https://docs.zernio.com/broadcasts/create-broadcast and https://docs.zernio.com/sequences/create-sequence

## Broadcasts

Broadcasts send one message to many contacts or raw recipients, now or later.

1. Read the exact profile/account and recipient selection.
2. Create or edit the draft only after confirming its content and targeting when creation itself is desired.
3. Add recipients and inspect the count, subscription state, duplicates, and platform eligibility.
4. Confirm separately immediately before `/send` or `/schedule`.
5. Paginate recipient results and report delivered, failed, skipped, and pending counts.

Never remove failed or opted-out recipients merely to make metrics look cleaner. Preserve the broadcast and recipient history.

## Sequences

Sequences are multi-step message schedules. Before enrollment, read the complete step list, delays, variable mapping, account/platform, enrollment status, and target contacts.

- Variables are positional (`"1"`, `"2"`, ...); supported sources include name, phone, email, company, and explicit custom values.
- Enrollment starts external messaging and requires confirmation of exact contact IDs.
- Removing an enrollment or changing a live sequence is a write; read its current status first.

## Comment-triggered DMs

Comment automations watch a specific Instagram or Facebook post, match configured keywords/audience rules, optionally reply publicly, and send a DM.

- Verify the exact source post/account and inspect recent logs before editing.
- Confirm keyword matching, audience/follower gate, public reply, private message, and enabled state together.
- Audience follow checks may return an explicit unknown state when the commenter has never DMed the account; do not treat unknown as false evidence.
- Other bots and self-generated messages must not create loops.


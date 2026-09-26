# SMS verification codes

Official docs: https://docs.zernio.com/verify/create-verification

- `POST /v1/verify/verifications` creates and sends an SMS code. Each accepted send bills a verification fee plus the normal message rate.
- `GET /v1/verify/verifications/{verificationId}` reads status.
- `POST /v1/verify/verifications/{verificationId}/check` checks the user-entered code.
- The current channel is SMS. Recipients use E.164 numbers; codes are 4-8 digits and TTL is 1-15 minutes.
- Recreating an active `(channel, to)` verification resends a new code on the same record, limited to once per 60 seconds. The original brand, length, and TTL remain in effect.
- Only the code hash is stored, but destination/status are still sensitive.

Sending or resending is billable external communication and requires confirmation of sender, destination, brand name, TTL, and purpose. Never expose a received code in logs or retain it after checking.


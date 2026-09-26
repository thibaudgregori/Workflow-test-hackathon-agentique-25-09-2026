# SMS and MMS

Official docs: https://docs.zernio.com/platforms/sms

## Sending

- `POST /v1/sms/messages` sends SMS or MMS from an SMS-enabled account number.
- Normalize recipients to E.164 and verify the exact sender number/account.
- Use `Idempotency-Key`; after a timeout, reconcile before retrying.
- Replies enter the unified Zernio inbox. Preserve opt-outs and read `/v1/sms/opt-outs` before any bulk send.
- MMS uses `mediaUrls`; validate allowed media and total size through the live docs.

## US carrier registration

US delivery requires an approved 10DLC or toll-free registration. Use `/v1/sms/registrations/preflight` before starting a registration. Registration is asynchronous and may require OTP, opt-in proof, an appeal, or a reviewer response.

- Reuse an existing approved registration for additional numbers when eligible; this avoids another brand fee.
- Do not fabricate opt-in language, proof, business data, or campaign examples.
- A sender ID or registration create/deactivation affects deliverability and may incur recurring charges; confirm first.

## Sender IDs and lookups

Alphanumeric sender IDs are country-specific and generally one-way; recipients may not be able to reply. `/v1/sms/lookup` reports carrier/line type and is a safe preflight. Limit-increase requests and sender-ID deletion are external writes requiring confirmation.


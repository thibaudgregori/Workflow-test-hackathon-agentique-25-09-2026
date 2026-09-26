# Phone numbers

Official docs: https://docs.zernio.com/platforms/phone-numbers

## Model

A Zernio phone number can carry PSTN voice, SMS/MMS, and WhatsApp. `/v1/phone-numbers` is canonical; older `/v1/whatsapp/phone-numbers/*` paths are deprecated aliases.

## Safe reads and preflights

- `GET /v1/phone-numbers/countries` - live countries, pricing, and capabilities.
- `GET /v1/phone-numbers/availability` and `/available` - inventory/feasibility before purchase.
- `POST /v1/phone-numbers/port-in/check` - portability before uploading time-limited documents.
- `GET /v1/phone-numbers/kyc` and KYC form/remediation reads - requirements before collecting personal data.
- `POST /v1/phone-numbers/kyc/validate-address` and `/kyc/review-packet` - advisory checks before submission.

## Mutating lifecycle

- Purchase: `POST /v1/phone-numbers/purchase` is payment-first and auto-assigns a number. Confirm country, number type, capabilities, recurring price, and exact profile first.
- Release: `DELETE /v1/phone-numbers/{id}` gives up the number and can terminate attached services. Treat it as destructive.
- Porting: upload documents immediately before `POST /v1/phone-numbers/port-in`; carrier uploads may expire after 30 minutes. A response can contain per-order partial failures.
- KYC: regulated countries require documents/identity data and may enter asynchronous pending/declined/remediation states. Use webhooks or bounded polling.
- Enable/disable voice or SMS through `POST`/`DELETE /v1/phone-numbers/{id}/{feature}` only after verifying capability and pricing.

Do not create a hosted KYC/share link without confirming the intended recipient and branding; it grants a third party access to submit regulated identity data.


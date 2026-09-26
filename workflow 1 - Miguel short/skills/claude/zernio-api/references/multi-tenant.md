# Multi-tenant architecture

Official docs: https://docs.zernio.com/multi-tenant

## Boundary and mapping

- Create one Zernio profile per customer and persist `customerId -> profileId`.
- Persist every `accountId -> customerId/profileId` mapping from connect results and `account.connected` webhooks.
- Always filter account reads by the customer's profile, then verify every account ID belongs to that customer before a write. Zernio validates account IDs at the team level, not as a hard tenant boundary.
- Configure webhooks once per team and route events internally using `profileId` or `accountId`.

## Least-privilege keys

API keys may be full-team, profile-scoped, read-only, and optionally expiring. A per-tenant service should receive only its profile IDs and required permission. Key creation/revocation requires confirmation and exact scope readback.

## Current rate-limit model

| Connected accounts | Requests/minute |
|---|---:|
| 0-2 | 60 |
| 3-2,000 | 600 |
| 2,001+ | 1,200 |

The budget is team-wide. Prefer webhooks over polling, smooth background work through a bounded queue, and enforce fairness between tenants. Honor `Retry-After` on `429`. Treat `402 PAYMENT_REQUIRED` as a team-wide billing suspension and alert rather than retrying.

## Offboarding

Before deleting a profile, disconnect its exact active accounts; active connections block deletion. Re-read every account/profile ID, preserve required history/mappings, and obtain destructive confirmation for each disconnect/deletion scope.


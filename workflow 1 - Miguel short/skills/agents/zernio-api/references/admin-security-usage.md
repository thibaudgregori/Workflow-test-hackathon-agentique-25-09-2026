# Administration, security, and usage

Official security docs: https://docs.zernio.com/security

## Connected apps

- `GET /v1/me/connected-apps` lists live OAuth clients such as AI assistants and MCP connectors.
- Revoking an app invalidates every live token and pending authorization it holds for the user. This is an immediate external-access change requiring exact client ID/name/scopes readback and confirmation.
- Connected-app management requires a session or full-access API key; profile-scoped, restricted, and OAuth tokens cannot enumerate sibling authorizations.

## Keys, team, and security

API-key creation/revocation, user invitations/role changes, SSO, SCIM, two-step verification, and team security settings are admin-plane actions. Use least privilege, never reveal secrets or backup codes, and verify the exact team/user/client/profile scope before every write.

Prefer profile-scoped/read-only/expiring keys for narrow services. Creating a replacement key does not authorize revoking the old one; verify migration first and obtain separate confirmation.

## Usage and billing

`/v1/usage` and related reads expose plan/billing status, account/call/SMS usage, and X API pricing. These are safe reads but can contain commercially sensitive data. Use live snapshots before cost recommendations. Treat `402 PAYMENT_REQUIRED` as a billing-state incident, not a retriable API failure.

## Logs and account settings

Read logs/health/settings before changing account defaults, menus, commands, ice breakers, or account groups. Group deletion does not delete accounts, but it is still a workspace mutation and requires exact-ID confirmation.


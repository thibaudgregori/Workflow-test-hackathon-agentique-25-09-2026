# Official clients and OpenAPI

Official docs: https://docs.zernio.com/sdks

## Access-path selection

1. Official `zernio` CLI for supported one-off reads/actions.
2. Official SDK or direct REST API for application code, bulk work, explicit pagination/retries, and the full surface.
3. Hosted MCP for interactive AI clients.

Official SDKs cover the full API:

- Node.js/TypeScript: `@zernio/node`
- Python: `zernio-sdk` (sync/async and direct media upload)
- Go: `github.com/zernio-dev/zernio-go`
- Ruby: `zernio-sdk`
- Java: `dev.zernio:zernio-sdk`
- PHP: `zernio-dev/zernio-php`
- .NET: `Zernio`
- Rust: `zernio`

For Python in this workspace, always run through `~/Documents/Workspace/.venv/bin/python` and install dependencies only after checking the existing environment and obtaining approval if installation changes are material.

The live OpenAPI 3.1 specification is at `https://docs.zernio.com/api/openapi`. Prefer generated types/current schemas over hardcoded request shapes. Never hardcode credentials; use `ZERNIO_API_KEY` through approved secret loading.

The vendor Chat SDK adapter is `@zernio/chat-sdk-adapter` for Instagram, Facebook, Telegram, WhatsApp, X, Bluesky, and Reddit.


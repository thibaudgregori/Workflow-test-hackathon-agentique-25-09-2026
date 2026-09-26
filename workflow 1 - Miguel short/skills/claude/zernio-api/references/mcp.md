# Zernio MCP

Official docs: https://docs.zernio.com/mcp

## Hosted server

- URL: `https://mcp.zernio.com/mcp`
- Registry name: `com.zernio/zernio`
- Authentication: Zernio OAuth where the client supports it, otherwise `Authorization: Bearer <API key>`.
- Zernio documents 496 tools: a compact core remains visible and additional endpoints are found through `search_tools` to avoid loading the whole surface into context.

## Client setup

Adding a server/plugin changes external configuration and requires confirmation. For Codex, the documented commands are:

```bash
codex mcp add zernio --url https://mcp.zernio.com/mcp
codex mcp login zernio
```

Do not run these merely because Zernio work is requested; first inspect whether the connector is already installed/authenticated.

## Tool-use safety

MCP exposes the full API, so tool availability is not authorization to mutate. Apply the same skill-specific gates: confirm recipients/content before messaging, spend/status before ads, and exact targets before destructive or billable telephony/admin actions. Use `search_tools` for the exact operation and inspect its schema rather than guessing.


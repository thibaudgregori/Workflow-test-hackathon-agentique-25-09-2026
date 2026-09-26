# Voice and calls

Official docs: https://docs.zernio.com/platforms/voice

## Capabilities

PSTN calling supports inbound/outbound calls, phone/SIP/AI-agent routing, browser WebRTC calling, optional recording/transcription, transfer/end actions, and unified call history. WhatsApp Business Calling is a separate channel, although both appear in `/v1/calls`.

## Endpoints

| Operation | Path |
|---|---|
| Unified history/detail/recording | `/v1/calls`, `/v1/calls/{id}`, `/v1/calls/{id}/recording` |
| Place/list/get PSTN call | `/v1/voice/calls` and `/v1/voice/calls/{id}` |
| Estimate cost | `/v1/voice/calls/estimate` |
| End or transfer | `/v1/voice/calls/{id}/end`, `/transfer` |
| Browser session/dial | `/v1/voice/calls/web`, `/v1/voice/calls/web/dial` |
| Configure number | `/v1/phone-numbers/{id}/voice` |
| WhatsApp calling config | `/v1/phone-numbers/{id}/whatsapp/calling` |

## Safety

- Run the estimate before outbound PSTN calls and confirm caller ID, destination, routing, recording, transcription, and maximum intended duration.
- Inbound routing can forward real customer calls or stream audio to an external AI/WebSocket service. Verify the destination and data-processing policy.
- Ending and blind-transferring live calls are immediate service actions. Confirm the exact active call ID and target.
- Recording URLs are sensitive and may expire. Do not persist or share them beyond the approved purpose.
- WhatsApp outbound calling is restricted in some countries. Read current platform restrictions before promising availability.


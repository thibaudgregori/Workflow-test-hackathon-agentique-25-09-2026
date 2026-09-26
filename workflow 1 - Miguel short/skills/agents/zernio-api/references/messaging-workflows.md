# Branching Workflows

Official create docs: https://docs.zernio.com/workflows/create-workflow

## Scope

Workflows are branching conversation automations represented as node/edge graphs. Supported platforms are WhatsApp, Instagram, Facebook, Telegram, Twitter/X, Bluesky, and Reddit.

## Lifecycle and endpoints

| Method | Path | Purpose |
|---|---|---|
| GET / POST | `/v1/workflows` | list or create a draft |
| GET / PATCH / DELETE | `/v1/workflows/{workflowId}` | read graph, update, or permanently delete |
| POST | `/v1/workflows/{workflowId}/activate` | start matching inbound messages |
| POST | `/v1/workflows/{workflowId}/pause` | stop new progression |
| GET / POST | `/v1/workflows/{workflowId}/executions` | list runs or manually trigger one |
| GET | `/v1/workflows/{workflowId}/executions/{executionId}/events` | read the run timeline |
| POST | `/v1/workflows/{workflowId}/duplicate` | copy a workflow |
| GET | `/v1/workflows/{workflowId}/versions` | list saved versions |
| GET / POST | `/v1/workflows/{workflowId}/versions/{version}` | inspect or restore a version |

## Invariants

- Creation produces a draft. Activation requires a structurally complete graph with one reachable trigger/entry.
- The graph can be changed only while draft or paused.
- Reassigning `accountId` derives platform/profile server-side and revalidates every node for the new platform.
- A manual run uses an existing `conversationId`, or a WhatsApp `to` number that finds/creates a conversation. It can send external messages and always requires confirmation.
- Execution timelines have 90-day retention. Inspect them when a run fails rather than blindly retrying.
- Deletion permanently removes the workflow and all executions. List the exact workflow ID/name and obtain explicit destructive confirmation.

## Safe workflow

Read the full graph and current status; validate reachable nodes and platform support; show the proposed graph/status delta; confirm; mutate; then re-read the graph, status, version, and any resulting run.


# Design HTTP Tunneling Service

> **Difficulty**: Hard  |  **Asked at**: Amazon, Cloudflare
> **Patterns the source uses**: Proxy, Observer, Strategy (protocol handling)

Design an ngrok-like HTTP tunneling service that exposes a local port to the internet via a unique public URL. The tunnel server receives incoming public HTTP requests and forwards them to the local client through a persistent connection, then relays the response back to the original caller.

## In scope

1. `create_tunnel(local_port)` — register a tunnel, return a unique public URL
2. `forward_request(tunnel_id, request)` — relay an incoming HTTP request to the local client
3. `close_tunnel(tunnel_id)` — deregister and clean up
4. `handle_incoming(request)` — entry point for public HTTP requests; route to correct tunnel
5. Persistent connection between tunnel server and tunnel client
6. Timeout handling when local server is unresponsive
7. Request/response correlation (match response to original caller)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/30-design-tunneling-service.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.

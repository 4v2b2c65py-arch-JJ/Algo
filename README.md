# Algo

API surface for the agent-loop algorithm. The algorithm runs on the host
machine; this repository ships the API contract and a client only — no
source code is included.

## Host the API

On the machine that runs the algorithm:

```
agent-loop serve --host 0.0.0.0 --port 8000 --api-token YOUR_TOKEN
```

The token is optional but recommended. When set, every request must carry
the header `X-API-Token: YOUR_TOKEN` or the server answers `401`.

## Clone and call

This repository clones into any machine and works immediately against the
host — no source, no build step, stdlib only:

```python
from algo_client import AlgoClient

client = AlgoClient("http://HOST:8000", api_token="YOUR_TOKEN")
print(client.health())
print(client.run("plan the release"))
print(client.monologue_scores())
```

## API

### Core

| Method | Path | Description |
| --- | --- | --- |
| GET | `/health` | service health |
| POST | `/run` | run a goal through the loop (`{"goal": "...", "agent": "planner"}`) |
| POST | `/inspect` | run a goal, then return the inspection report |
| GET | `/metrics` | measurement log |
| GET | `/leaderboard` | runtime leaderboard |
| GET | `/index` | continuity index |
| GET | `/inspections` | inspection report |

### Monologue analytics

| Method | Path | Description |
| --- | --- | --- |
| GET | `/monologue` | last monologue transcript |
| GET | `/monologue/scores` | per-thought scores |
| GET | `/monologue/frequency` | emit frequency waypoints |
| GET | `/monologue/security` | security measurement score |
| GET | `/monologue/velocity` | velocity per thought |
| GET | `/monologue/piles` | pile ups and pile downs |
| GET | `/monologue/firm` | asserted firm monologues |
| GET | `/monologue/model` | descriptive monologue model |
| GET | `/monologue/clauses` | captured clauses |
| GET | `/monologue/mentalscape` | mental terrain model |

### Battery

| Method | Path | Description |
| --- | --- | --- |
| GET | `/battery` | battery statuses and swap log |
| POST | `/battery/rest` | rest an agent (`{"agent": "...", "amount": 25}`) |
| POST | `/battery/swap` | swap to the best agent (`{"agent": "..."}`) |

### Matrix

| Method | Path | Description |
| --- | --- | --- |
| GET | `/matrix` | matrix viewer panel (query params: `flag`, `method`, `prefix`, `profile`, `space`) |
| GET | `/matrix/finalise` | assert finalise requirements (`?profile=...`) |
| POST | `/matrix/finalise` | finalise production for a profile |
| GET | `/matrix/observe` | observe guided completion (`?profile=...`) |

### Pipe

| Method | Path | Description |
| --- | --- | --- |
| GET | `/pipe` | role transport carriers (`?hide_carrier_log=true` to hide carried capsules) |
| GET | `/pipe/inspect` | inspect carry edges |
| GET | `/pipe/roles` | read roles |
| GET | `/pipe/carriers` | carriers by badge category (`?category=...`) |
| POST | `/pipe/package` | package roles (`{"name": "roles"}`) |
| POST | `/pipe/transport` | transport a capsule (`{"capsule": 1, "target": "executor"}`) |
| POST | `/pipe/awaken` | awaken release matrices |

### Worth

| Method | Path | Description |
| --- | --- | --- |
| GET | `/worth` | worth registry status |
| POST | `/worth/propose` | propose a task list (`{"tasks": ["..."]}`) |
| GET | `/closures` | closure menu for the task force |
| GET | `/procedures` | procedure menu (anti-stumble) |

### MCP layer

| Method | Path | Description |
| --- | --- | --- |
| GET | `/mcp/tools` | MCP tool menu |
| POST | `/mcp/enter` | enter with privilege auth (`{"client": "...", "key": "..."}`) |
| POST | `/mcp/call` | call an MCP tool (`{"client": "...", "tool": "...", "arguments": {}}`) |
| GET | `/mcp/autocomplete` | autocompletions (`?prefix=...&limit=5`) |
| GET | `/mcp/triggers` | remembered featured triggers |
| POST | `/mcp/trigger` | feature a trigger |
| POST | `/mcp/trigger/fire` | fire remembered triggers |
| GET | `/mcp/audit` | authority audit trail |

### Spotlight

| Method | Path | Description |
| --- | --- | --- |
| GET | `/spotlight` | searchable index stats |
| GET | `/spotlight/search` | search view elements (`?q=...&kind=...&objective=...`) |
| GET | `/spotlight/viewpoints` | saved viewpoints |
| POST | `/spotlight/viewpoints` | save a viewpoint |
| GET | `/spotlight/theme` | material theme layers |
| GET | `/spotlight/layer` | push a theme layer (`?layer=...`) |
| GET | `/spotlight/bindings` | GUI binding tweaks |

### Time ticker

| Method | Path | Description |
| --- | --- | --- |
| GET | `/ticker` | time tickers |
| POST | `/ticker/tick` | tick an agent (`{"agent": "...", "gap": false}`) |

### Scripting

| Method | Path | Description |
| --- | --- | --- |
| POST | `/script` | run a natural language script (`{"script": "...", "dedupe": true}`) |

### Magnet

| Method | Path | Description |
| --- | --- | --- |
| POST | `/magnet` | parse a magnet link (`{"url": "magnet:?xt=..."}`) |

## Errors

- `400` — bad request (invalid payload)
- `401` — missing or wrong `X-API-Token`
- `403` — insufficient privilege
- `404` — unknown route

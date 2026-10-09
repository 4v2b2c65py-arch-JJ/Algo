"""Algo client — the public API surface for the agent-loop algorithm.

The algorithm runs on the host machine behind `agent-loop serve`. This client
is the only artifact callers need: clone this repository, point it at the
host, and call the API. No source code is shipped here.

Usage:
    from algo_client import AlgoClient

    client = AlgoClient("http://192.168.1.20:8000", api_token="secret")
    print(client.health())
    print(client.run("plan the release"))

The server must be started with the matching token:
    agent-loop serve --host 0.0.0.0 --port 8000 --api-token secret
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class AlgoError(Exception):
    pass


class AlgoClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        api_token: str = "",
        timeout: float = 60.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.timeout = timeout

    def _request(
        self,
        method: str,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> Any:
        url = self.base_url + path
        data: Optional[bytes] = None
        headers: Dict[str, str] = {}
        if self.api_token:
            headers["X-API-Token"] = self.api_token
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=data, headers=headers, method=method)
        try:
            with urlopen(request, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise AlgoError(f"HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise AlgoError(f"unreachable: {exc.reason}") from exc
        if not body:
            return None
        return json.loads(body)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if params:
            path = path + "?" + urlencode(params)
        return self._request("GET", path)

    def post(
        self, path: str, payload: Optional[Dict[str, Any]] = None
    ) -> Any:
        return self._request("POST", path, payload or {})

    def health(self) -> Dict[str, Any]:
        return self.get("/health")

    def run(self, goal: str, agent: str = "planner") -> Dict[str, Any]:
        return self.post("/run", {"goal": goal, "agent": agent})

    def inspect(self, goal: str = "") -> Dict[str, Any]:
        return self.post("/inspect", {"goal": goal})

    def measurements(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.get("/metrics", {"limit": limit})

    def leaderboard(self) -> List[Dict[str, Any]]:
        return self.get("/leaderboard")

    def index(self) -> Dict[str, Any]:
        return self.get("/index")

    def inspections(self) -> Dict[str, Any]:
        return self.get("/inspections")

    def monologue(self) -> List[Dict[str, Any]]:
        return self.get("/monologue")

    def monologue_scores(self) -> List[Dict[str, Any]]:
        return self.get("/monologue/scores")

    def monologue_frequency(self) -> Dict[str, Any]:
        return self.get("/monologue/frequency")

    def monologue_security(self) -> Dict[str, Any]:
        return self.get("/monologue/security")

    def monologue_velocity(self) -> Dict[str, Any]:
        return self.get("/monologue/velocity")

    def monologue_piles(self) -> Dict[str, Any]:
        return self.get("/monologue/piles")

    def monologue_firm(self) -> Dict[str, Any]:
        return self.get("/monologue/firm")

    def monologue_model(self) -> Dict[str, Any]:
        return self.get("/monologue/model")

    def monologue_clauses(self) -> List[Dict[str, Any]]:
        return self.get("/monologue/clauses")

    def monologue_mentalscape(self) -> Dict[str, Any]:
        return self.get("/monologue/mentalscape")

    def battery(self) -> Dict[str, Any]:
        return self.get("/battery")

    def battery_rest(self, agent: str, amount: float = 25.0) -> Dict[str, Any]:
        return self.post("/battery/rest", {"agent": agent, "amount": amount})

    def battery_swap(self, agent: str) -> Dict[str, Any]:
        return self.post("/battery/swap", {"agent": agent})

    def matrix(self, **params: Any) -> Dict[str, Any]:
        return self.get("/matrix", params)

    def matrix_finalise(self, profile: str) -> Dict[str, Any]:
        return self.get("/matrix/finalise", {"profile": profile})

    def matrix_observe(self, profile: str) -> Dict[str, Any]:
        return self.get("/matrix/observe", {"profile": profile})

    def matrix_finalise_post(self, profile: str) -> Dict[str, Any]:
        return self.post("/matrix/finalise", {"profile": profile})

    def pipe(self, hide_carrier_log: bool = False) -> Dict[str, Any]:
        return self.get(
            "/pipe", {"hide_carrier_log": "true" if hide_carrier_log else ""}
        )

    def pipe_inspect(self) -> Dict[str, Any]:
        return self.get("/pipe/inspect")

    def pipe_roles(self) -> Dict[str, Any]:
        return self.get("/pipe/roles")

    def pipe_carriers(self, category: str = "") -> Dict[str, Any]:
        return self.get("/pipe/carriers", {"category": category})

    def pipe_package(self, name: str = "roles") -> Dict[str, Any]:
        return self.post("/pipe/package", {"name": name})

    def pipe_transport(self, capsule: int, target: str) -> Dict[str, Any]:
        return self.post(
            "/pipe/transport", {"capsule": capsule, "target": target}
        )

    def pipe_awaken(self) -> Dict[str, Any]:
        return self.post("/pipe/awaken", {})

    def worth(self) -> Dict[str, Any]:
        return self.get("/worth")

    def worth_propose(self, tasks: List[str]) -> Dict[str, Any]:
        return self.post("/worth/propose", {"tasks": tasks})

    def closures(self) -> Dict[str, Any]:
        return self.get("/closures")

    def procedures(self) -> Dict[str, Any]:
        return self.get("/procedures")

    def mcp_tools(self) -> List[Dict[str, Any]]:
        return self.get("/mcp/tools")

    def mcp_enter(self, client: str, key: str = "") -> Dict[str, Any]:
        return self.post("/mcp/enter", {"client": client, "key": key})

    def mcp_call(
        self, client: str, tool: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.post(
            "/mcp/call",
            {"client": client, "tool": tool, "arguments": arguments},
        )

    def mcp_autocomplete(
        self, prefix: str = "", limit: int = 5
    ) -> Dict[str, Any]:
        return self.get(
            "/mcp/autocomplete", {"prefix": prefix, "limit": limit}
        )

    def mcp_triggers(self) -> Dict[str, Any]:
        return self.get("/mcp/triggers")

    def mcp_feature_trigger(
        self, name: str, tool: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        return self.post(
            "/mcp/trigger",
            {"name": name, "tool": tool, "arguments": arguments},
        )

    def mcp_trigger_fire(self) -> Dict[str, Any]:
        return self.post("/mcp/trigger/fire", {})

    def mcp_audit(self) -> List[Dict[str, Any]]:
        return self.get("/mcp/audit")

    def ticker(self) -> Dict[str, Any]:
        return self.get("/ticker")

    def ticker_tick(self, agent: str, on_gap: bool = False) -> Dict[str, Any]:
        return self.post(
            "/ticker/tick", {"agent": agent, "gap": on_gap}
        )

    def spotlight(self) -> Dict[str, Any]:
        return self.get("/spotlight")

    def spotlight_search(
        self, query: str = "", kind: str = "", objective: str = ""
    ) -> Dict[str, Any]:
        return self.get(
            "/spotlight/search",
            {"q": query, "kind": kind, "objective": objective},
        )

    def spotlight_viewpoints(self) -> Dict[str, Any]:
        return self.get("/spotlight/viewpoints")

    def spotlight_save_viewpoint(
        self, name: str, query: str, kind: str = ""
    ) -> Dict[str, Any]:
        return self.post(
            "/spotlight/viewpoints",
            {"name": name, "query": query, "kind": kind},
        )

    def spotlight_theme(self) -> Dict[str, Any]:
        return self.get("/spotlight/theme")

    def spotlight_layer(self, layer: str) -> Dict[str, Any]:
        return self.get("/spotlight/layer", {"layer": layer})

    def spotlight_bindings(self) -> Dict[str, Any]:
        return self.get("/spotlight/bindings")

    def magnet(self, url: str) -> Dict[str, Any]:
        return self.post("/magnet", {"url": url})

    def script(self, text: str, dedupe: bool = True) -> Dict[str, Any]:
        return self.post(
            "/script", {"script": text, "dedupe": dedupe}
        )

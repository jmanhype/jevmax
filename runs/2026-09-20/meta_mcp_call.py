#!/usr/bin/env python3
"""Minimal streamable-HTTP MCP client for the configured Facebook Ads server.

The authorization header is read from Codex's existing helper and never printed.
"""
import argparse
import json
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


HELPER = Path.home() / ".codex" / "meta-ads-headers.py"
URL = "https://mcp.facebook.com/ads"


def auth_headers():
    raw = subprocess.check_output([__import__("sys").executable, str(HELPER)], text=True)
    return json.loads(raw)


def response_message(body):
    content_type = body.headers.get("Content-Type", "")
    if "text/event-stream" not in content_type:
        return json.loads(body.read().decode("utf-8"))
    for line in body.read().decode("utf-8").splitlines():
        if line.startswith("data:"):
            value = line[5:].strip()
            if value:
                return json.loads(value)
    raise RuntimeError("MCP event stream contained no data message")


def post(opener, session_id, payload):
    headers = {
        **auth_headers(),
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }
    if session_id:
        headers["Mcp-Session-Id"] = session_id
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=headers)
    try:
        with opener.open(req, timeout=60) as body:
            new_session = body.headers.get("Mcp-Session-Id")
            message = response_message(body) if body.status != 202 else None
            return body.status, new_session or session_id, message
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:1000]
        raise RuntimeError(f"MCP HTTP {exc.code}: {detail}") from exc


def initialize(opener):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "jevmax-local-probe", "version": "1.0"},
        },
    }
    status, session_id, message = post(opener, None, payload)
    if not message or "result" not in message:
        raise RuntimeError(f"MCP initialize failed: {message!r}")
    post(opener, session_id, {"jsonrpc": "2.0", "method": "notifications/initialized"})
    return session_id, message["result"]


def request(opener, session_id, method, params=None, request_id=2):
    payload = {"jsonrpc": "2.0", "id": request_id, "method": method}
    if params is not None:
        payload["params"] = params
    _, _, message = post(opener, session_id, payload)
    if message is None or "result" not in message:
        raise RuntimeError(f"MCP {method} failed: {message!r}")
    return message["result"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-tools", action="store_true")
    parser.add_argument("--call")
    parser.add_argument("--arguments", default="{}")
    args = parser.parse_args()

    opener = urllib.request.build_opener()
    session_id, init = initialize(opener)
    print(json.dumps({"connected": True, "server": init.get("serverInfo", {})}, ensure_ascii=False))

    if args.list_tools:
        result = request(opener, session_id, "tools/list")
        tools = result.get("tools", [])
        print(json.dumps({"tool_count": len(tools), "tools": [
            {"name": t.get("name"), "description": t.get("description"), "schema": t.get("inputSchema")}
            for t in tools
        ]}, ensure_ascii=False, indent=2))

    if args.call:
        result = request(opener, session_id, "tools/call", {
            "name": args.call,
            "arguments": json.loads(args.arguments),
        })
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

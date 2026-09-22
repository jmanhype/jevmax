"""Buffer MCP client (stdlib only). Talks to https://mcp.buffer.com/mcp via
JSON-RPC over streamable HTTP. Token comes from BUFFER_TOKEN (env or .env),
never from this file.

Usage:
    python3 buffer_mcp.py account
    python3 buffer_mcp.py channels
    python3 buffer_mcp.py posts
    python3 buffer_mcp.py create --channel <id> --text "caption" \
        --image https://... --at "2026-09-26T22:00:00Z"
"""
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

ENDPOINT = "https://mcp.buffer.com/mcp"
_id = [0]


def load_token():
    tok = os.environ.get("BUFFER_TOKEN")
    if tok:
        return tok.strip()
    for p in (
        Path(__file__).with_name(".env"),
        Path.home() / ".zcode/workspace/default/.env",
    ):
        if p.exists():
            for line in p.read_text().splitlines():
                if line.startswith("BUFFER_TOKEN="):
                    return line.strip().split("=", 1)[1]
    sys.exit("BUFFER_TOKEN not found (env var or .env file)")


def call(tool, arguments):
    _id[0] += 1
    body = json.dumps({
        "jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
        "params": {"name": tool, "arguments": arguments},
    }).encode()
    req = urllib.request.Request(ENDPOINT, data=body, headers={
        "Authorization": "Bearer " + load_token(),
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.load(r)
    content = data["result"]["content"]
    # tools return one or more text blocks; first is usually the payload,
    # last may be rateLimit info
    payload = content[0]["text"]
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return payload


def account():
    return call("get_account", {})


def channels(org_id):
    return call("list_channels", {"organizationId": org_id})


def posts(org_id):
    return call("list_posts", {"organizationId": org_id})


def create(channel_id, text, image=None, at=None):
    args = {"channelId": channel_id, "text": text}
    if image:
        args["assets"] = [{"type": "image", "source": image}]
    if at:
        args["scheduledAt"] = at
    return call("create_post", args)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("account")
    sub.add_parser("channels").add_argument("--org", required=True)
    sub.add_parser("posts").add_argument("--org", required=True)
    c = sub.add_parser("create")
    c.add_argument("--channel", required=True)
    c.add_argument("--text", required=True)
    c.add_argument("--image")
    c.add_argument("--at", help="ISO datetime, e.g. 2026-09-26T22:00:00Z")
    args = ap.parse_args()

    if args.cmd == "account":
        out = account()
    elif args.cmd == "channels":
        out = channels(args.org)
    elif args.cmd == "posts":
        out = posts(args.org)
    else:
        out = create(args.channel, args.text, args.image, args.at)
    print(json.dumps(out, indent=1)[:4000])


if __name__ == "__main__":
    main()

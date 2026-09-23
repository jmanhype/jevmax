#!/usr/bin/env python3
"""Generate one bible page via Kling MCP text_to_image (gemini-3-pro-image).
Usage: gen_page.py <prompt.md> <aspect_ratio> <out.png>
Prints the submission id, polls to completion, downloads the image.
"""
import json, sys, urllib.request, os

sys.path.insert(0, os.path.expanduser("~/workspace"))
from kling_mcp import generate, poll, tool_text

prompt_path, aspect, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
prompt = open(prompt_path, encoding="utf-8").read().strip()

print(f"Submitting {prompt_path} aspect={aspect} ...", flush=True)
sub = generate("text_to_image", "gemini-3-pro-image",
               {"prompt": prompt, "aspect_ratio": aspect,
                "img_resolution": "2k", "image_count": "1"},
               inputs=[])
print("SUBMISSION:", json.dumps(sub)[:400], flush=True)

gid = (sub.get("generationId") or sub.get("generation_id")
       or sub.get("id") or sub.get("taskId"))
if not gid:
    # sometimes nested
    for v in sub.values():
        if isinstance(v, dict) and ("generationId" in v or "generation_id" in v):
            gid = v.get("generationId") or v.get("generation_id")
            break
print("GID:", gid, flush=True)

task = poll(gid, timeout_s=1200, interval_s=25)
print("TASK_STATUS:", task.get("status"), flush=True)
dump_path = out_path + ".task.json"
json.dump(task, open(dump_path, "w"), indent=1)
print("task dumped to", dump_path, flush=True)

# find image urls
urls = []
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k.lower() in ("url", "imageurl", "resulturl") and isinstance(v, str) and v.startswith("http"):
                urls.append(v)
            else:
                walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(task)
# also common: task['result']['images'][*]['url']
print("URLS_FOUND:", len(urls), flush=True)
for u in urls[:4]:
    print("  ", u[:120], flush=True)

if urls:
    # prefer the last/longest (usually the final render, not a thumbnail)
    url = sorted(urls, key=len)[-1]
    print("downloading", url[:100], flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = urllib.request.urlopen(req, timeout=120).read()
    open(out_path, "wb").write(data)
    print(f"saved {out_path} ({len(data)} bytes)", flush=True)
else:
    print("NO_URLS — inspect", dump_path, flush=True)

#!/usr/bin/env python3
"""Upload bible pages to Kling and create the 'Arkady Korabelnikov' Element.
Usage: make_element.py <images_dir>
Cover = page_01; secondary = pages 02, 04, 07. Tag: Characters.
"""
import json, os, sys, urllib.request, uuid, mimetypes

sys.path.insert(0, os.path.expanduser("~/workspace"))
from kling_mcp import call_tool, tool_text

imgdir = sys.argv[1]
pages = {
    "cover": "page_01_primary_hero_reference.png",
    "secondary": ["page_02_orthographic_turnaround.png",
                  "page_04_expression_emotion_sheet.png",
                  "page_07_extremities_props_accessories.png"],
}

def upload(path):
    size = os.path.getsize(path)
    fname = os.path.basename(path)
    r = call_tool("file_upload", {"filename": fname,
                                  "contentType": "image/png",
                                  "size": size})
    info = json.loads(tool_text(r))
    ticket = info.get("ticket") or info.get("uploadTicket")
    up_url = info.get("upload_url") or info.get("uploadUrl") or info.get("url")
    print("ticket:", str(ticket)[:20], "... upload_url:", (up_url or "")[:80], flush=True)

    boundary = "----KlingBoundary" + uuid.uuid4().hex
    body = b""
    body += f"--{boundary}\r\n".encode()
    body += b'Content-Disposition: form-data; name="ticket"\r\n\r\n'
    body += ticket.encode() + b"\r\n"
    body += f"--{boundary}\r\n".encode()
    body += f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'.encode()
    body += b"Content-Type: image/png\r\n\r\n"
    body += open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(up_url, data=body, method="POST", headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}"})
    resp = urllib.request.urlopen(req, timeout=180).read().decode()
    print("upload resp:", resp[:300], flush=True)
    rd = json.loads(resp)
    # find the url
    url = rd.get("url") or rd.get("fileUrl") or rd.get("file_url")
    if not url:
        def walk(o):
            if isinstance(o, dict):
                for k, v in o.items():
                    if k.lower().endswith("url") and isinstance(v, str) and v.startswith("http"):
                        return v
                    r = walk(v)
                    if r:
                        return r
            elif isinstance(o, list):
                for v in o:
                    r = walk(v)
                    if r:
                        return r
        url = walk(rd)
    print("kling url:", (url or "")[:120], flush=True)
    return url

urls = {}
for role, fn in [("cover", pages["cover"])] + [("sec", f) for f in pages["secondary"]]:
    p = os.path.join(imgdir, fn)
    u = upload(p)
    urls.setdefault(role, []).append(u)

cover_url = urls["cover"][0]
secondary = [{"inputType": "URL", "name": f"secondary_{i+1}", "url": u}
             for i, u in enumerate(urls["sec"])]

print("calling element_create ...", flush=True)
r = call_tool("element_create", {
    "name": "Arkady Korabelnikov",
    "description": "Major Arkady Korabelnikov, 52, Soviet signals counterintelligence officer at the Object 10-D lunar listening post, 1959. Weathered WW2 veteran's face, steel-grey close-cropped hair, olive drab service tunic, major's single gilt star, service cap with red star cockade. Photorealistic 1959 16mm Kodak Ektachrome look. DIAL M FOR MOON supporting character.",
    "resource": {"cover": cover_url, "secondary": secondary},
    "tags": ["Characters"],
})
out = tool_text(r)
print("ELEMENT_CREATE_RESULT:", out[:800], flush=True)
open(os.path.join(imgdir, "element_result.json"), "w").write(out)

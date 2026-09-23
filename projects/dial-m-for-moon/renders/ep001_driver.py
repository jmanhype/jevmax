#!/usr/bin/env python3
"""EP001 pure-PixVerse render driver. Phase A: free 9:16 seed stills (gpt-image-2.5).
Phase B: v6 I2V, 5s, 720p, 9:16, 2 takes per shot. Fail-tolerant, logged.

Usage (full python path from project):
    python ep001_driver.py seeds     # phase A only (free)
    python ep001_driver.py videos    # phase B (spends ~40-50 cr/take)
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # dial-m-for-moon
BIBLES = os.path.join(ROOT, "bibles")
OUT = os.path.join(ROOT, "renders")
PIXVERSE = r"C:\Users\ged\AppData\Local\Programs\nodejs\pixverse.cmd"
VALYA_P1 = os.path.join(BIBLES, "valentina-orlova", "images", "page_01_primary_hero_reference.png")
VALYA_P5 = os.path.join(BIBLES, "valentina-orlova", "images", "page_05_cranial_appendage_details.png")
VALYA_P7 = os.path.join(BIBLES, "valentina-orlova", "images", "page_07_extremities_props_accessories.png")
KOR_P1 = os.path.join(BIBLES, "korabelnikov", "images", "page_01_primary_hero_reference.png")
REG = "1959 16mm Kodak Ektachrome reversal still, fresh print, organic grain, halation on practicals"

# (id, seed_prompt, seed_refs, motion_prompt, audio)
SHOTS = [
    ("S01", None, [VALYA_P1],  # seed = bible anchor directly
     "Slow cinematic push-in toward the seated woman, centered and symmetrical behind the vintage switchboard; "
     "her hand inserts a black plug mid-frame with one precise motion; rows of small orange lamps glow under her face; "
     "she leans in sharply toward the board. Steady, no camera shake. Period ambience: board hiss, one click, a sharp intake of breath. No speech, no music.", True),
    ("S02", "Macro insert, vertical: a 1959 Soviet switchboard frequency counter, black lacquer face, brass dial rim worn to white, "
     "the needle settling on 14, one small round orange lamp glowing beside it, cord web bokeh behind. " + REG, [VALYA_P7],
     "The needle settles on 14; the lamp filament blooms bright; a faint flicker. Locked-off macro insert, no camera motion. "
     "Room hiss drops out for one beat, then hum returns. No speech, no music.", True),
    ("S03", "Vertical close shot, 1959: a woman's pale hand hovers over a red bakelite cut-key on a black switchboard panel, "
     "a brass placard defocused above it, her grey-blue eyes sharp in the background already looking up. Ash-blonde bun, headset earcup. " + REG,
     [VALYA_P1, VALYA_P5],
     "Focus racks from the hovering hand to her eyes and back as the hand slowly withdraws from the key; micro-tremor in the fingers. "
     "Static close, no camera motion. Quiet room hum only. No speech.", False),
    ("S04", "Vertical insert: a brass placard on black lacquer reads СЕКЦИЯ 7 — НЕЗАРЕГИСТРИРОВАННЫЙ ПЕРЕХВАТ = ИЗМЕНА, scratched paint fill, "
     "and below it a red pencil held in fingers, caught mid-turn. " + REG, [VALYA_P7],
     "Slow tilt down from the placard to the red pencil turning once in the fingers. Locked-off insert. One small dry knock as the pencil "
     "leaves an ear. No speech, no music.", True),
    ("S05", "Vertical over-shoulder insert, 1959: a logbook page under warm tungsten lamp glow, a red pencil nib denting the paper mid-word, "
     "Cyrillic handwriting, the edge of a woman's jaw checking the door at frame edge. " + REG, [VALYA_P7],
     "The pencil presses and writes two more strokes, paper fiber denting; her head turns a few degrees toward the door. Slow micro push. "
     "Pencil scratch, distant corridor ambience. No speech, no music.", True),
    ("S06", "Vertical over-the-shoulder, 1959: foreground left, the back of a woman's ash-blonde head with headset earcup, soft; background, "
     "a heavy-set grey-haired officer in olive-grey uniform fills a dark corridor doorway, backlit by cold spill, peaked cap under his arm, "
     "black folder held flat. " + REG, [VALYA_P1, KOR_P1],
     "The door swing settles; the officer stands immovable in the frame; her head lifts slightly. Held over-the-shoulder framing, no camera motion. "
     "Hinges, boot heels stopping, one floor creak. No speech.", False),
    ("S07", "Vertical two-plane shot, 1959: foreground right, a woman's forearm sliding across a logbook page, sharp; background left, "
     "a heavy-set grey-haired officer's deep-set eyes over her shoulder, sharp; soft mid-ground between. Board lamps glow between them. " + REG,
     [VALYA_P1, KOR_P1],
     "Her forearm completes its slide covering the page; his chin lifts a fraction as he extends one hand. Both planes stay critically sharp. "
     "No camera motion. Low board hum between two short spoken Russian lines is NOT voiced — silence between them, room tone only. No speech.", False),
    ("S08", "Vertical insert, 1959: an open logbook held in a man's broad hands in olive-grey sleeves, one page mid-turn stopped, "
     "the page beneath blank with a fresh ink smudge under lamp light, black folder under his arm. " + REG, [KOR_P1, VALYA_P7],
     "The page turn stops mid-air and lowers flat; hold on the blank page and tacky ink smudge one full beat. Locked-off insert. "
     "Paper sound, then nothing — one beat of true silence. No speech, no music.", True),
    ("S09", "Vertical close, 1959: a woman's face soft in the background behind a logbook page held up in a man's hand in the sharp "
     "foreground; her grey-blue eyes perfectly still, parade-rest composure, ash-blonde bun, headset around her neck. " + REG,
     [VALYA_P1, KOR_P1],
     "Focus racks from the blank page to her motionless eyes and back to the page; her blink rate drops to zero; jaw sets. "
     "Static close. A single distant stove tick. No speech.", False),
    ("S10", "Vertical centered shot, 1959: the woman alone behind the switchboard bay, centered and symmetrical, ringed by rows of small "
     "orange lamps, one lamp isolated at frame top glowing steady — lamp 14; her hand rises into frame holding a red pencil. " + REG,
     [VALYA_P1],
     "Held centered framing with a slow push-in; lamp 14 flickers twice, flat, like a knock; her hand rises with the red pencil; nothing else "
     "moves. Cut to black on the second flicker. Two flat knocks of static, then silence. No speech, no music.", True),
]


def run(cmd, timeout):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        try:
            return json.loads(p.stdout)
        except json.JSONDecodeError:
            return {"status": "error", "error": (p.stdout + p.stderr)[-400:]}
    except subprocess.TimeoutExpired:
        return {"status": "error", "error": "timeout"}


def log(row):
    import csv
    exists = os.path.exists(os.path.join(OUT, "render_log.csv"))
    with open(os.path.join(OUT, "render_log.csv"), "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ts", "shot", "kind", "status", "credits", "id", "url", "local", "error"])
        if not exists:
            w.writeheader()
        row["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
        w.writerow(row)


def download(url, dest):
    d = subprocess.run(["curl", "-sL", "--max-time", "180", "-o", dest, url], capture_output=True)
    return d.returncode == 0 and os.path.exists(dest) and os.path.getsize(dest) > 10_000


def seeds():
    os.makedirs(os.path.join(OUT, "seeds"), exist_ok=True)
    for sid, seed_prompt, refs, _, _ in SHOTS:
        if sid == "S01":
            print("S01: uses bible page 1 directly (no seed gen)")
            continue
        dest = os.path.join(OUT, "seeds", f"{sid}_seed.png")
        if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
            print(f"{sid}: seed exists, skip")
            continue
        cmd = [PIXVERSE, "create", "image", "--prompt", seed_prompt, "-m", "gpt-image-2.5-flare",
               "--aspect-ratio", "9:16", "--quality", "2k", "--count", "1",
               "--idempotency-key", f"ep001-{sid}-seed", "--timeout", "300", "--json"]
        if refs:
            cmd += ["--images"] + refs
        data = run(cmd, 420)
        url = data.get("image_url") or (data.get("data") or {}).get("image_url") or data.get("url") or ""
        ok = bool(url) and download(url, dest)
        print(f"{sid}: {'OK' if ok else 'FAIL'} {data.get('status','?')} credits={data.get('cost_credits','?')}")
        log({"shot": sid, "kind": "seed", "status": "OK" if ok else data.get("status", "error"),
             "credits": data.get("cost_credits", ""), "id": data.get("image_id", ""), "url": url,
             "local": dest if ok else "", "error": "" if ok else json.dumps(data)[:200]})


def seed_for(sid):
    return VALYA_P1 if sid == "S01" else os.path.join(OUT, "seeds", f"{sid}_seed.png")


def videos():
    os.makedirs(os.path.join(OUT, "takes"), exist_ok=True)
    for sid, _, _, motion, audio in SHOTS:
        s = seed_for(sid)
        if not os.path.exists(s):
            print(f"{sid}: seed missing, skip")
            continue
        dest = os.path.join(OUT, "takes", f"{sid}_take1.mp4")
        if os.path.exists(dest) and os.path.getsize(dest) > 10_000:
            print(f"{sid}: take exists, skip")
            continue
        cmd = [PIXVERSE, "create", "video", "--prompt", motion, "--image", s,
               "-m", "v6", "--quality", "720p", "--duration", "5", "--aspect-ratio", "9:16",
               "--count", "2", "--seed", "1959", "--idempotency-key", f"ep001-{sid}-v1",
               "--timeout", "600", "--json"]
        cmd.append("--no-audio" if not audio else "--audio")
        data = run(cmd, 720)
        urls = []
        if isinstance(data.get("items"), list):
            urls = [it.get("video_url") for it in data["items"] if it.get("video_url")]
        if not urls and data.get("video_url"):
            urls = [data["video_url"]]
        ok = []
        for i, u in enumerate(urls[:2]):
            d = os.path.join(OUT, "takes", f"{sid}_take{i+1}.mp4")
            if download(u, d):
                ok.append(d)
        print(f"{sid}: {'OK' if ok else 'FAIL'} takes={len(ok)} credits={data.get('cost_credits','?')}")
        log({"shot": sid, "kind": "video", "status": "OK" if ok else data.get("status", "error"),
             "credits": data.get("cost_credits", ""), "id": str(data.get("video_id", "")), "url": ";".join(urls),
             "local": ";".join(ok), "error": "" if ok else json.dumps(data)[:200]})


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else ""
    os.makedirs(OUT, exist_ok=True)
    if phase == "seeds":
        seeds()
    elif phase == "videos":
        videos()
    else:
        sys.exit("usage: ep001_driver.py seeds|videos")

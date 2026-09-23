#!/usr/bin/env python3
"""Workflow #12 — StepFun audio layer: voices for the edit stage.

StepFun (api.stepfun.ai) is the pipeline's audio house: TTS for dialogue
(PixVerse --no-audio shots, SEVEN-THREE's bilingual mayday), music cues, ASR
for audio QC (transcribe a take, canon-check the lines). Verified 2026-09-23:
key valid on the international zone only (api.stepfun.com returns 401 for it).

Usage:
    python3 stepfun.py tts "Обычный лунный шум, товарищ майор." --out line.mp3 [--voice ID]
    python3 stepfun.py voices          # print system voice list reference
    python3 stepfun.py selftest

API shape (POST /v1/audio/speech, OpenAI-TTS style): {model, input, voice}.
Pricing: $0.36 / 10k chars (stepaudio-3-tts); cloning $1.50/voice.
Voice ids: https://platform.stepfun.ai/docs/en/guides/developer/tts
Not yet wired (documented, unverified shapes — check docs before coding):
  stepaudio-3-asr-max (SSE), stepaudio-3-music-preview,
  step-image-edit-2 (targeted bible-page fixes — the detail-gap bridge).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.stepfun.ai/v1"
TTS_MODEL = "stepaudio-3-tts"


def load_key():
    key = os.environ.get("STEPFUN_API_KEY")
    if key:
        return key.strip()
    for p in (
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
    ):
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    if line.startswith("STEPFUN_API_KEY="):
                        return line.strip().split("=", 1)[1]
    raise RuntimeError("STEPFUN_API_KEY not found (env var or jevmax/.env)")


def post(path, payload, timeout=120, max_retries=3):
    body = json.dumps(payload).encode("utf-8")
    delay = 2.0
    for attempt in range(max_retries):
        req = urllib.request.Request(
            BASE + path,
            data=body,
            headers={
                "Authorization": "Bearer " + load_key(),
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 529) and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"StepFun API HTTP {e.code}: {e.read()[:300]}") from e
        except urllib.error.URLError:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("StepFun API failed after retries")


def tts(text, out_path, voice=None):
    payload = {"model": TTS_MODEL, "input": text}
    if voice:
        payload["voice"] = voice
    data = post("/audio/speech", payload)
    with open(out_path, "wb") as f:
        f.write(data)
    print(f"wrote {out_path} ({len(data)} bytes, {len(text)} chars in)")


def voices():
    print("System voice ids: https://platform.stepfun.ai/docs/en/guides/developer/tts")
    print("Audition: https://audio.stepfun.ai/")
    print("Omit --voice for the default; clone a custom voice from ~3s of audio ($1.50/voice).")


def selftest():
    assert TTS_MODEL == "stepaudio-3-tts"
    assert BASE.endswith("/v1")
    print("stepfun selftest: PASS (constants only; no API calls)")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("tts")
    t.add_argument("text")
    t.add_argument("--out", default="speech.mp3")
    t.add_argument("--voice", default=None)
    sub.add_parser("voices")
    sub.add_parser("selftest")
    args = ap.parse_args()

    if args.cmd == "tts":
        tts(args.text, args.out, args.voice)
    elif args.cmd == "voices":
        voices()
    else:
        return selftest()
    return 0


if __name__ == "__main__":
    sys.exit(main())

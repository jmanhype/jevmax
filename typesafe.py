"""Shared TypeSafe System One client. Stdlib only — no dependencies.

Usage:
    from typesafe import ask, Usage
    answers, usage = ask(state, questions)
"""
import json
import os
import time
import urllib.error
import urllib.request

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-latest"


def load_key():
    key = os.environ.get("TYPESAFE_API_KEY")
    if key:
        return key.strip()
    for p in (
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.expanduser("~/.zcode/workspace/default/.env"),
    ):
        if os.path.exists(p):
            with open(p) as f:
                for line in f:
                    if line.startswith("TYPESAFE_API_KEY="):
                        return line.strip().split("=", 1)[1]
    raise RuntimeError("TYPESAFE_API_KEY not found (env var or .env file)")


def ask(state, questions, model=MODEL, max_retries=5, timeout=180):
    """One request: any number of independent questions over the same state.

    Returns (answers_map, usage_dict). Retries 429/529 with exponential backoff,
    matching the official SDK behavior.
    """
    body = json.dumps(
        {"state": state, "model": model, "questions": questions}
    ).encode("utf-8")
    delay = 2.0
    last_err = None
    for attempt in range(max_retries):
        req = urllib.request.Request(
            ENDPOINT,
            data=body,
            headers={
                "Authorization": "Bearer " + load_key(),
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.load(r)
            return data["answers"], data.get("usage", {})
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 529) and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"TypeSafe API HTTP {e.code}: {e.read()[:300]}") from e
        except urllib.error.URLError as e:
            last_err = e
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError(f"TypeSafe API failed after {max_retries} attempts: {last_err}")


def ask_batch(states_and_questions, workers=4, model=MODEL):
    """Run many (state, questions) requests concurrently.

    Returns (list_of_answers, merged_usage).
    """
    from concurrent.futures import ThreadPoolExecutor

    results = [None] * len(states_and_questions)
    usage = {"input_tokens": 0, "output_tokens": 0}

    def run(i):
        state, questions = states_and_questions[i]
        answers, u = ask(state, questions, model=model)
        for k in usage:
            usage[k] += u.get(k, 0)
        results[i] = answers

    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(run, range(len(states_and_questions))))
    return results, usage

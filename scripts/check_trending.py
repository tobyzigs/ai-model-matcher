# Checks app/trending.json (Trending on GitHub this week) before it is published.
# Usage: python3 -I scripts/check_trending.py [path]   (exit 0 = good; otherwise prints every problem)
import json
import re
import sys

REQUIRED = ("name", "what", "stars_week", "stars", "url")
NAME = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def problems(doc):
    out = []
    if not isinstance(doc, dict):
        return ["the file must hold one JSON object"]
    if not DATE.match(str(doc.get("updated", ""))):
        out.append('"updated" must be a date like 2026-11-30')
    if not str(doc.get("week", "")).startswith("Week of "):
        out.append('"week" must read "Week of <Month D, YYYY>"')
    repos = doc.get("repos")
    if not isinstance(repos, list):
        return out + ['"repos" must be a list']
    if len(repos) > 10:
        out.append(f'"repos" has {len(repos)} entries; the most is 10')
    seen = set()
    for i, r in enumerate(repos, 1):
        if not isinstance(r, dict):
            out.append(f"entry {i} is not an object")
            continue
        for k in REQUIRED:
            if not isinstance(r.get(k), str) or not r[k].strip():
                out.append(f'entry {i} needs "{k}"')
        name = str(r.get("name", ""))
        if not NAME.match(name):
            out.append(f'entry {i}: "name" must be owner/repo, got {name!r}')
        elif r.get("url") != "https://github.com/" + name:
            out.append(f'entry {i}: "url" must be https://github.com/{name}')
        if name.lower() in seen:
            out.append(f"entry {i}: {name} is listed twice")
        seen.add(name.lower())
        if len(str(r.get("what", "")).split()) > 20:
            out.append(f'entry {i}: "what" is over 20 words')
        if "early" in r and not isinstance(r["early"], bool):
            out.append(f'entry {i}: "early" must be true or false')
    return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "app/trending.json"
    with open(path, encoding="utf-8") as f:
        found = problems(json.load(f))
    for p in found:
        print("Problem:", p)
    sys.exit(1 if found else 0)

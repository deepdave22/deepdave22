"""Refresh the 'Recently active' section of README.md with the latest pushed repos."""
import json
import os
import re
import urllib.request

USER = os.environ.get("GITHUB_REPOSITORY_OWNER", "deepdave22")
START, END = "<!-- RECENT:START -->", "<!-- RECENT:END -->"

req = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=30",
    headers={"Accept": "application/vnd.github+json"},
)
with urllib.request.urlopen(req) as resp:
    repos = json.load(resp)

rows = [r for r in repos if r["name"] != USER and not r["fork"]][:5]
lines = ["| Repo | Language | Last push |", "|---|---|---|"]
for r in rows:
    desc = f" - {r['description']}" if r["description"] else ""
    lines.append(
        f"| [{r['name']}]({r['html_url']}){desc} | {r['language'] or '-'} | {r['pushed_at'][:10]} |"
    )

with open("README.md", encoding="utf-8") as f:
    text = f.read()

block = f"{START}\n" + "\n".join(lines) + f"\n{END}"
new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)

if new != text:
    with open("README.md", "w", encoding="utf-8", newline="\n") as f:
        f.write(new)

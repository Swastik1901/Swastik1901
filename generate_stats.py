#!/usr/bin/env python3
"""Fetch live GitHub stats via GraphQL and render profile-stats/stats.svg (no dependencies)."""
import json
import os
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import escape

USER = os.environ.get("USERNAME", "Swastik1901")
TOKEN = os.environ["GITHUB_TOKEN"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    name
    followers { totalCount }
    repositories(ownerAffiliation: OWNER, isFork: false, first: 100) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    pullRequests { totalCount }
    issues { totalCount }
    contributionsCollection {
      totalCommitContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(payload["errors"])
    return payload["data"]["user"]


def streaks(days):
    days = sorted(days, key=lambda d: d["date"])
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    # current streak: walk back from today (today may still be 0)
    counts = {d["date"]: d["contributionCount"] for d in days}
    cur, day = 0, date.today()
    if counts.get(day.isoformat(), 0) == 0:
        day -= timedelta(days=1)
    while counts.get(day.isoformat(), 0) > 0:
        cur += 1
        day -= timedelta(days=1)
    return cur, longest


def main():
    u = fetch()
    repos = u["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    cc = u["contributionsCollection"]
    cal = cc["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    cur, longest = streaks(days)

    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]
            item = langs.setdefault(n["name"], {"size": 0, "color": n["color"] or "#8b949e"})
            item["size"] += e["size"]
    total = sum(v["size"] for v in langs.values()) or 1
    top = sorted(langs.items(), key=lambda kv: -kv[1]["size"])[:5]

    rows = [
        ("Stars earned", stars),
        ("Commits (last 12 mo)", cc["totalCommitContributions"]),
        ("Pull requests", u["pullRequests"]["totalCount"]),
        ("Issues", u["issues"]["totalCount"]),
        ("Public repos", u["repositories"]["totalCount"]),
        ("Followers", u["followers"]["totalCount"]),
    ]

    W, H = 840, 300
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0e75b6"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="#1a1b27"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="url(#g)" stroke-width="2"/>',
        '<style>text{font-family:"Segoe UI",Ubuntu,Arial,sans-serif}'
        '.t{font-size:20px;font-weight:700;fill:#a78bfa}.l{font-size:14px;fill:#c0caf5}'
        '.v{font-size:14px;font-weight:700;fill:#7dcfff}.big{font-size:34px;font-weight:700;fill:#a78bfa}'
        '.s{font-size:12px;fill:#9aa5ce}</style>',
        f'<text x="28" y="40" class="t">{escape(u["name"] or USER)}\'s GitHub Stats</text>',
    ]
    for i, (k, v) in enumerate(rows):
        y = 78 + i * 28
        out.append(f'<text x="28" y="{y}" class="l">{escape(k)}</text>')
        out.append(f'<text x="220" y="{y}" class="v" text-anchor="end">{v}</text>')

    # streak block
    out += [
        '<line x1="250" y1="60" x2="250" y2="240" stroke="#3b3d57"/>',
        f'<text x="330" y="110" class="big" text-anchor="middle">{cal["totalContributions"]}</text>',
        '<text x="330" y="132" class="s" text-anchor="middle">Contributions (12 mo)</text>',
        f'<text x="330" y="190" class="big" text-anchor="middle">{cur}</text>',
        '<text x="330" y="212" class="s" text-anchor="middle">Current streak (days)</text>',
        f'<text x="450" y="190" class="big" text-anchor="middle">{longest}</text>',
        '<text x="450" y="212" class="s" text-anchor="middle">Longest streak</text>',
        '<line x1="520" y1="60" x2="520" y2="240" stroke="#3b3d57"/>',
        '<text x="545" y="78" class="t" style="font-size:16px">Top languages</text>',
    ]
    # language bars
    x0, bw = 545, 270
    for i, (name, d) in enumerate(top):
        pct = d["size"] / total * 100
        y = 104 + i * 30
        out.append(f'<text x="{x0}" y="{y}" class="l">{escape(name)}</text>')
        out.append(f'<text x="{x0+bw}" y="{y}" class="s" text-anchor="end">{pct:.1f}%</text>')
        out.append(f'<rect x="{x0}" y="{y+6}" width="{bw}" height="6" rx="3" fill="#2a2b3d"/>')
        out.append(f'<rect x="{x0}" y="{y+6}" width="{max(bw*pct/100,3):.1f}" height="6" rx="3" fill="{d["color"]}"/>')

    stamp = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    out.append(f'<text x="{W-20}" y="{H-14}" class="s" text-anchor="end">Updated {stamp}</text>')
    out.append("</svg>")

    os.makedirs("profile-stats", exist_ok=True)
    with open("profile-stats/stats.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print("stats.svg written")


if __name__ == "__main__":
    main()

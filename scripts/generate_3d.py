#!/usr/bin/env python3
"""Render a 3D isometric contribution graph to profile-3d-contrib/profile-3d.svg (no dependencies)."""
import json
import os
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("USERNAME", "Swastik1901")

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""

# top-face colours per level (0 = no contributions)
LEVELS = ["#2a2d45", "#0e75b6", "#3a8fd9", "#7c3aed", "#a78bfa"]


def shade(hex_color, f):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def level(count, mx):
    if count == 0:
        return 0
    q = count / mx
    return 1 if q <= 0.25 else 2 if q <= 0.5 else 3 if q <= 0.75 else 4


def build_svg(weeks, total, user):
    p = 17.0
    Wv = (p, p * 0.28)            # one week step (left -> right, slight tilt)
    Dv = (-p * 0.5, p * 0.48)     # one weekday step (towards the viewer)
    k = 0.9                       # tile size (leaves a gap between bars)
    max_h = 95.0
    counts = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    mx = max(counts) if counts and max(counts) > 0 else 1

    cells = []
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            di = d["weekday"]
            c = d["contributionCount"]
            X = wi * Wv[0] + di * Dv[0]
            Y = wi * Wv[1] + di * Dv[1]
            h = 3 + (c / mx) * max_h if c else 2
            cells.append((Y, X, h, level(c, mx)))
    cells.sort(key=lambda t: (t[0], t[1]))   # far -> near

    ax_, ay_ = Wv[0] * k, Wv[1] * k
    bx_, by_ = Dv[0] * k, Dv[1] * k
    min_x = min(c[1] for c in cells) + min(0, bx_) - 30
    max_x = max(c[1] for c in cells) + ax_ + 30
    min_y = min(c[0] - c[2] for c in cells) - 80
    max_y = max(c[0] for c in cells) + ay_ + by_ + 30
    W, H = max_x - min_x, max_y - min_y

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x:.0f} {min_y:.0f} {W:.0f} {H:.0f}" '
        f'width="{W:.0f}" height="{H:.0f}">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#14151f"/><stop offset="1" stop-color="#1c1633"/></linearGradient></defs>',
        f'<rect x="{min_x:.0f}" y="{min_y:.0f}" width="{W:.0f}" height="{H:.0f}" rx="16" fill="url(#bg)"/>',
        '<style>text{font-family:"Segoe UI",Ubuntu,Arial,sans-serif}</style>',
        f'<text x="{min_x + 28:.0f}" y="{min_y + 40:.0f}" fill="#a78bfa" font-size="22" font-weight="700">'
        f'{total} contributions in the last year</text>',
        f'<text x="{min_x + 28:.0f}" y="{min_y + 60:.0f}" fill="#9aa5ce" font-size="12">'
        f'@{user} &#183; updated {datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")}</text>',
    ]

    def poly(pts, fill):
        s_ = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        return f'<polygon points="{s_}" fill="{fill}"/>'

    for Y, X, h, lv in cells:
        top = LEVELS[lv]
        left, right = shade(top, 0.62), shade(top, 0.8)
        P = (X, Y - h)                       # back-left corner of the top face
        P1 = (P[0] + ax_, P[1] + ay_)        # + week vector
        P2 = (P1[0] + bx_, P1[1] + by_)      # front-right
        P3 = (P[0] + bx_, P[1] + by_)        # front-left
        down = lambda q: (q[0], q[1] + h)
        out.append(poly([P3, P2, down(P2), down(P3)], left))     # front face
        out.append(poly([P1, P2, down(P2), down(P1)], right))    # right face
        out.append(poly([P, P1, P2, P3], top))                   # top face
    out.append("</svg>")
    return "\n".join(out)


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(payload["errors"])
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["weeks"], cal["totalContributions"]


def main():
    weeks, total = fetch(os.environ["GITHUB_TOKEN"])
    os.makedirs("profile-3d-contrib", exist_ok=True)
    with open("profile-3d-contrib/profile-3d.svg", "w", encoding="utf-8") as f:
        f.write(build_svg(weeks, total, USER))
    print("profile-3d.svg written")


if __name__ == "__main__":
    main()

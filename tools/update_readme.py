"""Fill the stats section of README.md: solved count per platform and language, the 10 latest files.
Ratings are added when you set the handles below (Codeforces and AtCoder have public APIs).
Usage:  python tools/update_readme.py"""
import os, re, json, urllib.request, datetime
CODEFORCES = ""   # your handle
ATCODER = ""      # your handle
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = {".cpp": "C++", ".cc": "C++", ".c": "C", ".java": "Java", ".py": "Python"}
rows, files = {}, []
for d in ["cses", "leetcode", "codeforces", "atcoder", "project-euler"]:
    for dp, _, fs in os.walk(os.path.join(ROOT, d)):
        for f in fs:
            lang = EXT.get(os.path.splitext(f)[1])
            if not lang: continue
            rows.setdefault(d, {}).setdefault(lang, 0); rows[d][lang] += 1
            p = os.path.join(dp, f); files.append((os.path.getmtime(p), os.path.relpath(p, ROOT).replace(os.sep, "/")))
def get(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as r: return json.load(r)
    except Exception: return None
lines = []
total = sum(sum(v.values()) for v in rows.values())
lines.append(f"**{total} problems solved** · updated {datetime.date.today():%Y-%m-%d}")
rat = []
if CODEFORCES:
    j = get(f"https://codeforces.com/api/user.info?handles={CODEFORCES}")
    if j and j.get("status") == "OK": rat.append(f"Codeforces {j['result'][0].get('rating', 'unrated')}")
if ATCODER:
    j = get(f"https://atcoder.jp/users/{ATCODER}/history/json")
    if j: rat.append(f"AtCoder {j[-1]['NewRating']}")
if rat: lines.append("Ratings: " + " · ".join(rat))
lines += ["", "| Platform | C++ | C | Java | Python | Total |", "| --- | --- | --- | --- | --- | --- |"]
for d, v in rows.items():
    lines.append(f"| {d} | " + " | ".join(str(v.get(l, "")) for l in ["C++", "C", "Java", "Python"]) + f" | {sum(v.values())} |")
lines += ["", "Latest:"] + [f"- [{p}]({p})" for _, p in sorted(files, reverse=True)[:10]]
readme = os.path.join(ROOT, "README.md"); t = open(readme, encoding="utf-8").read()
t = re.sub(r"<!-- stats:start -->.*?<!-- stats:end -->", "<!-- stats:start -->\n" + "\n".join(lines) + "\n<!-- stats:end -->", t, flags=re.S)
open(readme, "w", encoding="utf-8").write(t); print("README updated:", total, "solutions")

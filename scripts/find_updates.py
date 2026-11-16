import os
import requests
import re
import json
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from sqlite_version import SQLiteVersion

root_dir = Path(__file__).parent.parent
with open(
    os.path.join(root_dir, "sqlite3_native_library/src/main/cpp/CMakeLists.txt")
) as f:
    start_sort_key = re.search(r"sqlite-autoconf-(\d+)\.tar\.gz", f.read()).group(1)

soup = BeautifulSoup(
    requests.get("https://sqlite.org/chronology.html", timeout=30).text, "lxml"
)

versions = []
anchor_found = False
for row in soup.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) >= 2:
        date = cells[0].get_text(strip=True)
        version = cells[1].get_text(strip=True)
        sort_key = cells[1].get("data-sortkey")
        if sort_key == start_sort_key:
            anchor_found = True
            break
        year = date.split("-")[0]
        versions.append(
            SQLiteVersion(
                version=version,
                date=date,
                release_log=f"https://sqlite.org/releaselog/{version.replace('.', '_')}.html",
                url=f"https://sqlite.org/{year}/sqlite-autoconf-{sort_key}.tar.gz",
            )
        )

if not anchor_found:
    print(
        f"未在年表中找到当前版本锚点 {start_sort_key}，可能页面结构或版本号格式已变化，跳过本次检查",
        file=sys.stderr,
    )
    print("[]")
    sys.exit(0)

versions.reverse()


def tarball_exists(url: str) -> bool:
    try:
        return (
            requests.head(url, timeout=10, allow_redirects=True).status_code == 200
        )
    except requests.RequestException as e:
        print(f"校验 {url} 失败：{e}", file=sys.stderr)
        return False


# 官网只为主线的最新版本发布 autoconf 包，旧分支补丁等没有对应 tarball，直接过滤
versions = [v for v in versions if tarball_exists(v.url)]

limit = int(sys.argv[1]) if len(sys.argv) > 1 else len(versions)
versions = versions[:limit]

print(json.dumps([v.__dict__ for v in versions], ensure_ascii=False, indent=2))
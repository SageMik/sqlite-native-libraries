import re
import json
import sys
from pathlib import Path
from sqlite_version import SQLiteVersion

version_data = json.loads(sys.argv[1])
version = SQLiteVersion(**version_data)
root_dir = Path(__file__).parent.parent
replacements = [
    {
        "file": root_dir / "sqlite3_native_library/src/main/cpp/CMakeLists.txt",
        "pattern": r"URL https://sqlite\.org/\d{4}/sqlite-autoconf-\d+\.tar\.gz",
        "replacement": f"URL {version.url}",
    },
    {
        "file": root_dir / "sqlite3_native_library/oh-package.json5",
        "pattern": r'"version": "[^"]+"',
        "replacement": f'"version": "{version.version}"',
    },
    {
        "file": root_dir / "sqlite3_native_library/CHANGELOG.md",
        "mode": "prepend",
        "content": f"""## {version.version}

更新至 **SQLite: [{version.version}]({version.release_log}) ({version.date})** 。

""",
    },
]

for item in replacements:
    with open(item["file"], "r", encoding="utf-8") as f:
        content = f.read()

    if "mode" in item and item["mode"] == "prepend":
        content = item["content"] + content
    else:
        content = re.sub(item["pattern"], item["replacement"], content)

    with open(item["file"], "w", encoding="utf-8") as f:
        f.write(content)

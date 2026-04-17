#!/usr/bin/env python3
import requests, re, json
from bs4 import BeautifulSoup

with open('sqlite3_native_library/src/main/cpp/CMakeLists.txt') as f:
    start_sort_key = re.search(r'sqlite-autoconf-(\d+)\.tar\.gz', f.read()).group(1)

soup = BeautifulSoup(requests.get('https://sqlite.org/chronology.html', timeout=30).text, 'lxml')

versions = []
for row in soup.find_all('tr'):
    cells = row.find_all('td')
    if len(cells) >= 2:
        date = cells[0].get_text(strip=True)
        ver = cells[1].get_text(strip=True)
        sort_key = cells[1].get('data-sortkey')
        if sort_key == start_sort_key:
            break
        year = date.split('-')[0]
        versions.append({
            "date": date,
            "version": ver,
            "url": f"https://sqlite.org/{year}/sqlite-autoconf-{sort_key}.tar.gz"
        })

versions.reverse()
print(json.dumps(versions, ensure_ascii=False, indent=2))

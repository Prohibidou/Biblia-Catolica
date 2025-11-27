import urllib.request
import json
import os

urls = [
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/json/SpaPlatense.json",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/csv/SpaPlatense.csv",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/formats/txt/SpaPlatense.txt",
    "https://raw.githubusercontent.com/scrollmapper/bible_databases/master/json/SpaPlatense.json", # Fallback
]

for url in urls:
    try:
        print(f"Trying {url}...")
        with urllib.request.urlopen(url) as response:
            data = response.read()
            ext = url.split('.')[-1]
            output_file = f"scripts/SpaPlatense.{ext}"
            with open(output_file, 'wb') as f:
                f.write(data)
            print(f"Success! Downloaded to {output_file}")
            break
    except Exception as e:
        print(f"Failed {url}: {e}")

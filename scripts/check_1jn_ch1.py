import sqlite3
import gzip
import shutil
import os

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_check_1jn.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check 1 John chapter 1
cursor.execute("SELECT verse, text FROM verses WHERE book='1JN' AND chapter=1 ORDER BY verse LIMIT 10")
rows = cursor.fetchall()

print("1 John Chapter 1 verses:")
for r in rows:
    print(f"{r[0]}: {r[1][:80]}...")

# Check if verse 1 exists
cursor.execute("SELECT COUNT(*) FROM verses WHERE book='1JN' AND chapter=1 AND verse=1")
count = cursor.fetchone()[0]
print(f"\n1 John 1:1 exists: {count > 0}")

conn.close()
os.remove(db_path)

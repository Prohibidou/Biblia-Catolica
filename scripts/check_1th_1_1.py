import sqlite3
import gzip
import shutil
import os

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_check.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check 1 Thessalonians 1:1
cursor.execute("SELECT verse, text, comment FROM verses WHERE book='1TH' AND chapter=1 AND verse=1")
row = cursor.fetchone()

if row:
    print(f"1 Thessalonians 1:1")
    print(f"Verse: {row[0]}")
    print(f"Text: {row[1]}")
    print(f"Comment: {row[2][:100] if row[2] else 'No comment'}...")
else:
    print("Not found")

conn.close()
os.remove(db_path)

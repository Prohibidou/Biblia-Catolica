import sqlite3
import gzip
import shutil
import os

# Decompress first
gz_path = "public/bibles/straubinger.sqlite.gz"
db_path = "scripts/temp_straubinger.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
        
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT verse, text, comment FROM verses WHERE book='GEN' AND chapter=1 LIMIT 5")
rows = cursor.fetchall()

for r in rows:
    print(f"Verse {r[0]}: {r[1][:50]}...")
    if r[2]:
        print(f"  Comment: {r[2][:100]}...")
    else:
        print("  No comment")
        
conn.close()
os.remove(db_path)

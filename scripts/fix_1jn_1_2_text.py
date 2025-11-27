import sqlite3
import gzip
import shutil
import os

# Text for 1 John 1:2
correct_1_2_text = "pues la vida se manifestó, y nosotros la hemos visto y damos testimonio y os anunciamos la vida eterna que estaba junto al Padre y se nos manifestó"

print("Fixing 1 John 1:2 text...")

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_fix_1jn.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# First check what we have
cursor.execute("SELECT verse, text FROM verses WHERE book='1JN' AND chapter=1 ORDER BY verse LIMIT 5")
print("\nBefore fix:")
for r in cursor.fetchall():
    print(f"  1:{r[0]} - {r[1][:60]}...")

# Update verse 2
cursor.execute(
    "UPDATE verses SET text = ? WHERE book = '1JN' AND chapter = 1 AND verse = 2",
    (correct_1_2_text,)
)

print(f"\nUpdated {cursor.rowcount} verse(s)")

# Verify
cursor.execute("SELECT verse, text FROM verses WHERE book='1JN' AND chapter=1 ORDER BY verse LIMIT 5")
print("\nAfter fix:")
for r in cursor.fetchall():
    print(f"  1:{r[0]} - {r[1][:60]}...")

conn.commit()
conn.close()

# Recompress
print("\nRecompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")

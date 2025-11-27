import sqlite3
import gzip
import shutil
import os

# Correct text for 1 Thessalonians 1:1
correct_text = "Pablo, Silvano y Timoteo, a la iglesia de los tesalonicenses, en Dios Padre y en el Señor Jesucristo: la gracia y la paz estén con vosotros."

print("Fixing 1 Thessalonians 1:1 text...")

# Decompress
gz_path = "public/bibles/navarra.sqlite.gz"
db_path = "scripts/temp_fix_1th.sqlite"

with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Update the text
cursor.execute(
    "UPDATE verses SET text = ? WHERE book = '1TH' AND chapter = 1 AND verse = 1",
    (correct_text,)
)

print(f"Updated {cursor.rowcount} verse(s)")

# Verify
cursor.execute("SELECT verse, text, comment FROM verses WHERE book='1TH' AND chapter=1 AND verse=1")
row = cursor.fetchone()

if row:
    print(f"\nVerification:")
    print(f"Verse: {row[0]}")
    print(f"Text: {row[1]}")
    print(f"Comment: {row[2][:100] if row[2] else 'No comment'}...")

conn.commit()
conn.close()

# Recompress
print("\nRecompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")

import sqlite3
import gzip
import shutil
import os

# Paths
gz_path = 'public/bibles/navarra.sqlite.gz'
db_path = 'scripts/temp_check_john.sqlite'

print(f"Decompressing {gz_path}...")
with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\nChecking John comments in 'comments' table:")
# Check a sample chapter, e.g., John 1
cursor.execute("SELECT verse_start, verse_end, text FROM comments WHERE book='JHN' AND chapter=1 ORDER BY verse_start LIMIT 5")
rows = cursor.fetchall()

if not rows:
    print("No comments found in 'comments' table for John 1. Checking 'verses' table...")
    cursor.execute("SELECT verse, comment FROM verses WHERE book='JHN' AND chapter=1 AND comment IS NOT NULL LIMIT 3")
    v_rows = cursor.fetchall()
    for r in v_rows:
        print(f"Verse {r[0]}: {r[1][:100]}...")
else:
    for r in rows:
        print(f"Verses {r[0]}-{r[1]}: {r[2][:100]}...")
        # Check for potential separators inside the text
        if '<br>' in r[2]:
            print("  -> Contains <br>")
        if '\n' in r[2]:
            print("  -> Contains \\n")
        if 'COMENTARIO' in r[2]:
            print("  -> Contains 'COMENTARIO'")

conn.close()
os.remove(db_path)

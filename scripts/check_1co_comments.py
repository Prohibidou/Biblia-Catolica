import sqlite3
import gzip
import shutil
import os

def check_comments(bible_name, gz_path):
    print(f"\n=== Checking {bible_name} ===")
    
    # Decompress
    db_path = f"scripts/temp_{bible_name}.sqlite"
    with gzip.open(gz_path, 'rb') as f_in:
        with open(db_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check 1 Corinthians (1CO)
    cursor.execute("SELECT verse, text, comment FROM verses WHERE book='1CO' AND chapter=1 LIMIT 5")
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ No verses found for 1 Corinthians!")
    else:
        print(f"✅ Found {len(rows)} verses in 1 Corinthians chapter 1")
        for r in rows:
            print(f"\nVerse {r[0]}: {r[1][:50]}...")
            if r[2]:
                print(f"  Comment: {r[2][:100]}...")
            else:
                print("  ❌ No comment")
    
    # Count total comments in 1CO
    cursor.execute("SELECT COUNT(*) FROM verses WHERE book='1CO' AND comment IS NOT NULL AND comment != ''")
    count = cursor.fetchone()[0]
    print(f"\nTotal verses with comments in 1 Corinthians: {count}")
    
    # Count total verses in 1CO
    cursor.execute("SELECT COUNT(*) FROM verses WHERE book='1CO'")
    total = cursor.fetchone()[0]
    print(f"Total verses in 1 Corinthians: {total}")
    
    conn.close()
    os.remove(db_path)

# Check both Bibles
check_comments("Straubinger", "public/bibles/straubinger.sqlite.gz")
check_comments("Navarra", "public/bibles/navarra.sqlite.gz")

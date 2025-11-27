import sqlite3
import gzip
import shutil
import os
import json
import re

# Paths
gz_path = 'public/bibles/navarra.sqlite.gz'
db_path = 'scripts/temp_rebuild_comments.sqlite'
json_path = 'scripts/navarra_final_merged.json'

print(f"Decompressing {gz_path}...")
with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Backup Jude and Philemon comments (since we manually fixed them)
print("Backing up Jude and Philemon comments...")
cursor.execute("SELECT book, chapter, verse_start, verse_end, text FROM comments WHERE book IN ('JUD', 'PHM')")
manual_comments = cursor.fetchall()
print(f"Backed up {len(manual_comments)} comments for JUD/PHM.")

# 2. Clear comments table
print("Clearing comments table...")
cursor.execute("DELETE FROM comments")

# 3. Load JSON and parse comments
print("Loading JSON...")
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)
    data = json_data['data']

print("Processing comments from JSON...")
# Regex to find references at the end of string
# Pattern: Book Abbrev + space + Chapter,Verse(-Chapter,Verse or -Verse)
# We need to capture groups to parse logic
# Group 1: Book
# Group 2: Start Chapter
# Group 3: Start Verse
# Group 4: End Chapter (optional)
# Group 5: End Verse (optional)
# e.g. Gn 1,1 -> 1, 1, None, None
# e.g. Gn 1,3-5 -> 1, 3, None, 5 (Wait, regex logic needs to be precise)

# Improved regex
# Matches: "Gn 1,1", "Gn 1,3-5", "Gn 1,1-2,4"
ref_pattern = re.compile(r'([1-4]?\s?[A-Za-z]+)\s+(\d+),(\d+)(?:-(\d+)(?:,(\d+))?)?[a-z]?\s*$')

count = 0
skipped_jud_phm = 0

for item in data:
    book = item['book']
    # Skip JUD and PHM from JSON processing
    if book in ['JUD', 'PHM', 'Judas', 'Filemón', 'Jud', 'Flm']:
        skipped_jud_phm += 1
        continue
        
    if 'comment' in item and item['comment']:
        text = item['comment'].strip()
        chapter = item['chapter']
        verse = item['verse']
        
        # Default range is just the verse itself
        v_start = verse
        v_end = verse
        
        # Try to parse range from text end
        match = ref_pattern.search(text[-30:])
        if match:
            # We found a reference!
            # Groups: 1=Book, 2=Ch, 3=V_start, 4=End_Part1, 5=End_Part2
            
            # Logic:
            # If 1,3-5 -> Ch=1, V=3, End=5 (Group 4 is 5, Group 5 is None)
            # If 1,1-2,4 -> Ch=1, V=1, EndCh=2, EndV=4 (Group 4 is 2, Group 5 is 4)
            
            g2 = int(match.group(2)) # Start Chapter
            g3 = int(match.group(3)) # Start Verse
            g4 = match.group(4)      # End Part 1
            g5 = match.group(5)      # End Part 2
            
            # Verify chapter matches current chapter (sanity check)
            if g2 == chapter:
                v_start = g3
                
                if g5:
                    # Format: Ch,V-Ch,V (e.g. 1,1-2,4)
                    # This implies cross-chapter comment.
                    # Our DB structure supports verse_start/end but assumes same chapter?
                    # Actually table has 'chapter' column.
                    # If comment spans chapters, we have a problem with current schema.
                    # But usually comments are attached to the starting verse's chapter.
                    # Let's assume we only care about verses in THIS chapter for now, 
                    # or if it spans, we just mark it to the end of this chapter?
                    # Complex. Let's look at simple case first.
                    
                    end_ch = int(g4)
                    end_v = int(g5)
                    
                    if end_ch == chapter:
                        v_end = end_v
                    else:
                        # Spans chapters. For now, let's just set end to a high number?
                        # Or just ignore cross-chapter logic and set to start verse?
                        # Let's keep it simple: if cross chapter, just use start verse to avoid UI bugs
                        # unless we handle cross-chapter comments in UI.
                        pass
                elif g4:
                    # Format: Ch,V-V (e.g. 1,3-5)
                    v_end = int(g4)
                else:
                    # Format: Ch,V (e.g. 1,1)
                    v_end = v_start
            
            # Remove the reference from the text?
            # User might want to keep it as citation. Let's keep it.
            
        # Insert
        cursor.execute(
            "INSERT INTO comments (book, chapter, verse_start, verse_end, text) VALUES (?, ?, ?, ?, ?)",
            (book, chapter, v_start, v_end, text)
        )
        count += 1

print(f"Inserted {count} comments from JSON.")
print(f"Skipped {skipped_jud_phm} items for JUD/PHM.")

# 4. Restore Jude and Philemon
print("Restoring Jude and Philemon comments...")
for c in manual_comments:
    cursor.execute(
        "INSERT INTO comments (book, chapter, verse_start, verse_end, text) VALUES (?, ?, ?, ?, ?)",
        (c[0], c[1], c[2], c[3], c[4])
    )
print("Restored manual comments.")

conn.commit()
conn.close()

# Recompress
print("Recompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")

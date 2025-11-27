import sqlite3
import gzip
import shutil
import os

# Paths
gz_path = 'public/bibles/navarra.sqlite.gz'
db_path = 'scripts/temp_migration.sqlite'

print(f"Decompressing {gz_path}...")
with gzip.open(gz_path, 'rb') as f_in:
    with open(db_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Create comments table
print("Creating comments table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse_start INTEGER NOT NULL,
    verse_end INTEGER NOT NULL,
    text TEXT NOT NULL
)
''')

# Create index for faster lookups
cursor.execute('CREATE INDEX IF NOT EXISTS idx_comments_book_ch ON comments (book, chapter)')

# 2. Process verses to extract and group comments
print("Processing comments...")

# Get all verses with comments
cursor.execute("SELECT book, chapter, verse, comment FROM verses WHERE comment IS NOT NULL AND comment != '' ORDER BY book, chapter, verse")
rows = cursor.fetchall()

# Helper to split comments
def split_comments(text):
    if not text:
        return []
    # Split by <br><br> and clean up
    parts = text.split('<br><br>')
    return [p.strip() for p in parts if p.strip()]

# We will process book by book, chapter by chapter
current_book = None
current_chapter = None
chapter_verses = []

def process_chapter(book, chapter, verses_data):
    if not verses_data:
        return

    # 1. Expand comments for each verse: {verse_num: [comment_text_1, comment_text_2, ...]}
    verse_comments_map = {}
    for v_num, v_comment in verses_data:
        verse_comments_map[v_num] = split_comments(v_comment)

    # 2. Identify unique comments and their ranges
    # We'll iterate through verses and try to extend ranges for each comment text found
    
    # Set of (verse_num, comment_index) that have been processed
    processed = set()
    
    # Sort verses to ensure order
    sorted_verses = sorted(verse_comments_map.keys())
    
    new_comments = []

    for v_num in sorted_verses:
        comments_list = verse_comments_map[v_num]
        
        for idx, comment_text in enumerate(comments_list):
            key = (v_num, idx)
            if key in processed:
                continue
            
            # Start a new comment range
            start = v_num
            end = v_num
            
            processed.add(key)
            
            # Look ahead to extend range
            # We look for the SAME text in the SAME relative position (idx) or just present?
            # Strict approach: same text must be present.
            # To handle the case where V17 has [A, B] and V20 has [A], we should look for 'A' in subsequent verses.
            # But we must be careful not to merge distinct occurrences.
            # Since we are processing sequentially, we extend as long as the next verse ALSO has this comment text.
            
            next_v_idx = sorted_verses.index(v_num) + 1
            while next_v_idx < len(sorted_verses):
                next_v = sorted_verses[next_v_idx]
                
                # Check if verses are contiguous (optional, but usually comments are for contiguous ranges)
                # If there is a gap in verses (e.g. 17, 19), should we stop? 
                # Usually yes, unless the missing verse just doesn't exist in DB (unlikely for contiguous range).
                # Let's assume contiguous logic: next_v should be end + 1 ideally, 
                # but sometimes verses are skipped in numbering. 
                # We'll just check if the next available verse in our map contains the text.
                
                next_v_comments = verse_comments_map[next_v]
                
                # Check if comment_text exists in next_v_comments
                # We also want to "consume" it from the next verse so it's not treated as a new comment later
                # But a comment text might appear multiple times? Unlikely for the exact same long text.
                
                if comment_text in next_v_comments:
                    # Find which index it is at
                    next_c_idx = next_v_comments.index(comment_text)
                    next_key = (next_v, next_c_idx)
                    
                    if next_key not in processed:
                        end = next_v
                        processed.add(next_key)
                        next_v_idx += 1
                    else:
                        # Already processed (maybe part of another overlapping range? unlikely with this logic)
                        break
                else:
                    break
            
            new_comments.append({
                'book': book,
                'chapter': chapter,
                'verse_start': start,
                'verse_end': end,
                'text': comment_text
            })

    # Insert into DB
    for c in new_comments:
        cursor.execute(
            "INSERT INTO comments (book, chapter, verse_start, verse_end, text) VALUES (?, ?, ?, ?, ?)",
            (c['book'], c['chapter'], c['verse_start'], c['verse_end'], c['text'])
        )

# Main loop
for row in rows:
    book, chapter, verse, comment = row
    
    if book != current_book or chapter != current_chapter:
        # Process previous chapter
        if current_book:
            process_chapter(current_book, current_chapter, chapter_verses)
        
        current_book = book
        current_chapter = chapter
        chapter_verses = []
    
    chapter_verses.append((verse, comment))

# Process last chapter
if current_book:
    process_chapter(current_book, current_chapter, chapter_verses)

conn.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM comments")
count = cursor.fetchone()[0]
print(f"Migrated {count} comments to new table.")

# Check Jude specifically
print("\nChecking Jude comments:")
cursor.execute("SELECT verse_start, verse_end, text FROM comments WHERE book='JUD' ORDER BY verse_start")
for r in cursor.fetchall():
    print(f"  Verses {r[0]}-{r[1]}: {r[2][:50]}...")

# 3. Cleanup (Optional: remove comment column from verses? No, just set to NULL to save space)
# User said "cada comentario debe ser uno individualmente... en el backend".
# Keeping the old column might be confusing. Let's set it to NULL to force usage of new table.
print("\nClearing old 'comment' column in verses table...")
cursor.execute("UPDATE verses SET comment = NULL")
conn.commit()

conn.close()

# Recompress
print("Recompressing database...")
with open(db_path, 'rb') as f_in:
    with gzip.open(gz_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(db_path)
print("Done!")

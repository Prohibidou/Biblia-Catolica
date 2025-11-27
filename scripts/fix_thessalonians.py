import sqlite3
import gzip
import shutil
import re
import os

def extract_thessalonians_comments(txt_file):
    """Extract comments for 1 and 2 Thessalonians from source file"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    comments = {}
    
    # Find 1 Thessalonians section
    start_1th = content.find('1 TESALONICENSES')
    end_1th = content.find('2 TESALONICENSES', start_1th)
    
    if start_1th == -1 or end_1th == -1:
        print("Could not find 1 Thessalonians section")
        return comments
    
    # Find 2 Thessalonians section  
    start_2th = end_1th
    # Find next book (1 Timothy)
    end_2th = content.find('1 TIMOTEO', start_2th)
    
    if end_2th == -1:
        end_2th = content.find('TIMOTEO', start_2th)
        if end_2th == -1:
            end_2th = len(content)
    
    sections = [
        ('1TH', content[start_1th:end_1th]),
        ('2TH', content[start_2th:end_2th])
    ]
    
    for book_id, section in sections:
        print(f"\nProcessing {book_id}...")
        
        # Pattern for Thessalonians: "COMENTARIO\n\n\n1 Ts 1,1" or "2 Ts 1,1"
        book_abbrev = '1 Ts' if book_id == '1TH' else '2 Ts'
        
        # Pattern: COMENTARIO followed by reference like "1 Ts 1,1" or "1 Ts 1,1-5"
        pattern = rf'COMENTARIO\s*\n+\s*{re.escape(book_abbrev)}\s+(\d+),(\d+)(?:-(\d+))?\s*\n+(.*?)(?=\n\s*Volver|COMENTARIO|\Z)'
        
        matches = re.finditer(pattern, section, re.DOTALL)
        
        for match in matches:
            chapter = int(match.group(1))
            verse_start = int(match.group(2))
            verse_end = int(match.group(3)) if match.group(3) else verse_start
            comment_text = match.group(4).strip()
            
            # Clean up the comment
            comment_text = re.sub(r'\s+', ' ', comment_text)
            comment_text = comment_text.replace('\n', ' ')
            
            # Store comment for all verses in range
            for verse in range(verse_start, verse_end + 1):
                key = (book_id, chapter, verse)
                if key not in comments:
                    comments[key] = comment_text
                else:
                    # Append if there's already a comment
                    comments[key] += "<br><br>" + comment_text
                    
        print(f"Found {sum(1 for k in comments if k[0] == book_id)} comments for {book_id}")
    
    return comments

def fix_1th_verses_and_add_comments(gz_path, comments):
    """Fix 1 Thessalonians verse numbering and add comments"""
    print(f"\n=== Updating database ===")
    
    # Decompress
    db_path = "scripts/temp_navarra_update.sqlite"
    with gzip.open(gz_path, 'rb') as f_in:
        with open(db_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # First, fix 1 Thessalonians numbering
    # The issue is that verse numbering is off by one
    # Current: 1:2, 2:1, 2:2, 2:3...
    # Should be: 1:1, 1:2, 1:3, 1:4...
    
    print("\nFixing 1 Thessalonians verse numbering...")
    
    # Get all 1TH verses
    cursor.execute("SELECT chapter, verse, text, title FROM verses WHERE book='1TH' ORDER BY chapter, verse")
    verses_1th = cursor.fetchall()
    
    print(f"Found {len(verses_1th)} verses in 1TH")
    print(f"First few: {verses_1th[:5]}")
    
    # It looks like the problem is:
    # - 1:2 should be 1:1
    # - 2:1 should be 1:2
    # - etc.
    
    # Let's check the pattern
    if verses_1th and verses_1th[0][0] == 1 and verses_1th[0][1] == 2:
        print("Confirmed: verses start at 1:2 instead of 1:1")
        
        # Delete all 1TH verses
        cursor.execute("DELETE FROM verses WHERE book='1TH'")
        
        # Re-insert with corrected numbering
        correct_verse = 1
        current_chapter = 1
        
        for ch, v, text, title in verses_1th:
            # If we're still in chapter 1 or 2, renumber
            if ch <= 2:
                if ch == 2:
                    # This is actually still chapter 1
                    new_ch = 1
                    new_v = correct_verse
                else:
                    new_ch = 1
                    new_v = correct_verse
                
                cursor.execute(
                    "INSERT INTO verses (book, chapter, verse, text, title, comment) VALUES (?, ?, ?, ?, ?, ?)",
                    ('1TH', new_ch, new_v, text, title, None)
                )
                correct_verse += 1
            else:
                # For later chapters, adjust chapter number down by 1
                cursor.execute(
                    "INSERT INTO verses (book, chapter, verse, text, title, comment) VALUES (?, ?, ?, ?, ?, ?)",
                    ('1TH', ch - 1, v, text, title, None)
                )
    
    conn.commit()
    
    # Verify the fix
    cursor.execute("SELECT chapter, verse FROM verses WHERE book='1TH' ORDER BY chapter, verse LIMIT 5")
    print(f"After fix, first verses: {cursor.fetchall()}")
    
    # Now update with comments
    print("\nAdding comments...")
    updated = 0
    for (book, chapter, verse), comment in comments.items():
        cursor.execute(
            "UPDATE verses SET comment = ? WHERE book = ? AND chapter = ? AND verse = ?",
            (comment, book, chapter, verse)
        )
        if cursor.rowcount > 0:
            updated += 1
    
    conn.commit()
    
    print(f"Updated {updated} verses with comments")
    
    # Verify
    for book_id in ['1TH', '2TH']:
        cursor.execute("SELECT COUNT(*) FROM verses WHERE book = ? AND comment IS NOT NULL AND comment != ''", (book_id,))
        count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM verses WHERE book = ?", (book_id,))
        total = cursor.fetchone()[0]
        print(f"{book_id}: {count}/{total} verses now have comments")
    
    conn.close()
    
    # Recompress
    print("\nRecompressing database...")
    with open(db_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(db_path)
    print("Done!")

if __name__ == "__main__":
    # Extract comments from source
    comments = extract_thessalonians_comments("scripts/Sagrada_Biblia_Navarra_full.txt")
    
    print(f"\nTotal comments extracted: {len(comments)}")
    
    # Sample some comments
    print("\n=== Sample comments ===")
    for key in list(comments.keys())[:3]:
        book, ch, v = key
        print(f"{book} {ch}:{v} - {comments[key][:100]}...")
    
    # Fix verses and update database
    fix_1th_verses_and_add_comments("public/bibles/navarra.sqlite.gz", comments)

import sqlite3
import gzip
import shutil
import re
import os

def extract_john_letters_comments(txt_file):
    """Extract comments for 1, 2, 3 John from source file"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    comments = {}
    
    # Find the letters of John
    # They appear as: 1 JUAN, 2 JUAN, 3 JUAN
    start_1jn = content.find('CARTA DE SAN JUAN')
    if start_1jn == -1:
        start_1jn = content.find('1 JUAN')
    
    # Find delimiters
    start_2jn = content.find('2 JUAN', start_1jn + 1)
    start_3jn = content.find('3 JUAN', start_2jn + 1)
    end_3jn = content.find('JUDAS', start_3jn)
    
    if end_3jn == -1:
        end_3jn = len(content)
    
    sections = [
        ('1JN', content[start_1jn:start_2jn] if start_2jn != -1 else ''),
        ('2JN', content[start_2jn:start_3jn] if start_2jn != -1 and start_3jn != -1 else ''),
        ('3JN', content[start_3jn:end_3jn] if start_3jn != -1 else '')
    ]
    
    for book_id, section in sections:
        if not section:
            print(f"Warning: Could not find section for {book_id}")
            continue
            
        print(f"\nProcessing {book_id}...")
        
        # Pattern for John letters: "COMENTARIO\n\n\n1 Jn 1,1" or similar
        # Book can be "1 Jn", "2 Jn", "3 Jn"
        if book_id == '1JN':
            book_abbrev = '1 Jn'
        elif book_id == '2JN':
            book_abbrev = '2 Jn'
        else:
            book_abbrev = '3 Jn'
        
        # Pattern: COMENTARIO followed by reference
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
                    comments[key] += "<br><br>" + comment_text
                    
        print(f"Found {sum(1 for k in comments if k[0] == book_id)} comments for {book_id}")
    
    return comments

def fix_john_verses_and_add_comments(gz_path, comments):
    """Fix 1 John verse numbering and add comments for all John letters"""
    print(f"\n=== Updating database ===")
    
    # Decompress
    db_path = "scripts/temp_navarra_update.sqlite"
    with gzip.open(gz_path, 'rb') as f_in:
        with open(db_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fix 1 John numbering (similar to 1 Thessalonians issue)
    print("\nChecking 1 John verse numbering...")
    
    cursor.execute("SELECT chapter, verse, text, title FROM verses WHERE book='1JN' ORDER BY chapter, verse")
    verses_1jn = cursor.fetchall()
    
    print(f"Found {len(verses_1jn)} verses in 1JN")
    if verses_1jn:
        print(f"First verse: {verses_1jn[0]}")
    
    # Check if first verse is numbered incorrectly
    if verses_1jn and verses_1jn[0][0] == 1 and verses_1jn[0][1] == 2:
        print("Confirmed: 1 John starts at 1:2 instead of 1:1")
        
        # Get correct text for 1:1 from source
        correct_1_1_text = "Lo que existía desde el principio, lo que hemos oído, lo que hemos visto con nuestros ojos, lo que contemplamos y palparon nuestras manos acerca de la Palabra de vida"
        
        # Delete all 1JN verses
        cursor.execute("DELETE FROM verses WHERE book='1JN'")
        
        # Re-insert with corrected numbering
        verse_num = 1
        current_chapter = 1
        
        # Insert the missing 1:1 first
        cursor.execute(
            "INSERT INTO verses (book, chapter, verse, text, title, comment) VALUES (?, ?, ?, ?, ?, ?)",
            ('1JN', 1, 1, correct_1_1_text, '', None)
        )
        verse_num = 2
        
        # Now process the rest
        for ch, v, text, title in verses_1jn:
            if ch == 1:
                # Still in chapter 1, continue numbering
                cursor.execute(
                    "INSERT INTO verses (book, chapter, verse, text, title, comment) VALUES (?, ?, ?, ?, ?, ?)",
                    ('1JN', 1, verse_num, text, title, None)
                )
                verse_num += 1
            else:
                # Other chapters, keep as-is
                cursor.execute(
                    "INSERT INTO verses (book, chapter, verse, text, title, comment) VALUES (?, ?, ?, ?, ?, ?)",
                    ('1JN', ch, v, text, title, None)
                )
        
        conn.commit()
        
        # Verify the fix
        cursor.execute("SELECT chapter, verse, text FROM verses WHERE book='1JN' AND chapter=1 ORDER BY verse LIMIT 5")
        print(f"After fix, first verses of 1 John:")
        for r in cursor.fetchall():
            print(f"  {r[0]}:{r[1]} - {r[2][:60]}...")
    
    # Now add comments for all three letters
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
    for book_id in ['1JN', '2JN', '3JN']:
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
    comments = extract_john_letters_comments("scripts/Sagrada_Biblia_Navarra_full.txt")
    
    print(f"\nTotal comments extracted: {len(comments)}")
    
    # Sample some comments
    print("\n=== Sample comments ===")
    for key in list(comments.keys())[:3]:
        book, ch, v = key
        print(f"{book} {ch}:{v} - {comments[key][:100]}...")
    
    # Fix verses and update database
    fix_john_verses_and_add_comments("public/bibles/navarra.sqlite.gz", comments)

import sqlite3
import gzip
import shutil
import re
import os

def extract_corinthians_comments(txt_file):
    """Extract comments for 1 and 2 Corinthians from source file"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    comments = {}
    
    # Find 1 Corinthians section
    start_1co = content.find('1 CORINTIOS')
    end_1co = content.find('2 CORINTIOS', start_1co)
    
    if start_1co == -1 or end_1co == -1:
        print("Could not find 1 Corinthians section")
        return comments
    
    # Find 2 Corinthians section  
    start_2co = end_1co
    end_2co = content.find('GÁLATAS', start_2co)
    
    if end_2co == -1:
        # Try alternative ending markers
        end_2co = content.find('GALATAS', start_2co)
        if end_2co == -1:
            end_2co = len(content)
    
    sections = [
        ('1CO', content[start_1co:end_1co]),
        ('2CO', content[start_2co:end_2co])
    ]
    
    for book_id, section in sections:
        print(f"\nProcessing {book_id}...")
        
        # Find all comment blocks like "COMENTARIO\n1 Co 1,1-9\n\n\nText..."
        # Pattern: COMENTARIO followed by reference, then text until next COMENTARIO or Volver
        pattern = r'COMENTARIO\s*\n\s*\d\s*Co\s*(\d+),(\d+)(?:-(\d+))?\s*\n+(.*?)(?=\n\s*Volver|COMENTARIO|\Z)'
        
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

def update_database(gz_path, comments):
    """Update SQLite database with comments"""
    print(f"\n=== Updating database ===")
    
    # Decompress
    db_path = "scripts/temp_navarra_update.sqlite"
    with gzip.open(gz_path, 'rb') as f_in:
        with open(db_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update each verse with its comment
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
    for book_id in ['1CO', '2CO']:
        cursor.execute("SELECT COUNT(*) FROM verses WHERE book = ? AND comment IS NOT NULL AND comment != ''", (book_id,))
        count = cursor.fetchone()[0]
        print(f"{book_id}: {count} verses now have comments")
    
    conn.close()
    
    # Recompress
    print("Recompressing database...")
    with open(db_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    os.remove(db_path)
    print("Done!")

if __name__ == "__main__":
    # Extract comments from source
    comments = extract_corinthians_comments("scripts/Sagrada_Biblia_Navarra_full.txt")
    
    print(f"\nTotal comments extracted: {len(comments)}")
    
    # Sample some comments
    print("\n=== Sample comments ===")
    for key in list(comments.keys())[:3]:
        book, ch, v = key
        print(f"{book} {ch}:{v} - {comments[key][:100]}...")
    
    # Update database
    update_database("public/bibles/navarra.sqlite.gz", comments)

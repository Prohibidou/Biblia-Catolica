import sqlite3
import gzip
import shutil
import re
import os

def extract_epistles_comments(txt_file):
    """Extract comments for Jude, 1 Peter, 2 Peter, and Philemon from source file"""
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    comments = {}
    
    # Find sections for each book
    # Looking for patterns like "CARTA DE JUDAS", "1 PEDRO", etc.
    
    # Jude
    jud_start = content.find('JUDAS')
    if jud_start == -1:
        jud_start = content.find('CARTA DE JUDAS')
    
    # 1 Peter
    peter1_start = content.find('1 PEDRO')
    if peter1_start == -1:
        peter1_start = content.find('PRIMERA CARTA DE SAN PEDRO')
    
    # 2 Peter
    peter2_start = content.find('2 PEDRO', peter1_start + 1 if peter1_start != -1 else 0)
    if peter2_start == -1:
        peter2_start = content.find('SEGUNDA CARTA DE SAN PEDRO')
    
    # Philemon
    philemon_start = content.find('FILEMÓN')
    if philemon_start == -1:
        philemon_start = content.find('FILEMON')
    if philemon_start == -1:
        philemon_start = content.find('CARTA A FILEMON')
    
    # Define sections with proper boundaries
    sections = []
    
    if jud_start != -1:
        # Jude is usually near the end, before Revelation
        jud_end = content.find('APOCALIPSIS', jud_start)
        if jud_end == -1:
            jud_end = len(content)
        sections.append(('JUD', content[jud_start:jud_end], 'Jds'))
    
    if peter1_start != -1 and peter2_start != -1:
        sections.append(('1PE', content[peter1_start:peter2_start], '1 P'))
    
    if peter2_start != -1:
        # 2 Peter ends where 1 John or next book starts
        peter2_end = content.find('1 JUAN', peter2_start)
        if peter2_end == -1:
            peter2_end = content.find('PRIMERA CARTA', peter2_start + 100)
        if peter2_end == -1:
            peter2_end = len(content)
        sections.append(('2PE', content[peter2_start:peter2_end], '2 P'))
    
    if philemon_start != -1:
        # Philemon is short, ends at Hebrews
        philemon_end = content.find('HEBREOS', philemon_start)
        if philemon_end == -1:
            philemon_end = content.find('CARTA A LOS HEBREOS', philemon_start)
        if philemon_end == -1:
            philemon_end = len(content)
        sections.append(('PHM', content[philemon_start:philemon_end], 'Flm'))
    
    for book_id, section, book_abbrev in sections:
        print(f"\nProcessing {book_id} (abbrev: {book_abbrev})...")
        
        # Pattern: COMENTARIO followed by reference
        pattern = rf'COMENTARIO\s*\n+\s*{re.escape(book_abbrev)}\s+(\d+),(\d+)(?:-(\d+))?\s*\n+(.*?)(?=\n\s*Volver|COMENTARIO|\Z)'
        
        matches = re.finditer(pattern, section, re.DOTALL)
        
        count = 0
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
                    count += 1
                else:
                    comments[key] += "<br><br>" + comment_text
                    
        print(f"Found {count} comments for {book_id}")
    
    return comments

def add_comments_to_database(gz_path, comments):
    """Add comments to the database"""
    print(f"\n=== Updating database ===")
    
    # Decompress
    db_path = "scripts/temp_navarra_update.sqlite"
    with gzip.open(gz_path, 'rb') as f_in:
        with open(db_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add comments
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
    for book_id in ['JUD', '1PE', '2PE', 'PHM']:
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
    comments = extract_epistles_comments("scripts/Sagrada_Biblia_Navarra_full.txt")
    
    print(f"\nTotal comments extracted: {len(comments)}")
    
    # Sample some comments
    print("\n=== Sample comments ===")
    for key in list(comments.keys())[:5]:
        book, ch, v = key
        print(f"{book} {ch}:{v} - {comments[key][:100]}...")
    
    # Update database
    add_comments_to_database("public/bibles/navarra.sqlite.gz", comments)

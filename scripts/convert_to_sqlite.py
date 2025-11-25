import sqlite3
import json
import gzip
import os
import sys

def convert_json_to_sqlite(json_path, output_name):
    """
    Converts a JSON bible file to a compressed SQLite database.
    Expected JSON format:
    [
        {
            "book": "GEN",
            "chapter": 1,
            "verse": 1,
            "text": "In the beginning..."
        },
        ...
    ]
    """
    
    print(f"Processing {json_path}...")
    
    # 1. Create SQLite DB
    db_path = f"{output_name}.sqlite"
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 2. Create Schema
    # We use a simple schema optimized for read speed
    cursor.execute('''
        CREATE TABLE verses (
            book TEXT,
            chapter INTEGER,
            verse INTEGER,
            text TEXT,
            comment TEXT
        )
    ''')
    
    # Index for fast lookups by chapter
    cursor.execute('CREATE INDEX idx_chapter ON verses (book, chapter)')
    # Index for search (optional, increases size but speeds up LIKE queries)
    # cursor.execute('CREATE INDEX idx_text ON verses (text)') 

    # 3. Load JSON and Insert
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Inserting {len(data)} verses...")
    
    # Prepare bulk insert
    verses_to_insert = []
    for item in data:
        verses_to_insert.append((
            item['book'],
            item['chapter'],
            item['verse'],
            item['text'],
            item.get('comment', None)
        ))
        
    cursor.executemany('INSERT INTO verses VALUES (?,?,?,?,?)', verses_to_insert)
    
    conn.commit()
    conn.close()
    
    print(f"Database created at {db_path}")
    
    # 4. Compress to GZIP
    gz_path = f"{output_name}.sqlite.gz"
    print(f"Compressing to {gz_path}...")
    
    with open(db_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            f_out.writelines(f_in)
            
    # Cleanup raw sqlite file
    import time
    time.sleep(0.5) # Wait for file handle release on Windows
    try:
        os.remove(db_path)
    except PermissionError:
        print(f"Warning: Could not remove temporary file {db_path}. You may delete it manually.")
    
    print("Done! File ready for deployment.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_to_sqlite.py <input_json_file> [output_name]")
        print("Example: python convert_to_sqlite.py bible_data.json rvr1960")
    else:
        input_file = sys.argv[1]
        output_name = sys.argv[2] if len(sys.argv) > 2 else "bible"
        convert_json_to_sqlite(input_file, output_name)

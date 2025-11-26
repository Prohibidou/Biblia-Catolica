#!/usr/bin/env python3
"""
Convert Navarra JSON to SQLite
"""
import json
import sqlite3
import os

JSON_FILE = "scripts/navarra_final_merged.json"
DB_FILE = "navarra_complete.sqlite"

def convert():
    print(f"Loading {JSON_FILE}...")
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        verses = data['data']
        
    print(f"Creating {DB_FILE}...")
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Create table
    c.execute('''
        CREATE TABLE verses (
            book TEXT,
            chapter INTEGER,
            verse INTEGER,
            text TEXT,
            title TEXT,
            comment TEXT,
            PRIMARY KEY (book, chapter, verse)
        )
    ''')
    
    print("Inserting verses...")
    count = 0
    for v in verses:
        c.execute('INSERT OR REPLACE INTO verses VALUES (?, ?, ?, ?, ?, ?)', (
            v['book'],
            v['chapter'],
            v['verse'],
            v['text'],
            v.get('title', ''),
            v.get('comment', '')
        ))
        count += 1
        
    conn.commit()
    conn.close()
    print(f"✅ Created database with {count} verses.")

if __name__ == "__main__":
    convert()

import sqlite3

def clean_rev():
    conn = sqlite3.connect('navarra_complete.sqlite')
    c = conn.cursor()
    
    print("Cleaning Revelation...")
    
    # Check max chapter
    c.execute("SELECT max(chapter) FROM verses WHERE book='REV'")
    max_chap = c.fetchone()[0]
    print(f"Max Chapter in REV: {max_chap}")
    
    # Delete chapters > 22
    c.execute("DELETE FROM verses WHERE book='REV' AND chapter > 22")
    print(f"Deleted extra chapters. Rows affected: {c.rowcount}")
    
    # Check max verse in chapter 22
    c.execute("SELECT max(verse) FROM verses WHERE book='REV' AND chapter=22")
    max_verse = c.fetchone()[0]
    print(f"Max Verse in REV 22: {max_verse}")
    
    # Delete verses > 21 in chapter 22
    c.execute("DELETE FROM verses WHERE book='REV' AND chapter=22 AND verse > 21")
    print(f"Deleted extra verses in REV 22. Rows affected: {c.rowcount}")
    
    conn.commit()
    
    # New total
    c.execute("SELECT count(*) FROM verses")
    print(f"New Total Verses: {c.fetchone()[0]}")
    
    conn.close()

clean_rev()

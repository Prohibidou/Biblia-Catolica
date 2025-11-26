import sqlite3

DB_FILE = "navarra_complete.sqlite"

def verify():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Total
    c.execute("SELECT count(*) FROM verses")
    total = c.fetchone()[0]
    print(f"Total verses: {total}")
    
    # Genesis with comment
    print("\n--- Genesis Example ---")
    c.execute("SELECT book, chapter, verse, text, comment FROM verses WHERE book='GEN' AND comment != '' LIMIT 1")
    row = c.fetchone()
    if row:
        print(f"{row[0]} {row[1]}:{row[2]}")
        print(f"Text: {row[3][:50]}...")
        print(f"Comment: {row[4][:100]}...")
    else:
        print("No Genesis comments found!")

    # Romans
    print("\n--- Romans Example ---")
    c.execute("SELECT book, chapter, verse, text, comment FROM verses WHERE book='ROM' LIMIT 1")
    row = c.fetchone()
    if row:
        print(f"{row[0]} {row[1]}:{row[2]}")
        print(f"Text: {row[3][:50]}...")
        if row[4]:
            print(f"Comment: {row[4][:100]}...")
    else:
        print("No Romans verses found!")

    conn.close()

verify()

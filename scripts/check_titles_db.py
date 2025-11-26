import sqlite3

def check_titles():
    conn = sqlite3.connect('navarra_complete.sqlite')
    c = conn.cursor()
    c.execute("SELECT count(*) FROM verses WHERE title != ''")
    count = c.fetchone()[0]
    print(f"Verses with titles: {count}")
    
    if count > 0:
        c.execute("SELECT book, chapter, verse, title FROM verses WHERE title != '' LIMIT 5")
        for row in c.fetchall():
            print(row)
    conn.close()

check_titles()

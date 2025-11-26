import sqlite3

def check_rev():
    conn = sqlite3.connect('navarra_complete.sqlite')
    c = conn.cursor()
    c.execute("SELECT chapter, verse, text FROM verses WHERE book='REV' ORDER BY chapter DESC, verse DESC LIMIT 10")
    for row in c.fetchall():
        print(row)
    conn.close()

check_rev()

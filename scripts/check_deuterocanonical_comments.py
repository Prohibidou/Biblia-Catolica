import sqlite3

conn = sqlite3.connect('navarra_complete.sqlite')
c = conn.cursor()

deuterocanonical = ['TOB', 'JDT', '1MA', '2MA', 'WIS', 'SIR', 'BAR']

print("DEUTEROCANONICAL BOOKS - Comments Status:\n")
for book in deuterocanonical:
    # Total verses
    c.execute('SELECT count(*) FROM verses WHERE book = ?', (book,))
    total = c.fetchone()[0]
    
    # Verses with comments
    c.execute('SELECT count(*) FROM verses WHERE book = ? AND comment != ""', (book,))
    with_comments = c.fetchone()[0]
    
    # Get first verse with comment as example
    c.execute('SELECT chapter, verse, comment FROM verses WHERE book = ? AND comment != "" LIMIT 1', (book,))
    example = c.fetchone()
    
    print(f"{book:4} - Total: {total:4} verses | Comments: {with_comments:3} | {'✅' if with_comments > 0 else '❌'}")
    if example:
        print(f"      Example: {book} {example[0]}:{example[1]} - {example[2][:60]}...")
    print()

# Check Daniel chapter 13-14 (additions)
print("\nDANIEL CHAPTERS 13-14 (Additions):")
c.execute('SELECT chapter, count(*) FROM verses WHERE book="DAN" AND chapter > 12 GROUP BY chapter')
for row in c.fetchall():
    print(f"  Chapter {row[0]}: {row[1]} verses")

# Check Joel chapter 4
print("\nJOEL CHAPTER 4:")
c.execute('SELECT count(*) FROM verses WHERE book="JOL" AND chapter=4')
count = c.fetchone()[0]
print(f"  Chapter 4: {count} verses")

conn.close()

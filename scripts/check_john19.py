import sqlite3

conn = sqlite3.connect('navarra_complete.sqlite')
c = conn.cursor()

# Check John 19
c.execute('SELECT count(*), min(verse), max(verse) FROM verses WHERE book="JHN" AND chapter=19')
result = c.fetchone()
print(f'Juan 19: {result[0]} verses (from {result[1]} to {result[2]})')

# Show first 5 verses
print('\nFirst 5 verses:')
c.execute('SELECT verse, text FROM verses WHERE book="JHN" AND chapter=19 ORDER BY verse LIMIT 5')
for row in c.fetchall():
    text = row[1][:100] + '...' if len(row[1]) > 100 else row[1]
    print(f'  {row[0]}: {text}')

# Check if there are any comments
c.execute('SELECT count(*) FROM verses WHERE book="JHN" AND chapter=19 AND comment != ""')
comments_count = c.fetchone()[0]
print(f'\nComments: {comments_count}')

conn.close()

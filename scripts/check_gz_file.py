import gzip
import sqlite3
import os

# Check the compressed file
print("Checking navarra.sqlite.gz...")
with gzip.open('public/bibles/navarra.sqlite.gz', 'rb') as f:
    data = f.read()
    
with open('temp_check.sqlite', 'wb') as f:
    f.write(data)

# Query it
conn = sqlite3.connect('temp_check.sqlite')
c = conn.cursor()

c.execute('SELECT count(*) FROM verses WHERE book="JHN" AND chapter=19')
count = c.fetchone()[0]
print(f'Juan 19 in .gz file: {count} verses')

if count == 0:
    print("ERROR: The .gz file doesn't have Juan 19!")
    print("Need to regenerate the .gz file from navarra_complete.sqlite")

conn.close()
os.remove('temp_check.sqlite')

import sqlite3
import json
import os
import gzip

json_file = 'scripts/full_bible_final.json'
db_file = 'public/bibles/navarra.sqlite'

if os.path.exists(db_file):
    os.remove(db_file)

print(f"Creando base de datos en {db_file}...")
conn = sqlite3.connect(db_file)
c = conn.cursor()

c.execute('''
    CREATE TABLE verses (
        book TEXT,
        chapter INTEGER,
        verse INTEGER,
        text TEXT,
        comment TEXT,
        PRIMARY KEY (book, chapter, verse)
    )
''')

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Insertando {len(data)} versículos...")

count = 0
for v in data:
    try:
        c.execute('INSERT INTO verses VALUES (?, ?, ?, ?, ?)', 
                 (v['book'], v['chapter'], v['verse'], v['text'], v.get('comment', '')))
        count += 1
    except sqlite3.IntegrityError:
        pass

conn.commit()
conn.close()

print(f"Base de datos creada con {count} versículos.")

print("Comprimiendo...")
with open(db_file, 'rb') as f_in:
    with gzip.open(db_file + '.gz', 'wb') as f_out:
        f_out.writelines(f_in)

print(f"Creado {db_file}.gz")

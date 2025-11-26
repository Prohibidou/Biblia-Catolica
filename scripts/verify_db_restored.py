import sqlite3
import gzip

with gzip.open('public/bibles/navarra.sqlite.gz', 'rb') as f:
    db_bytes = f.read()

conn = sqlite3.connect(':memory:')
conn.deserialize(db_bytes)
c = conn.cursor()

c.execute('SELECT COUNT(*) FROM verses')
total = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM verses WHERE comment != ''")
with_comments = c.fetchone()[0]

c.execute('SELECT DISTINCT book FROM verses ORDER BY book')
books = [row[0] for row in c.fetchall()]

print(f"✅ BASE DE DATOS RESTAURADA:")
print(f"   Total versículos: {total:,}")
print(f"   Con comentarios: {with_comments:,}")
print(f"   Libros ({len(books)}): {', '.join(books)}")

conn.close()

import sqlite3

conn = sqlite3.connect('navarra_complete.sqlite')
c = conn.cursor()

# Verificar 3 Juan
c.execute('SELECT count(*) FROM verses WHERE book="3JN"')
count = c.fetchone()[0]
print(f'3 Juan total versículos: {count}')

if count > 0:
    c.execute('SELECT chapter, verse, text FROM verses WHERE book="3JN" ORDER BY chapter, verse')
    print('\nTodos los versículos de 3 Juan:')
    for row in c.fetchall():
        print(f'  {row[0]}:{row[1]} - {row[2][:60]}...')
else:
    print('❌ 3 JUAN ESTÁ VACÍO')

# Verificar otros libros pequeños del NT
print('\n\nEstado de cartas cortas:')
for book_code, book_name in [('2JN', '2 Juan'), ('3JN', '3 Juan'), ('JUD', 'Judas'), ('PHM', 'Filemón')]:
    c.execute(f'SELECT count(*) FROM verses WHERE book="{book_code}"')
    count = c.fetchone()[0]
    print(f'  {book_name}: {count} versículos')

# Verificar títulos de sección
print('\n\nEjemplo de títulos de sección (comentarios):')
c.execute('SELECT book, chapter, verse, comment FROM verses WHERE comment IS NOT NULL AND comment != "" LIMIT 10')
for row in c.fetchall():
    print(f'  {row[0]} {row[1]}:{row[2]} - {row[3][:60]}...')

conn.close()

import json

data = json.load(open('scripts/navarra_at_fixed.json', 'r', encoding='utf-8'))

# Contar versículos de 1 Reyes
reyes1 = [v for v in data if v['book'] == '1KI']
print(f'1 Reyes tiene {len(reyes1)} versículos')
print(f'\nPrimeros 5 versículos:')
for v in reyes1[:5]:
    print(f"  {v['chapter']}:{v['verse']} - {v['text'][:70]}...")

# Mostrar todos los libros encontrados
books = {}
for v in data:
    if v['book'] not in books:
        books[v['book']] = 0
    books[v['book']] += 1

print(f'\n\nTodos los libros ({len(books)}) y sus versículos:')
for book in sorted(books.keys()):
    print(f'  {book}: {books[book]} versículos')

print(f'\n\nTotal de versículos: {len(data)}')

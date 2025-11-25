import json

data = json.load(open('scripts/navarra_nt.json', encoding='utf-8'))

books = {}
for v in data:
    book = v['book']
    if book not in books:
        books[book] = 0
    books[book] += 1

print('Versículos extraídos por libro:')
print('='*50)
for book, count in sorted(books.items()):
    print(f'  {book}: {count} versículos')

print(f'\nTotal: {len(data)} versículos')

# Ver ejemplos de cada libro
print('\n\nPrimeros versículos de cada libro:')
print('='*50)
for book in sorted(set(v['book'] for v in data)):
    verses = [v for v in data if v['book'] == book][:3]
    print(f'\n{book}:')
    for v in verses:
        title = f" [{v.get('section_title', 'Sin título')}]" if v.get('section_title') else ""
        print(f"  {v['chapter']}:{v['verse']}{title}")
        print(f"    {v['text'][:80]}...")

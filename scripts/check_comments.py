import json

with open('scripts/gospels_extracted.json', encoding='utf-8') as f:
    data = json.load(f)

comments = [v for v in data if 'comment' in v]
print(f'Versículos con comentarios: {len(comments)} de {len(data)}')

if comments:
    print('\nEjemplos de comentarios:')
    for v in comments[:10]:
        print(f"\n{v['book']} {v['chapter']}:{v['verse']}")
        print(f"  Comentario: {v['comment'][:150]}...")
        print(f"  Texto: {v['text'][:80]}...")
else:
    print("\n❌ No se encontraron comentarios. El parser necesita ajustes.")

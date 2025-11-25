import requests
import json
import time

print("Descargando Biblia RV1960 completa desde API...")

# La API devuelve todos los libros
all_verses = []

# Lista de códigos de libros en orden
book_codes = [
    'gen', 'exo', 'lev', 'num', 'deu', 'jos', 'jdg', 'rut', '1sa', '2sa', '1ki', '2ki', '1ch', '2ch', 
    'ezr', 'neh', 'est', 'job', 'psa', 'pro', 'ecc', 'sng', 'isa', 'jer', 'lam', 'ezk', 'dan',
    'hos', 'jol', 'amo', 'oba', 'jon', 'mic', 'nah', 'hab', 'zep', 'hag', 'zec', 'mal',
    'mat', 'mrk', 'luk', 'jhn', 'act', 'rom', '1co', '2co', 'gal', 'eph', 'php', 'col',
    '1th', '2th', '1ti', '2ti', 'tit', 'phm', 'heb', 'jas', '1pe', '2pe', '1jn', '2jn', '3jn', 'jud', 'rev'
]

for book_code in book_codes:
    url = f"https://biblia-api.vercel.app/api/books/{book_code}"
    print(f"Descargando {book_code.upper()}...")
    
    try:
        response = requests.get(url, timeout=20)
        
        if response.status_code == 200:
            book_data = response.json()
            
            # Extraer versículos
            for chapter in book_data.get('chapters', []):
                chapter_num = chapter['chapter']
                for verse in chapter.get('verses', []):
                    all_verses.append({
                        'book': book_code.upper(),
                        'chapter': chapter_num,
                        'verse': verse['verse'],
                        'text': verse['text'],
                        'comment': ''
                    })
            
            print(f"  ✓ {len([c for c in book_data.get('chapters', [])])} capítulos")
        else:
            print(f"  ❌ Error {response.status_code}")
        
        time.sleep(0.1)  # Evitar rate limiting
        
    except Exception as e:
        print(f"  ❌ Error: {e}")

# Guardar
output_file = "scripts/bible_rv1960_full.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\n✓ Descarga completada!")
print(f"  Total versículos: {len(all_verses)}")
print(f"  Guardado en: {output_file}")

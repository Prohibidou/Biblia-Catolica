import re
import json

SOURCE_FILE = "scripts/Sagrada_Biblia_Navarra_full.txt"
OUTPUT_FILE = "scripts/biblia_completa_correcta.json"

print("="*70)
print("PARSER CORRECTO - Usando lógica simple de números")
print("="*70)

# Leer archivo
print(f"\nLeyendo: {SOURCE_FILE}")
with open(SOURCE_FILE, 'r', encoding='utf-8', errors='ignore') as f:
    all_lines = f.readlines()

print(f"Total líneas: {len(all_lines):,}")

# Variables
current_book = None
current_chapter = 0
current_verse = 0
verse_buffer = ""
pending_titles = []
all_verses = []

# Mapa simple de detección de libros (buscaremos los títulos exactos)
BOOK_MAP = {
    'GÉNESIS': 'GEN', 'ÉXODO': 'EXO', 'LEVÍTICO': 'LEV', 'NÚMEROS': 'NUM', 'DEUTERONOMIO': 'DEU',
    'JOSUÉ': 'JOS', 'JUECES': 'JDG', 'RUT': 'RUT', '1 SAMUEL': '1SA', '2 SAMUEL': '2SA',
    '1 REYES': '1KI', '2 REYES': '2KI', '1 CRÓNICAS': '1CH', '2 CRÓNICAS': '2CH',
    'ESDRAS': 'EZR', 'NEHEMÍAS': 'NEH', 'TOBÍAS': 'TOB', 'JUDIT': 'JDT', 'ESTER': 'EST',
    '1 MACABEOS': '1MA', '2 MACABEOS': '2MA', 'JOB': 'JOB', 'SALMOS': 'PSA',
    'PROVERBIOS': 'PRO', 'ECLESIASTÉS': 'ECC', 'CANTAR': 'SNG', 'SABIDURÍA': 'WIS',
    'ECLESIÁSTICO': 'SIR', 'ISAÍAS': 'ISA', 'JEREMÍAS': 'JER', 'LAMENTACIONES': 'LAM',
    'BARUC': 'BAR', 'EZEQUIEL': 'EZK', 'DANIEL': 'DAN', 'OSEAS': 'HOS', 'JOEL': 'JOL',
    'AMÓS': 'AMO', 'ABDÍAS': 'OBA', 'JONÁS': 'JON', 'MIQUEAS': 'MIC', 'NAHÚM': 'NAH',
    'HABACUC': 'HAB', 'SOFONÍAS': 'ZEP', 'AGEO': 'HAG', 'ZACARÍAS': 'ZEC', 'MALAQUÍAS': 'MAL',
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN', 'HECHOS': 'ACT',
    'ROMANOS': 'ROM', '1 CORINTIOS': '1CO', '2 CORINTIOS': '2CO', 'GÁLATAS': 'GAL',
    'EFESIOS': 'EPH', 'FILIPENSES': 'PHP', 'COLOSENSES': 'COL', '1 TESALONICENSES': '1TH',
    '2 TESALONICENSES': '2TH', '1 TIMOTEO': '1TI', '2 TIMOTEO': '2TI', 'TITO': 'TIT',
    'FILEMÓN': 'PHM', 'HEBREOS': 'HEB', 'SANTIAGO': 'JAS', '1 PEDRO': '1PE', '2 PEDRO': '2PE',
    '1 JUAN': '1JN', '2 JUAN': '2JN', '3 JUAN': '3JN', 'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

verse_count = 0
title_count = 0
processing = False

print("\nProcesando líneas...")

for i, line in enumerate(all_lines):
    line = line.strip()
    
    if not line:
        continue
    
    # Progreso cada 50k líneas
    if i % 50000 == 0 and i > 0:
        print(f"  Línea {i:,}... ({verse_count} versículos, {title_count} títulos)")
    
    # Detectar inicio de contenido REAL (Génesis 1:1)
    if not processing:
        # Buscar "1 En el principio creó" o "1 "En el principio creó"
        if re.match(r'^1\s+"?En el principio cre', line):
            processing = True
            current_book = 'GEN'
            current_chapter = 1
            current_verse = 1
            verse_buffer = line
            print(f"\n✓ Inicio encontrado en línea {i}: {line[:60]}")
            continue
        else:
            continue
    
    # Detectar cambio de libro (líneas con solo el nombre del libro en mayúsculas)
    line_upper = line.upper()
    if line_upper in BOOK_MAP and len(line.split()) <= 3:
        # Guardar versículo anterior antes de cambiar de libro
        if verse_buffer and current_verse > 0:
            text_clean = re.sub(r'^\d+\s*["""]?\s*', '', verse_buffer)
            text_clean = re.sub(r'\s+', ' ', text_clean).strip()
            
            v = {
                'book': current_book,
                'chapter': current_chapter,
                'verse': current_verse,
                'text': text_clean
            }
            if pending_titles:
                v['comment'] = '<br>'.join(pending_titles)
                pending_titles = []
            
            all_verses.append(v)
            verse_count += 1
        
        # Cambiar de libro
        current_book = BOOK_MAP[line_upper]
        current_chapter = 0  # Se incrementará cuando vea el primer "1"
        current_verse = 0
        verse_buffer = ""
        print(f"  📖 {line} ({current_book})")
        continue
    
    # Detectar versículo (línea que empieza con número)
    verse_match = re.match(r'^(\d+)\s+(.+)', line)
    
    if verse_match:
        new_verse_num = int(verse_match.group(1))
        verse_text = verse_match.group(2)
        
        # ¿Es versículo 1? → Nuevo capítulo
        if new_verse_num == 1:
            # Guardar versículo anterior
            if verse_buffer and current_verse > 0:
                text_clean = re.sub(r'^\d+\s*["""]?\s*', '', verse_buffer)
                text_clean = re.sub(r'\s+', ' ', text_clean).strip()
                
                v = {
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': current_verse,
                    'text': text_clean
                }
                if pending_titles:
                    v['comment'] = '<br>'.join(pending_titles)
                    pending_titles = []
                
                all_verses.append(v)
                verse_count += 1
            
            # Nuevo capítulo
            current_chapter += 1
            current_verse = 1
            verse_buffer = verse_text
        
        # ¿Es el siguiente versículo esperado?
        elif new_verse_num == current_verse + 1:
            # Guardar versículo anterior
            if verse_buffer:
                text_clean = re.sub(r'^\d+\s*["""]?\s*', '', verse_buffer)
                text_clean = re.sub(r'\s+', ' ', text_clean).strip()
                
                v = {
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': current_verse,
                    'text': text_clean
                }
                if pending_titles:
                    v['comment'] = '<br>'.join(pending_titles)
                    pending_titles = []
                
                all_verses.append(v)
                verse_count += 1
            
            # Nuevo versículo
            current_verse = new_verse_num
            verse_buffer = verse_text
        else:
            # Número fuera de secuencia → añadir al buffer
            verse_buffer += " " + line
    
    # Sin número al inicio → es título o continuación
    else:
        # ¿Es título? (mayúsculas, largo > 10)
        if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.:,;-]+$', line) and len(line) > 10:
            formatted_title = f"<strong>{line}</strong>"
            pending_titles.append(formatted_title)
            title_count += 1
        # ¿Es referencia? (Gn 1,1 etc)
        elif re.match(r'^(Gn|Ex|Lv|Nm|Dt|Mt|Mc|Lc|Jn|Hch)', line):
            formatted_ref = f"<em>{line}</em>"
            pending_titles.append(formatted_ref)
        # Texto normal → añadir al buffer del versículo
        elif verse_buffer:
            verse_buffer += " " + line

# Guardar último versículo
if verse_buffer and current_verse > 0:
    text_clean = re.sub(r'^\d+\s*["""]?\s*', '', verse_buffer)
    text_clean = re.sub(r'\s+', ' ', text_clean).strip()
    
    v = {
        'book': current_book,
        'chapter': current_chapter,
        'verse': current_verse,
        'text': text_clean
    }
    if pending_titles:
        v['comment'] = '<br>'.join(pending_titles)
    
    all_verses.append(v)
    verse_count += 1

print(f"\n✓ Procesamiento completado")
print(f"  Total versículos: {verse_count:,}")
print(f"  Total títulos: {title_count:,}")

# Estadísticas por libro
books_stats = {}
for v in all_verses:
    book = v['book']
    if book not in books_stats:
        books_stats[book] = {'verses': 0, 'with_comment': 0}
    books_stats[book]['verses'] += 1
    if v.get('comment'):
        books_stats[book]['with_comment'] += 1

print(f"\nLibros encontrados: {len(books_stats)}")
for book, stats in sorted(books_stats.items()):
    print(f"  {book}: {stats['verses']:,} vs ({stats['with_comment']} con coment.)")

# Guardar
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\n✅ Guardado en: {OUTPUT_FILE}")

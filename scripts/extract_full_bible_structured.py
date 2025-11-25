import re
import json
import os

SOURCE_FILE = "scripts/Sagrada_Biblia_Navarra_full.txt"

# Definición de zonas de búsqueda para evitar falsos positivos en índices
ZONES = {
    'AT': (56000, 135000),
    'NT': (135000, 170000)
}

# Libros por zona (orden canónico aproximado para búsqueda secuencial)
BOOKS_AT = [
    ('GEN', ['GÉNESIS', 'GENESIS']), ('EXO', ['ÉXODO', 'EXODO']), ('LEV', ['LEVÍTICO']), ('NUM', ['NÚMEROS']), ('DEU', ['DEUTERONOMIO']),
    ('JOS', ['JOSUÉ']), ('JDG', ['JUECES']), ('RUT', ['RUT']), ('1SA', ['I SAMUEL', '1 SAMUEL']), ('2SA', ['II SAMUEL']),
    ('1KI', ['I REYES', '1 REYES']), ('2KI', ['II REYES']), ('1CH', ['I CRÓNICAS']), ('2CH', ['II CRÓNICAS']),
    ('EZR', ['ESDRAS']), ('NEH', ['NEHEMÍAS']), ('TOB', ['TOBÍAS']), ('JDT', ['JUDIT']), ('EST', ['ESTER']),
    ('1MA', ['I MACABEOS']), ('2MA', ['II MACABEOS']), ('JOB', ['JOB']), ('PSA', ['SALMOS']), ('PRO', ['PROVERBIOS']),
    ('ECC', ['ECLESIASTÉS']), ('SNG', ['CANTAR']), ('WIS', ['SABIDURÍA']), ('SIR', ['ECLESIÁSTICO']),
    ('ISA', ['ISAÍAS']), ('JER', ['JEREMÍAS']), ('LAM', ['LAMENTACIONES']), ('BAR', ['BARUC']), ('EZK', ['EZEQUIEL']),
    ('DAN', ['DANIEL']), ('HOS', ['OSEAS']), ('JOL', ['JOEL']), ('AMO', ['AMÓS']), ('OBA', ['ABDÍAS']),
    ('JON', ['JONÁS']), ('MIC', ['MIQUEAS']), ('NAH', ['NAHÚM']), ('HAB', ['HABACUC']), ('ZEP', ['SOFONÍAS']),
    ('HAG', ['AGEO']), ('ZEC', ['ZACARÍAS']), ('MAL', ['MALAQUÍAS'])
]

BOOKS_NT = [
    ('MAT', ['MATEO']), ('MRK', ['MARCOS']), ('LUK', ['LUCAS']), ('JHN', ['JUAN']), ('ACT', ['HECHOS']),
    ('ROM', ['ROMANOS']), ('1CO', ['I CORINTIOS', '1 CORINTIOS']), ('2CO', ['II CORINTIOS']),
    ('GAL', ['GÁLATAS']), ('EPH', ['EFESIOS']), ('PHP', ['FILIPENSES']), ('COL', ['COLOSENSES']),
    ('1TH', ['I TESALONICENSES']), ('2TH', ['II TESALONICENSES']), ('1TI', ['I TIMOTEO']), ('2TI', ['II TIMOTEO']),
    ('TIT', ['TITO']), ('PHM', ['FILEMÓN']), ('HEB', ['HEBREOS']), ('JAS', ['SANTIAGO']),
    ('1PE', ['I PEDRO']), ('2PE', ['II PEDRO']), ('1JN', ['I JUAN']), ('2JN', ['II JUAN']), ('3JN', ['III JUAN']),
    ('JUD', ['JUDAS']), ('REV', ['APOCALIPSIS'])
]

def clean_text(text):
    text = re.sub(r'^[\d\*\?m]+\s*', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    text = re.sub(r'(\d+)([A-ZÁÉÍÓÚÑ])', r'\1 \2', text)
    text = text.replace('*', '\n* ')
    text = text.replace('?', '\n? ')
    text = re.sub(r'\s(m\s+[A-ZÁÉÍÓÚÑ])', r'\n\1', text)
    return text

def extract_verses(book_code, lines):
    verses = []
    current_chapter = 1
    current_verse = 0 
    buffer = ""
    pending_comment = [] 
    current_comment = None
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detectar inicio de versículo
        new_verse_num = None
        match_num = re.match(r'^(\d+)', line)
        if match_num:
            new_verse_num = int(match_num.group(1))
        elif re.match(r'^[\*\?m]\s+', line) or line.startswith('*') or line.startswith('?'):
            new_verse_num = current_verse + 1
        
        is_new_verse = False
        if new_verse_num is not None:
            if new_verse_num == 1:
                if current_verse > 0 or (current_chapter == 1 and current_verse == 0):
                     is_new_verse = True
                     if current_verse > 0: current_chapter += 1
            elif new_verse_num > current_verse and new_verse_num <= current_verse + 10:
                is_new_verse = True
            elif re.match(r'^[\*\?m]', line):
                is_new_verse = True
        
        if is_new_verse:
            if buffer and current_verse > 0:
                v_obj = {
                    'book': book_code,
                    'chapter': current_chapter if new_verse_num != 1 else current_chapter - 1,
                    'verse': current_verse,
                    'text': clean_text(buffer)
                }
                if current_comment: v_obj['comment'] = current_comment
                verses.append(v_obj)
            
            current_verse = new_verse_num if new_verse_num else current_verse + 1
            buffer = line
            
            if pending_comment:
                current_comment = "<br>".join(pending_comment)
                pending_comment = []
            else:
                current_comment = None
            
        else:
            # Títulos y Referencias
            is_title = False
            if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,:;-]+$', line) and len(line) > 3: is_title = True
            elif re.match(r'^(Mt|Mc|Lc|Jn|Hch|Rm|Gén|Ex|Sal|Is)\s+\d+', line): is_title = True
            elif re.match(r'^[IVX]+\.\s', line): is_title = True
            
            if is_title:
                fmt = f"<em>{line}</em>" if re.match(r'^(Mt|Mc|Lc)', line) else f"<strong>{line}</strong>"
                pending_comment.append(fmt)
            else:
                if len(line) > 2: buffer += " " + line

    if buffer and current_verse > 0:
        v_obj = {
            'book': book_code,
            'chapter': current_chapter,
            'verse': current_verse,
            'text': clean_text(buffer)
        }
        if current_comment: v_obj['comment'] = current_comment
        verses.append(v_obj)
        
    return verses

print("Leyendo archivo fuente...")
with open(SOURCE_FILE, encoding='utf-8', errors='ignore') as f:
    full_text = f.readlines()

all_verses = []

# Procesar Zonas
for zone_name, (start_z, end_z) in ZONES.items():
    print(f"\n--- Procesando Zona {zone_name} ({start_z}-{end_z}) ---")
    books_list = BOOKS_AT if zone_name == 'AT' else BOOKS_NT
    
    # Buscar libros en esta zona
    found_books = []
    
    # Estrategia: Buscar secuencialmente. 
    # Si encontramos un libro, restringimos la búsqueda del siguiente a DESPUÉS de este.
    current_search_start = start_z
    
    for code, titles in books_list:
        found_pos = -1
        
        # Buscar título + versículo 1
        for i in range(current_search_start, end_z):
            line = full_text[i].strip()
            if not line: continue
            
            # Coincidencia de título
            line_upper = line.upper()
            is_title_match = False
            for t in titles:
                if t in line_upper and len(line_upper) < len(t) + 15:
                    is_title_match = True
                    break
            
            if is_title_match:
                # Verificar versículo 1 cerca
                for j in range(1, 400): # Rango amplio
                    if i+j >= len(full_text): break
                    if re.match(r'^1[\s\.]+[A-ZÁÉÍÓÚÑ"“]', full_text[i+j].strip()):
                        found_pos = i+j # Usar línea del verso 1 como inicio
                        break
                if found_pos != -1: break
        
        if found_pos != -1:
            print(f"  Encontrado {code} en línea {found_pos}")
            found_books.append((code, found_pos))
            current_search_start = found_pos # El siguiente libro debe estar después
        else:
            print(f"  ⚠️ No encontrado: {code}")

    # Extraer contenido
    for i, (code, start_line) in enumerate(found_books):
        if i < len(found_books) - 1:
            end_line = found_books[i+1][1]
        else:
            end_line = end_z # Hasta el final de la zona
        
        print(f"  Extrayendo {code} ({start_line}-{end_line})...")
        raw_lines = full_text[start_line:end_line]
        processed = preprocess_text("".join(raw_lines))
        v_list = extract_verses(code, processed.split('\n'))
        print(f"    ✓ {len(v_list)} versículos.")
        all_verses.extend(v_list)

# Guardar JSON final
with open('scripts/full_bible_final.json', 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\nTotal Global: {len(all_verses)} versículos.")

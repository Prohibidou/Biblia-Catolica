import re
import json

SOURCE_FILE = "scripts/Sagrada_Biblia_Navarra_full.txt"

# Lista ordenada de libros del NT para buscar sus inicios
NT_BOOKS = [
    ('MAT', ['EVANGELIO SEGÚN SAN MATEO', 'MATEO'], '1 Genealogía de Jesucristo'),
    ('MRK', ['EVANGELIO SEGÚN SAN MARCOS', 'MARCOS'], '1 Comienzo del Evangelio'),
    ('LUK', ['EVANGELIO SEGÚN SAN LUCAS', 'LUCAS'], '1 Puesto que muchos han intentado'),
    ('JHN', ['EVANGELIO SEGÚN SAN JUAN', 'JUAN'], '1 En el principio existía el Verbo'),
    ('ACT', ['HECHOS DE LOS APÓSTOLES', 'HECHOS'], '1 Escribí el primer libro'), # Ajustado
    ('ROM', ['CARTA A LOS ROMANOS', 'ROMANOS'], '1 Pablo, siervo de Jesucristo, apóstol por vocación'), # Más largo
    ('1CO', ['I CORINTIOS', '1 CORINTIOS'], '1 Pablo, llamado a ser apóstol de Cristo Jesús por voluntad de Dios'),
    ('2CO', ['II CORINTIOS', '2 CORINTIOS'], '1 Pablo, apóstol de Cristo Jesús por voluntad de Dios, y el hermano Timoteo'),
    ('GAL', ['CARTA A LOS GÁLATAS', 'GÁLATAS'], '1 Pablo, apóstol —no de parte de hombres'),
    ('EPH', ['CARTA A LOS EFESIOS', 'EFESIOS'], '1 Pablo, apóstol de Cristo Jesús por voluntad de Dios, a los santos'),
    ('PHP', ['CARTA A LOS FILIPENSES', 'FILIPENSES'], '1 Pablo y Timoteo, siervos de Cristo Jesús'),
    ('COL', ['CARTA A LOS COLOSENSES', 'COLOSENSES'], '1 Pablo, apóstol de Cristo Jesús por voluntad de Dios, y el hermano Timoteo, a los santos'),
    ('1TH', ['I TESALONICENSES', '1 TESALONICENSES'], '1 Pablo, Silvano y Timoteo, a la iglesia de los tesalonicenses'),
    ('2TH', ['II TESALONICENSES', '2 TESALONICENSES'], '1 Pablo, Silvano y Timoteo, a la iglesia de los tesalonicenses en Dios'),
    ('1TI', ['I TIMOTEO', '1 TIMOTEO'], '1 Pablo, apóstol de Cristo Jesús por mandato de Dios'),
    ('2TI', ['II TIMOTEO', '2 TIMOTEO'], '1 Pablo, apóstol de Cristo Jesús por voluntad de Dios, según la promesa'),
    ('TIT', ['CARTA A TITO', 'TITO'], '1 Pablo, siervo de Dios, apóstol de Jesucristo'),
    ('PHM', ['CARTA A FILEMÓN', 'FILEMÓN'], '1 Pablo, prisionero de Cristo Jesús, y Timoteo'),
    ('HEB', ['CARTA A LOS HEBREOS', 'HEBREOS'], '1 En muchas ocasiones y de muchas maneras'),
    ('JAS', ['CARTA DE SANTIAGO', 'SANTIAGO'], '1 Santiago, siervo de Dios'),
    ('1PE', ['I PEDRO', '1 PEDRO'], '1 Pedro, apóstol de Jesucristo'),
    ('2PE', ['II PEDRO', '2 PEDRO'], '1 Simón Pedro, siervo'),
    ('1JN', ['I JUAN', '1 JUAN'], '1 Lo que existía desde el principio'),
    ('2JN', ['II JUAN', '2 JUAN'], '1 El Presbítero a la Dama'),
    ('3JN', ['III JUAN', '3 JUAN'], '1 El Presbítero, al querido Gayo'),
    ('JUD', ['CARTA DE JUDAS', 'JUDAS'], '1 Judas, siervo de Jesucristo'),
    ('REV', ['APOCALIPSIS'], '1 Revelación de Jesucristo')
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
                # Lógica robusta para cambio de capítulo
                if current_verse > 0: # Si ya llevamos versículos, el 1 indica nuevo capítulo
                     is_new_verse = True
                     current_chapter += 1
                elif current_chapter == 1 and current_verse == 0: # Primer versículo del libro
                     is_new_verse = True
            elif new_verse_num > current_verse and new_verse_num <= current_verse + 10:
                is_new_verse = True
            elif re.match(r'^[\*\?m]', line):
                is_new_verse = True
        
        if is_new_verse:
            # Guardar versículo ANTERIOR
            if buffer and current_verse > 0:
                v_obj = {
                    'book': book_code,
                    'chapter': current_chapter if new_verse_num != 1 else current_chapter - 1,
                    'verse': current_verse,
                    'text': clean_text(buffer)
                }
                if current_comment:
                    v_obj['comment'] = current_comment
                verses.append(v_obj)
            
            # Iniciar NUEVO versículo
            current_verse = new_verse_num if new_verse_num else current_verse + 1
            buffer = line
            
            # Asignar comentarios pendientes
            if pending_comment:
                current_comment = "<br>".join(pending_comment)
                pending_comment = []
            else:
                current_comment = None
            
        else:
            # Detectar Títulos y Referencias
            is_title = False
            if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,:;-]+$', line) and len(line) > 3: is_title = True
            elif re.match(r'^(Mt|Mc|Lc|Jn|Hch|Rm|1Co|2Co|Gén|Ex|Lev|Num|Dt|Jos|Jue|Rut|1S|2S|1R|2R|1Cr|2Cr|Esd|Neh|Tob|Jdt|Est|1M|2M|Job|Sal|Prov|Ecl|Cant|Sab|Eclo|Is|Jer|Lam|Bar|Ez|Dan|Os|Jl|Am|Abd|Jon|Miq|Nah|Hab|Sof|Ag|Zac|Mal)\s+\d+', line): is_title = True
            elif re.match(r'^[IVX]+\.\s', line): is_title = True
            
            if is_title:
                if re.match(r'^(Mt|Mc|Lc|Jn|Gén|Ex)', line):
                    fmt = f"<em>{line}</em>"
                else:
                    fmt = f"<strong>{line}</strong>"
                pending_comment.append(fmt)
            else:
                if len(line) > 2:
                    buffer += " " + line

    # Guardar último versículo
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

print(f"Total líneas: {len(full_text)}")

# Encontrar inicio de cada libro
# Encontrar inicio de cada libro
book_starts = {}

# Mapa de títulos a códigos para búsqueda rápida
title_map = {}
for code, titles, _ in NT_BOOKS:
    for t in titles:
        title_map[t] = code

print("Buscando libros por Título + Versículo 1 (en zona NT > 100,000)...")

for i in range(100000, len(full_text)):
    line = full_text[i].strip()
    if not line: continue
    
    line_upper = line.upper()
    
    # Es un título conocido?
    possible_code = None
    for title, code in title_map.items():
        # Coincidencia exacta o muy cercana
        if line_upper == title or (title in line_upper and len(line_upper) < len(title) + 10):
            possible_code = code
            break
    
    if possible_code and possible_code not in book_starts:
        # Verificar si hay un versículo 1 en las próximas 300 líneas
        # (Aumentamos rango porque hay introducciones largas)
        found_verse_1 = False
        verse_line_idx = -1
        
        for j in range(1, 300):
            if i+j >= len(full_text): break
            next_line = full_text[i+j].strip()
            
            # Patrón de versículo 1: "1 Texto..." o "1. Texto..."
            if re.match(r'^1[\s\.]+[A-ZÁÉÍÓÚÑ"“]', next_line):
                found_verse_1 = True
                verse_line_idx = i+j
                break
        
        if found_verse_1:
            print(f"Encontrado {possible_code} en línea {i} (Verso 1 en {verse_line_idx})")
            book_starts[possible_code] = verse_line_idx # Usamos la línea del verso 1 como inicio de extracción
        
# Verificar faltantes
missing = [b[0] for b in NT_BOOKS if b[0] not in book_starts]
if missing:
    print(f"⚠️ Faltan: {missing}")
    # Intentar búsqueda de frase para los faltantes (fallback)
    for code in missing:
        # ... lógica de frase si es necesario ...
        pass


# Ordenar libros por posición en el archivo (CRUCIAL para extracción correcta)
sorted_books_by_pos = sorted(book_starts.items(), key=lambda x: x[1])

print("\nOrden de libros detectado en el archivo:")
for code, pos in sorted_books_by_pos:
    print(f"  {code}: {pos}")

# Extraer y procesar
all_verses = []

for i, (code, start_line) in enumerate(sorted_books_by_pos):
    # El final es el inicio del siguiente libro encontrado
    if i < len(sorted_books_by_pos) - 1:
        next_code, end_line = sorted_books_by_pos[i+1]
    else:
        end_line = len(full_text)
    
    print(f"Procesando {code} (Líneas {start_line}-{end_line})...")
    
    # Extraer bloque de texto
    raw_lines = full_text[start_line:end_line]
    processed_text = preprocess_text("".join(raw_lines))
    
    verses = extract_verses(code, processed_text.split('\n'))
    print(f"  ✓ {len(verses)} versículos extraídos.")
    all_verses.extend(verses)

# Guardar JSON
with open('scripts/nt_full_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\nTotal NT: {len(all_verses)} versículos.")

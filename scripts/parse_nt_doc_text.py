import re
import json

# Mapeo de libros del NT
NT_BOOKS_MAP = {
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN',
    'HECHOS': 'ACT', 'ROMANOS': 'ROM',
    '1ª CARTA A LOS CORINTIOS': '1CO', '2ª CARTA A LOS CORINTIOS': '2CO',
    'GÁLATAS': 'GAL', 'EFESIOS': 'EPH', 'FILIPENSES': 'PHP', 'COLOSENSES': 'COL',
    '1ª CARTA A LOS TESALONICENSES': '1TH', '2ª CARTA A LOS TESALONICENSES': '2TH',
    '1ª CARTA A TIMOTEO': '1TI', '2ª CARTA A TIMOTEO': '2TI',
    'TITO': 'TIT', 'FILEMÓN': 'PHM', 'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS',
    '1ª CARTA DE SAN PEDRO': '1PE', '2ª CARTA DE SAN PEDRO': '2PE',
    '1ª CARTA DE SAN JUAN': '1JN', '2ª CARTA DE SAN JUAN': '2JN', '3ª CARTA DE SAN JUAN': '3JN',
    'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

def parse_nt_text(file_path):
    print(f"Leyendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    # Patrones
    book_pattern = re.compile(r'EL EVANGELIO SEGÚN SAN ([A-Z]+)|LOS HECHOS DE LOS APÓSTOLES|LAS CARTAS.*|LA CARTA.*|EL APOCALIPSIS')
    chapter_pattern = re.compile(r'^\s*(\d+)\s*$')
    verse_start_pattern = re.compile(r'^\s*(\d+)\s+(.+)')
    section_title_pattern = re.compile(r'^([A-ZÁÉÍÓÚÑ][a-zñáéíóúü\s,\.:]+)(\s*\(\d+.*)?$')
    
def parse_nt_text(file_path):
    print(f"Leyendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    # Mapeo inverso para detectar libros
    # Solo usaremos estos si aparecen en líneas específicas
    
    # Mapa de líneas de inicio de libros (basado en análisis del archivo)
    BOOK_STARTS = {
        393: 'MAT',
        2833: 'MRK',
        4562: 'LUK',
        7295: 'JHN',
        9331: 'ACT',
        11465: 'ROM',
        12450: '1CO',
        13161: '2CO',
        13686: 'GAL',
        14019: 'EPH',
        14332: 'PHP',
        14545: 'COL',
        14801: '1TH',
        14972: '2TH',
        15084: '1TI',
        15357: '2TI',
        15529: 'TIT',
        15631: 'PHM',
        15698: 'HEB',
        16470: 'JAS',
        16705: '1PE',
        16993: '2PE',
        17187: '1JN',
        17414: '2JN',
        17453: '3JN',
        17488: 'JUD',
        17589: 'REV'
    }
    
    # Rango de tolerancia para encontrar el título (por si cambian ligeramente las líneas)
    TOLERANCE = 5
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Verificar si estamos cerca de un inicio de libro conocido
        for start_line, book_code in BOOK_STARTS.items():
            if abs(i - start_line) <= TOLERANCE:
                # Verificar si la línea parece un título (mayúsculas) para confirmar
                if line.isupper() and len(line) > 5:
                    if current_book != book_code:
                        current_book = book_code
                        current_chapter = 0
                        print(f"Cambio de libro: {current_book} (Línea {i})")
        
        if not line:
            i += 1
            continue

        # 2. Detectar Capítulo
        # En este archivo, los capítulos son números aislados en una línea
        if re.match(r'^\d+$', line) and len(line) < 4:
            try:
                chap = int(line)
                # Validación simple: los capítulos son secuenciales o es el 1
                if chap == current_chapter + 1 or (chap == 1):
                    current_chapter = chap
                    # print(f"  Capítulo {current_chapter}")
                    i += 1
                    continue
            except:
                pass

        # 3. Detectar Título de Sección
        # Heurística: Línea que no empieza con número, tiene paréntesis con referencias, o es corta y descriptiva
        # Y NO es parte de un versículo (difícil de saber)
        # En este archivo, los títulos suelen tener referencias abajo: "(Lc 3,23-38)"
        is_title = False
        if not line[0].isdigit():
            # Si tiene referencia explícita
            if "(" in line and ")" in line and any(c.isdigit() for c in line):
                is_title = True
            # Si la siguiente línea es una referencia
            elif i+1 < len(lines) and lines[i+1].strip().startswith("(") and ")" in lines[i+1]:
                is_title = True
            # Si la siguiente línea es un número de capítulo
            elif i+1 < len(lines) and re.match(r'^\d+$', lines[i+1].strip()):
                is_title = True
            # Si la siguiente línea empieza con número de versículo (1 ...)
            elif i+1 < len(lines) and re.match(r'^\d+\s+', lines[i+1].strip()):
                is_title = True
                
        if is_title:
            # Limpiar el título de referencias
            current_section_title = line.split('(')[0].strip()
            i += 1
            continue

        # 4. Detectar Versículos
        if current_book and current_chapter > 0:
            # Buscar inicio de versículo: "N Texto"
            # Puede haber múltiples en una línea: "1 Texto. 2 Texto."
            
            # Regex para encontrar números de versículo seguidos de texto
            # Usamos finditer para encontrar todas las ocurrencias
            
            # Patrón: un número, espacio, texto... hasta el siguiente número espacio o fin
            # Pero cuidado con números dentro del texto.
            # Asumimos que el número de versículo está precedido por inicio de línea o punto/espacio
            
            # Estrategia: Dividir la línea por números que parecen versículos
            
            # Primero, ¿empieza la línea con un número?
            if re.match(r'^\d+\s+', line):
                # Es una línea de versículos
                parts = re.split(r'(\d+)\s+', line)
                # parts[0] vacío, parts[1] num, parts[2] text, parts[3] num, parts[4] text...
                
                idx = 1
                while idx < len(parts):
                    v_num = int(parts[idx])
                    v_text = parts[idx+1].strip() if idx+1 < len(parts) else ""
                    
                    # A veces el split separa mal si hay números en el texto.
                    # Pero en este formato parece consistente: "2 Abrahán... 3 Judá..."
                    
                    # Verificar si el siguiente "número" es realmente un versículo
                    # (heurística: es secuencial o cercano al anterior?)
                    # Por ahora confiamos en el formato
                    
                    verses.append({
                        'book': current_book,
                        'chapter': current_chapter,
                        'verse': v_num,
                        'text': v_text,
                        'section_title': current_section_title
                    })
                    current_section_title = None # El título aplica al primer versículo del grupo
                    
                    idx += 2
            
            # Si no empieza con número, es continuación del versículo anterior
            elif verses and not is_title:
                verses[-1]['text'] += " " + line

        i += 1

    return verses

# Ejecutar
extracted_file = 'scripts/nt_doc_extracted.txt'
print(f"Procesando {extracted_file}...")
verses = parse_nt_text(extracted_file)

print(f"\nTotal versículos extraídos: {len(verses)}")

# Guardar
output_json = 'scripts/navarra_nt_doc.json'
with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)
print(f"Guardado en {output_json}")

# Estadísticas
books_found = {}
for v in verses:
    b = v['book']
    books_found[b] = books_found.get(b, 0) + 1

print("\nVersículos por libro:")
for b, c in sorted(books_found.items()):
    print(f"  {b}: {c}")

import re
import json

# Mapa exacto de líneas de inicio de libros (del análisis anterior)
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

def is_section_title(line, next_line):
    """Detecta si una línea es un título de sección."""
    if not line or len(line) < 5:
        return False
    
    # Los títulos no empiezan con número
    if line[0].isdigit():
        return False
    
    # Ignorar líneas que son claramente continuación de versículos
    # (terminan con coma, punto y coma, "y", conjunciones)
    if line.endswith((',', ';', ' y', ' de', ' del', ' en', ' con')):
        return False
    
    # Patrón A: Tiene referencia en la misma línea
    # Ej: "Genealogía de Jesucristo (1,1-17)"
    if re.search(r'\(\d+[,\-\d]*\)', line):
        return True
    
    # Patrón B: La siguiente línea es una referencia
    # Ej: línea = "Adoración de los Magos", next = "(Mt 2,1-12)"
    if next_line and next_line.strip().startswith('(') and ')' in next_line:
        # Verificar que tenga números (referencias bíblicas)
        if any(c.isdigit() for c in next_line):
            return True
    
    # Patrón C: La siguiente línea es un número de capítulo
    if next_line and re.match(r'^\d+$', next_line.strip()):
        return True
    
    # Patrón D: La siguiente línea empieza con "1 " (capítulo 1, versículo 1)
    if next_line and re.match(r'^1\s+[A-Z]', next_line.strip()):
        return True
    
    return False

def is_chapter_number(line):
    """Detecta si una línea es solo un número de capítulo."""
    stripped = line.strip()
    return re.match(r'^\d+$', stripped) and len(stripped) <= 3

def extract_verses_from_line(line):
    """
    Extrae todos los versículos de una línea.
    Retorna lista de tuplas (verse_num, text).
    """
    # Buscar patrón "N Texto" al inicio
    match = re.match(r'^(\d+)\s+(.+)$', line)
    if not match:
        return []
    
    first_verse = int(match.group(1))
    rest = match.group(2)
    
    # Ahora buscar versículos adicionales dentro del texto: " N Texto"
    # Pero cuidado con números que son parte del texto (años, cantidades, etc.)
    # Patrón: espacio + número + espacio + letra mayúscula (inicio de oración)
    
    verses = []
    current_verse = first_verse
    current_text = ""
    
    # Split por el patrón " \d+ " pero conservando el número
    parts = re.split(r'(\s\d+\s)', rest)
    
    if len(parts) == 1:
        # No hay más versículos, todo es texto del primer versículo
        verses.append((first_verse, rest))
    else:
        # Hay múltiples versículos
        current_text = parts[0]  # Texto del primer versículo
        
        i = 1
        while i < len(parts):
            separator = parts[i]  # " N "
            
            # Extraer el número
            num_match = re.search(r'\d+', separator)
            if num_match:
                # Guardar el versículo actual
                verses.append((current_verse, current_text.strip()))
                
                # El siguiente número es el nuevo versículo
                current_verse = int(num_match.group())
                current_text = parts[i+1] if i+1 < len(parts) else ""
                i += 2
            else:
                # No debería pasar, pero por si acaso
                current_text += separator + (parts[i+1] if i+1 < len(parts) else "")
                i += 2
        
        # Guardar el último versículo
        if current_text:
            verses.append((current_verse, current_text.strip()))
    
    return verses

def parse_nt_improved(file_path):
    print(f"Leyendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()  # Mantener espacios iniciales
        next_line = lines[i+1].strip() if i+1 < len(lines) else ""
        
        # 1. Detectar cambio de libro
        for start_line, book_code in BOOK_STARTS.items():
            if i == start_line or (abs(i - start_line) <= 2 and line.isupper() and len(line) > 10):
                if current_book != book_code:
                    current_book = book_code
                    current_chapter = 0
                    print(f"📖 {current_book} (línea {i})")
                break
        
        # Saltar líneas vacías
        if not line.strip():
            i += 1
            continue
        
        # Ignorar líneas de navegación
        if "Ir a" in line or "[Ir a" in line:
            i += 1
            continue
        
        # 2. Detectar capítulo
        if is_chapter_number(line):
            new_chapter = int(line.strip())
            # Validar que sea secuencial o sea el 1
            if new_chapter == current_chapter + 1 or new_chapter == 1:
                current_chapter = new_chapter
                # print(f"  Cap {current_chapter}")
                i += 1
                continue
        
        # 3. Detectar título de sección
        if current_book and is_section_title(line.strip(), next_line):
            # Limpiar el título (quitar referencias)
            title = re.sub(r'\s*\(\d+[,\-\d]*\)\s*$', '', line.strip())
            current_section_title = title
            # print(f"    📌 {title}")
            i += 1
            continue
        
        # 4. Detectar y extraer versículos
        if current_book and current_chapter > 0:
            stripped = line.strip()
            
            # ¿Empieza con número? Es inicio de versículo(s)
            if stripped and stripped[0].isdigit():
                verse_list = extract_verses_from_line(stripped)
                
                for v_num, v_text in verse_list:
                    # Crear el versículo
                    verse_data = {
                        'book': current_book,
                        'chapter': current_chapter,
                        'verse': v_num,
                        'text': v_text,
                        'section_title': current_section_title
                    }
                    verses.append(verse_data)
                    
                    # El título solo aplica al primer versículo
                    current_section_title = None
                
                i += 1
                continue
            
            # Si NO empieza con número y NO es título, es continuación del versículo anterior
            elif verses and not is_section_title(stripped, next_line):
                # Agregar al último versículo
                verses[-1]['text'] += " " + stripped
                i += 1
                continue
        
        i += 1
    
    return verses

# Ejecutar
if __name__ == '__main__':
    input_file = 'scripts/nt_doc_extracted.txt'
    output_file = 'scripts/navarra_nt_v2.json'
    
    print("Parseando NT con lógica mejorada...")
    verses = parse_nt_improved(input_file)
    
    print(f"\n✓ Total versículos extraídos: {len(verses)}")
    
    # Estadísticas por libro
    books_stats = {}
    for v in verses:
        b = v['book']
        books_stats[b] = books_stats.get(b, 0) + 1
    
    print("\n📊 Versículos por libro:")
    for book in sorted(books_stats.keys()):
        print(f"  {book}: {books_stats[book]}")
    
    # Verificar libros problemáticos
    print("\n🔍 Verificación de libros pequeños:")
    for book_code, expected in [('2JN', 13), ('3JN', 14), ('JUD', 25), ('PHM', 25)]:
        actual = books_stats.get(book_code, 0)
        status = "✓" if actual > 0 else "❌"
        print(f"  {status} {book_code}: {actual} versículos (esperados ~{expected})")
    
    # Guardar
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Guardado en {output_file}")

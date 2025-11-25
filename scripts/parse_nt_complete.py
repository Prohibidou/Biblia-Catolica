import PyPDF2
import re
import json

# Mapeo de libros del NT
NT_BOOKS = {
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN',
    'HECHOS': 'ACT',
    'ROMANOS': 'ROM',
    '1 CORINTIOS': '1CO', '2 CORINTIOS': '2CO',
    'GÁLATAS': 'GAL', 'EFESIOS': 'EPH', 'FILIPENSES': 'PHP',
    'COLOSENSES': 'COL',
    '1 TESALONICENSES': '1TH', '2 TESALONICENSES': '2TH',
    '1 TIMOTEO': '1TI', '2 TIMOTEO': '2TI',
    'TITO': 'TIT', 'FILEMÓN': 'PHM',
    'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS',
    '1 PEDRO': '1PE', '2 PEDRO': '2PE',
    '1 JUAN': '1JN', '2 JUAN': '2JN', '3 JUAN': '3JN',
    'JUDAS': 'JUD',
    'APOCALIPSIS': 'REV'
}

def extract_nt_with_titles(pdf_path, start_page=2530, end_page=3200):
    """
    Extrae el NT con versículos y títulos de secciones.
    """
    print(f"Abriendo PDF...")
    pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))
    
    print(f"Procesando páginas {start_page} a {end_page}...")
    
    current_book = None
    current_chapter = 1
    verses = []
    
    # Procesar cada página
    for page_num in range(start_page - 1, min(end_page, len(pdf.pages))):
        if (page_num - start_page + 1) % 50 == 0:
            print(f"  Procesando página {page_num + 1}... ({len(verses)} versículos extraídos)")
        
        text = pdf.pages[page_num].extract_text()
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Detectar cambio de libro
            for book_name, book_code in NT_BOOKS.items():
                if book_name in line.upper() and 'EVANGELIO' in text.upper()[:500]:
                    # Es un título de libro
                    if 'SEGÚN' in line.upper() or book_name in ['HECHOS', 'ROMANOS', 'APOCALIPSIS']:
                        current_book = book_code
                        current_chapter = 1
                        print(f"\n  → Encontrado libro: {book_name} ({book_code})")
                        break
                elif book_name in line.upper() and len(line) < 30:  # Nombre corto de libro
                    current_book = book_code
                    current_chapter = 1
                    print(f"\n  → Encontrado libro: {book_name} ({book_code})")
                    break
            
            # Detectar número de capítulo
            if re.match(r'^\d+$', line) and len(line) <= 3:
                # Podría ser un número de capítulo
                # Verificar contexto
                try:
                    chapter_num = int(line)
                    # Verificar si es seguido por un título o versículo
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # Si la siguiente línea es un título o empieza con número, es capítulo
                        if (not next_line.isdigit() and len(next_line) > 5) or next_line.isdigit():
                            if chapter_num > current_chapter or chapter_num == 1:
                                current_chapter = chapter_num
                except:
                    pass
            
            # Detectar títulos de sección (líneas que no son versículos)
            # Los títulos suelen estar antes de los versículos
            if (line and not line.isdigit() and len(line) > 10 and 
                not line.startswith('—') and  # No es diálogo
                not any(ref in line for ref in ['Mc ', 'Mt ', 'Lc ', 'Jn ', 'Rm ']) and  # No es referencia
                not re.match(r'^\d+\s+\w+$', line)):  # No es "1 Mt" o similar
                
                # Verificar si la siguiente línea es un número de versículo
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if re.match(r'^\d+$', next_line) and int(next_line) < 100:
                        # Es un título de sección
                        # El siguiente versículo tendrá este título
                        section_title = line
                        # Buscar el versículo siguiente
                        j = i + 1
                        while j < len(lines) and j < i + 10:
                            verse_line = lines[j].strip()
                            if re.match(r'^\d+$', verse_line):
                                verse_num = int(verse_line)
                                # Obtener el texto del versículo (líneas siguientes hasta el próximo número)
                                verse_text = ''
                                k = j + 1
                                while k < len(lines) and k < j + 20:
                                    text_line = lines[k].strip()
                                    if re.match(r'^\d+$', text_line) or '=====' in text_line:
                                        break
                                    if text_line and not text_line.startswith('Lc ') and not text_line.startswith('Mt '):
                                        verse_text += ' ' + text_line
                                    k += 1
                                
                                if verse_text.strip() and current_book:
                                    verses.append({
                                        'book': current_book,
                                        'chapter': current_chapter,
                                        'verse': verse_num,
                                        'text': verse_text.strip(),
                                        'section_title': section_title
                                    })
                                
                                i = k - 1
                                break
                            j += 1
            
            # Detectar versículos normales (sin título de sección previo)
            if re.match(r'^\d+$', line) and len(line) <= 3:
                try:
                    verse_num = int(line)
                    if verse_num > 0 and verse_num < 200 and current_book:
                        # Obtener el texto del versículo
                        verse_text = ''
                        j = i + 1
                        while j < len(lines) and j < i + 15:
                            text_line = lines[j].strip()
                            if re.match(r'^\d+$', text_line) or '=====' in text_line:
                                break
                            if text_line and not any(ref in text_line for ref in ['Mc ', 'Mt ', 'Lc ', 'Jn ']):
                                verse_text += ' ' + text_line
                            j += 1
                        
                        if verse_text.strip() and len(verse_text) > 10:
                            # Verificar que no lo hayamos agregado ya con un título
                            already_added = any(
                                v['book'] == current_book and 
                                v['chapter'] == current_chapter and 
                                v['verse'] == verse_num 
                                for v in verses[-5:] if verses
                            )
                            
                            if not already_added:
                                verses.append({
                                    'book': current_book,
                                    'chapter': current_chapter,
                                    'verse': verse_num,
                                    'text': verse_text.strip(),
                                    'section_title': None
                                })
                        
                        i = j - 1
                except:
                    pass
            
            i += 1
    
    return verses

# Ejecutar extracción
pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
print("Iniciando extracción del Nuevo Testamento...\n")

verses = extract_nt_with_titles(pdf_path, start_page=2530, end_page=3200)

print(f"\n{'='*70}")
print(f"RESUMEN:")
print(f"  Total de versículos extraídos: {len(verses)}")

# Contar versículos con títulos
with_titles = sum(1 for v in verses if v.get('section_title'))
print(f"  Versículos con título de sección: {with_titles}")

# Contar libros
books = set(v['book'] for v in verses if v.get('book'))
print(f"  Libros extraídos: {len(books)}")
print(f"  Códigos: {', '.join(sorted(books))}")

# Guardar JSON
output_file = 'scripts/navarra_nt.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)

print(f"\n✓ Versículos guardados en {output_file}")

# Mostrar ejemplos
print(f"\n{'='*70}")
print("EJEMPLOS DE VERSÍCULOS EXTRAÍDOS:")
print(f"{'='*70}\n")

for v in verses[:5]:
    title_info = f" [{v['section_title']}]" if v.get('section_title') else ""
    print(f"{v['book']} {v['chapter']}:{v['verse']}{title_info}")
    print(f"  {v['text'][:100]}...")
    print()

print(f"\n✅ Extracción completada. Ahora convertir a SQLite...")

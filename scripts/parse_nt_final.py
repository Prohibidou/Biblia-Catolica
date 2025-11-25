import re
import json

# Códigos de libros
BOOK_MAP = {
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN',
    'HECHOS': 'ACT', 'ROMANOS': 'ROM',
    'CORINTIOS_1': '1CO', 'CORINTIOS_2': '2CO',
    'GÁLATAS': 'GAL', 'EFESIOS': 'EPH', 'FILIPENSES': 'PHP', 'COLOSENSES': 'COL',
    'TESALONICENSES_1': '1TH', 'TESALONICENSES_2': '2TH',
    'TIMOTEO_1': '1TI', 'TIMOTEO_2': '2TI',
    'TITO': 'TIT', 'FILEMÓN': 'PHM', 'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS',
    'PEDRO_1': '1PE', 'PEDRO_2': '2PE',
    'JUAN_1': '1JN', 'JUAN_2': '2JN', 'JUAN_3': '3JN',
    'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

# Líneas exactas de inicio (del análisis previo)
BOOK_STARTS = {
    393: 'MAT', 2833: 'MRK', 4562: 'LUK', 7295: 'JHN',
    9331: 'ACT', 11465: 'ROM',
    12450: '1CO', 13161: '2CO', 13686: 'GAL',
    14019: 'EPH', 14332: 'PHP', 14545: 'COL',
    14801: '1TH', 14972: '2TH',
    15084: '1TI', 15357: '2TI', 15529: 'TIT',
    15631: 'PHM', 15698: 'HEB', 16470: 'JAS',
    16705: '1PE', 16993: '2PE',
    17187: '1JN', 17414: '2JN', 17453: '3JN',
    17488: 'JUD', 17589: 'REV'
}

def parse_nt_final(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    # Libros de un solo capítulo
    single_chapter_books = {'PHM', '2JN', '3JN', 'JUD'}
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Saltar vacías
        if not line:
            i += 1
            continue
        
        # 1. Detectar libro por línea exacta
        for start_line, book_code in BOOK_STARTS.items():
            if abs(i - start_line) <= 3:  # Tolerancia de 3 líneas
                # Verificar que la línea parece un título
                if line.isupper() and len(line) > 5:
                    if current_book != book_code:
                        current_book = book_code
                        current_chapter = 1 if book_code in single_chapter_books else 0
                        print(f"📖 {current_book} (línea {i})")
                    break
        
        # 2. Capítulo (número solo)
        if re.match(r'^\d+$', line) and len(line) < 4 and current_book not in single_chapter_books:
            chap = int(line)
            if chap == current_chapter + 1 or chap == 1:
                current_chapter = chap
                i += 1
                continue
        
        # 3. Título de sección
        is_section = False
        if current_book and not line[0].isdigit():
            if "(" in line and ")" in line and any(c.isdigit() for c in line):
                is_section = True
            elif i+1 < len(lines) and lines[i+1].strip().startswith("("):
                is_section = True
            
            if is_section:
                current_section_title = re.sub(r'\([^)]+\)', '', line).strip()
                i += 1
                continue
        
        # 4. Versículos
        if current_book and current_chapter > 0 and line and line[0].isdigit():
            # Dividir por "número + espacio"
            parts = re.split(r'(\d+)\s+', line)
            
            idx = 1
            while idx < len(parts) - 1:
                v_num = int(parts[idx])
                v_text = parts[idx + 1]
                
                v_text = v_text.strip()
                
                verses.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': v_num,
                    'text': v_text,
                    'section_title': current_section_title
                })
                current_section_title = None
                idx += 2
            
            i += 1
            continue
        
        # 5. Continuación
        if verses and current_book and current_chapter > 0 and not is_section:
            verses[-1]['text'] += " " + line
        
        i += 1
    
    return verses

if __name__ == '__main__':
    print("Parseando NT (versión final)...")
    verses = parse_nt_final('scripts/nt_doc_extracted_blocks.txt')
    print(f"\n✓ Total: {len(verses)} versículos")
    
    # Estadísticas
    stats = {}
    for v in verses:
        stats[v['book']] = stats.get(v['book'], 0) + 1
    
    print("\nPor libro:")
    for book in sorted(stats.keys()):
        print(f"  {book}: {stats[book]}")
    
    # Guardar
    with open('scripts/navarra_nt_final.json', 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Guardado en navarra_nt_final.json")

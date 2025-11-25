import re
import json

# Mapa de libros (códigos estándar)
BOOK_CODES = {
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN',
    'HECHOS': 'ACT', 'ROMANOS': 'ROM',
    'CORINTIOS': '1CO', # Lógica especial para 1/2
    'GÁLATAS': 'GAL', 'EFESIOS': 'EPH', 'FILIPENSES': 'PHP', 'COLOSENSES': 'COL',
    'TESALONICENSES': '1TH', # Lógica especial
    'TIMOTEO': '1TI', # Lógica especial
    'TITO': 'TIT', 'FILEMÓN': 'PHM', 'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS',
    'PEDRO': '1PE', # Lógica especial
    'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

def clean_line(line):
    return line.strip()

def is_book_title(line):
    """Detecta si una línea es un título de libro."""
    upper = line.upper()
    if len(upper) < 5: return False
    
    # Patrones claros de títulos
    if "EVANGELIO SEGÚN SAN" in upper: return True
    if "HECHOS DE LOS APÓSTOLES" in upper: return True
    if "CARTA A" in upper or "CARTA DE" in upper: return True
    if "APOCALIPSIS" in upper and len(upper) < 30: return True
    
    return False

def get_book_code(line):
    upper = line.upper()
    
    if "MATEO" in upper: return 'MAT'
    if "MARCOS" in upper: return 'MRK'
    if "LUCAS" in upper: return 'LUK'
    if "JUAN" in upper:
        if "EVANGELIO" in upper: return 'JHN'
        if "PRIMERA" in upper or "1" in upper: return '1JN'
        if "SEGUNDA" in upper or "2" in upper: return '2JN'
        if "TERCERA" in upper or "3" in upper: return '3JN'
        # Por defecto si solo dice "CARTA DE SAN JUAN" (raro)
        return '1JN' 
        
    if "HECHOS" in upper: return 'ACT'
    if "ROMANOS" in upper: return 'ROM'
    
    if "CORINTIOS" in upper: return '1CO' if "PRIMERA" in upper or "1" in upper else '2CO'
    if "TESALONICENSES" in upper: return '1TH' if "PRIMERA" in upper or "1" in upper else '2TH'
    if "TIMOTEO" in upper: return '1TI' if "PRIMERA" in upper or "1" in upper else '2TI'
    if "PEDRO" in upper: return '1PE' if "PRIMERA" in upper or "1" in upper else '2PE'
    
    if "GÁLATAS" in upper: return 'GAL'
    if "EFESIOS" in upper: return 'EPH'
    if "FILIPENSES" in upper: return 'PHP'
    if "COLOSENSES" in upper: return 'COL'
    if "TITO" in upper: return 'TIT'
    if "FILEMÓN" in upper: return 'PHM'
    if "HEBREOS" in upper: return 'HEB'
    if "SANTIAGO" in upper: return 'JAS'
    if "JUDAS" in upper: return 'JUD'
    if "APOCALIPSIS" in upper: return 'REV'
    
    return None

def parse_nt_v3(file_path):
    print(f"Leyendo {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    # Estado para manejar libros pequeños (1 cap)
    is_single_chapter_book = False
    
    i = 0
    while i < len(lines):
        line = clean_line(lines[i])
        
        if not line:
            i += 1
            continue
            
        # 1. Detectar Libro
        if is_book_title(line):
            # Verificar con línea siguiente para confirmar (a veces el título está dividido)
            full_title = line
            if i+1 < len(lines) and lines[i+1].strip().isupper():
                full_title += " " + lines[i+1].strip()
            
            code = get_book_code(full_title)
            if code:
                current_book = code
                current_chapter = 0
                is_single_chapter_book = code in ['PHM', '2JN', '3JN', 'JUD']
                if is_single_chapter_book:
                    current_chapter = 1 # Estos libros tienen un solo capítulo implícito
                
                print(f"📖 LIBRO DETECTADO: {current_book} (Línea {i})")
                i += 1
                continue

        # 2. Detectar Capítulo (número solo)
        if re.match(r'^\d+$', line) and len(line) < 4:
            try:
                chap = int(line)
                # Validar
                if chap == current_chapter + 1 or chap == 1:
                    current_chapter = chap
                    # print(f"  Capítulo {current_chapter}")
                    i += 1
                    continue
            except:
                pass
                
        # 3. Detectar Título de Sección
        is_title = False
        if current_book and not line[0].isdigit():
            # Si tiene referencia explícita (Mt 1,1)
            if "(" in line and ")" in line and any(c.isdigit() for c in line):
                is_title = True
            # Si la siguiente línea es referencia
            elif i+1 < len(lines) and lines[i+1].strip().startswith("(") and ")" in lines[i+1]:
                is_title = True
                
            if is_title:
                # Limpiar referencia del título
                current_section_title = re.sub(r'\s*\([^)]+\).*', '', line).strip()
                i += 1
                continue

        # 4. Detectar Versículos
        if current_book and current_chapter > 0:
            # Buscar inicio de versículo "N Texto"
            # Ojo: A veces es "1 Texto 2 Texto" o "1 Texto. 2 Texto"
            if re.match(r'^\d+\s+', line):
                # Split por (espacio o punto) + número + espacio
                parts = re.split(r'(?:^|\s|\.)((\d+)\s+', line)
                
                idx = 1
                # Procesar parts
                if not parts[0].strip() and len(parts) > 1:
                    idx = 1
                elif len(parts) > 1 and parts[1].isdigit():
                     idx = 1
                else:
                     idx = 1

                while idx < len(parts):
                    if parts[idx] and parts[idx].isdigit():
                        v_num = int(parts[idx])
                        v_text = parts[idx+1].strip() if idx+1 < len(parts) else ""
                        
                        # Limpiar texto de puntos iniciales si quedaron
                        if v_text.startswith('.'): v_text = v_text[1:].strip()
                        
                        verses.append({
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': v_num,
                            'text': v_text,
                            'section_title': current_section_title
                        })
                        current_section_title = None
                        idx += 2
                    else:
                        idx += 1
                
                i += 1
                continue
            
            # Continuación de versículo
            elif verses and not is_title:
                # Añadir al último versículo
                verses[-1]['text'] += " " + line
                i += 1
                continue
                
        i += 1
        
    return verses

if __name__ == '__main__':
    input_file = 'scripts/nt_doc_extracted_blocks.txt'
    output_file = 'scripts/navarra_nt_v3.json'
    
    if re.search(r'careful', input_file):
        print("⚠️ Asegúrate de que la extracción 'careful' haya terminado antes de ejecutar esto.")
    
    verses = parse_nt_v3(input_file)
    print(f"Total versículos: {len(verses)}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)

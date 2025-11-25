import re
import json

# Estructura canónica para saber cuándo acaba un capítulo
NT_STRUCTURE = {
    'MAT': {1:25, 2:23, 3:17, 4:25, 5:48, 6:34, 7:29, 8:34, 9:38, 10:42, 11:30, 12:50, 13:58, 14:36, 15:39, 16:28, 17:27, 18:35, 19:30, 20:34, 21:46, 22:46, 23:39, 24:51, 25:46, 26:75, 27:66, 28:20},
    'MRK': {1:45, 2:28, 3:35, 4:41, 5:43, 6:56, 7:37, 8:38, 9:50, 10:52, 11:33, 12:44, 13:37, 14:72, 15:47, 16:20},
    'LUK': {1:80, 2:52, 3:38, 4:44, 5:39, 6:49, 7:50, 8:56, 9:62, 10:42, 11:54, 12:59, 13:35, 14:35, 15:32, 16:31, 17:37, 18:43, 19:48, 20:47, 21:38, 22:71, 23:56, 24:53},
    'JHN': {1:51, 2:25, 3:36, 4:54, 5:47, 6:71, 7:53, 8:59, 9:41, 10:42, 11:57, 12:50, 13:38, 14:31, 15:27, 16:33, 17:26, 18:40, 19:42, 20:31, 21:25}
}

def clean_text(text):
    # Eliminar marcadores de inicio si quedaron
    text = re.sub(r'^[\d\*\?m]+\s*', '', text)
    # Eliminar espacios extra
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_text(text):
    # Separar números pegados a letras mayúsculas (ej: "17Por" -> "17 Por")
    text = re.sub(r'(\d+)([A-ZÁÉÍÓÚÑ])', r'\1 \2', text)
    
    # Reemplazar marcadores en medio de línea por saltos de línea
    # *Judá -> \n* Judá
    text = text.replace('*', '\n* ')
    text = text.replace('?', '\n? ')
    
    # m Abrahán -> \n m Abrahán (solo si m está seguida de espacio y mayúscula)
    text = re.sub(r'\s(m\s+[A-ZÁÉÍÓÚÑ])', r'\n\1', text)
    
    return text

def parse_book(book_code, filename):
    print(f"Parseando {book_code} desde {filename}...")
    
    with open(filename, encoding='utf-8') as f:
        raw_content = f.read()
    
    # Pre-procesar contenido
    processed_content = preprocess_text(raw_content)
    lines = processed_content.split('\n')
    
    verses = []
    current_chapter = 1
    current_verse = 0 
    buffer = ""
    pending_comment = [] # Para acumular títulos y referencias
    
    # Mapeo de capítulos para este libro
    structure = NT_STRUCTURE.get(book_code, {})
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        # Detectar inicio de versículo
        new_verse_num = None
        
        # Patrones de inicio de versículo
        match_num = re.match(r'^(\d+)', line)
        if match_num:
            new_verse_num = int(match_num.group(1))
        
        # Marcadores especiales
        elif re.match(r'^[\*\?m]\s+', line) or line.startswith('*') or line.startswith('?'):
            new_verse_num = current_verse + 1
        
        # Lógica de cambio de capítulo
        if new_verse_num is not None:
            # Caso especial: Versículo 1
            if new_verse_num == 1:
                if current_verse >= 10 or (current_chapter == 1 and current_verse == 0):
                    if current_verse > 0: 
                        if buffer:
                            verses.append({
                                'book': book_code,
                                'chapter': current_chapter,
                                'verse': current_verse,
                                'text': clean_text(buffer)
                            })
                            buffer = ""
                    
                    if current_verse > 0:
                        current_chapter += 1
                    
                    current_verse = 1
                    buffer = line
                    
                    # Asignar comentarios pendientes a este nuevo versículo (el 1)
                    if pending_comment:
                        # Buscar el último versículo añadido para ver si se lo asignamos a él o al nuevo
                        # Generalmente los títulos van ANTES del versículo, así que pertenecen a este nuevo versículo
                        verses[-1]['comment'] = " ".join(pending_comment) if verses else ""
                        # O mejor, lo guardamos en el versículo actual que estamos empezando?
                        # En la estructura de Verse, el comentario suele ir asociado al versículo.
                        # Pero como aún no hemos creado el objeto versículo 1 (solo estamos en buffer),
                        # necesitamos una forma de guardarlo.
                        # Lo guardaremos en una variable temporal 'current_comment'
                        pass 
                    continue
            
            is_valid_sequence = False
            if re.match(r'^[\*\?m]', line):
                is_valid_sequence = True
            elif new_verse_num > current_verse and new_verse_num <= current_verse + 5:
                is_valid_sequence = True
            
            if is_valid_sequence:
                # Guardar versículo anterior
                if buffer:
                    v_obj = {
                        'book': book_code,
                        'chapter': current_chapter,
                        'verse': current_verse,
                        'text': clean_text(buffer)
                    }
                    # Si había comentarios acumulados ANTES de este versículo, asignarlos
                    if pending_comment:
                        v_obj['comment'] = "<br>".join(pending_comment)
                        pending_comment = []
                    
                    verses.append(v_obj)
                
                if re.match(r'^[\*\?m]', line):
                    current_verse += 1
                else:
                    current_verse = new_verse_num
                
                buffer = line
            else:
                buffer += " " + line
        else:
            # No es inicio de versículo
            # Detectar si es un título de sección o referencia
            # Títulos: Mayúsculas, Romanos
            # Referencias: Lc 1,1; Mt 3,4
            is_title = False
            if re.match(r'^[IVX]+\.\s', line): is_title = True
            elif re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,:;]+$', line) and len(line) > 3: is_title = True
            elif re.match(r'^(Mt|Mc|Lc|Jn|Hch|Rm|1Co|2Co)\s\d+', line): is_title = True
            elif "Evangelio" in line or "Capítulo" in line: is_title = True
            
            if is_title:
                # Es un título o referencia. Lo guardamos para el SIGUIENTE versículo.
                # Limpiamos un poco el formato
                formatted_title = f"<strong>{line}</strong>" if not re.match(r'^(Mt|Mc|Lc|Jn)', line) else f"<em>{line}</em>"
                pending_comment.append(formatted_title)
            else:
                # Texto normal que continúa el versículo anterior o es basura
                # Si parece texto narrativo, lo añadimos al buffer
                if len(line) > 3:
                    buffer += " " + line

    # Guardar último versículo
    if buffer and current_verse > 0:
        v_obj = {
            'book': book_code,
            'chapter': current_chapter,
            'verse': current_verse,
            'text': clean_text(buffer)
        }
        if pending_comment:
            v_obj['comment'] = "<br>".join(pending_comment)
        verses.append(v_obj)
    
    print(f"✓ {book_code}: {len(verses)} versículos extraídos.")
    return verses

# Procesar los 4 evangelios
all_verses = []
for book in ['MAT', 'MRK', 'LUK', 'JHN']:
    filename = f'scripts/raw_{book}.txt'
    book_verses = parse_book(book, filename)
    all_verses.extend(book_verses)

# Guardar resultado
with open('scripts/gospels_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\nTotal versículos extraídos: {len(all_verses)}")

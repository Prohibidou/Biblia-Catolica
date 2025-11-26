import PyPDF2
import re
import json

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_FILE = "scripts/biblia_completa_con_comentarios.json"

print("="*70)
print("PARSER DEFINITIVO - Con sección de comentarios al final")
print("="*70)

print(f"\nExtrayendo texto del PDF...")
with open(PDF_FILE, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    
    all_lines = []
    for page_num in range(total_pages):
        if page_num % 1000 == 0:
            print(f"  Página {page_num}/{total_pages}...")
        
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        if text:
            all_lines.extend(text.split('\n'))

print(f"✓ {len(all_lines):,} líneas extraídas")

# PASO 1: Encontrar dónde empiezan los comentarios
print("\nBuscando sección de comentarios...")
comments_start_idx = -1
for i, line in enumerate(all_lines):
    if "COMENTARIO" in line.upper() and i > 100000:  # Los comentarios están muy al final
        comments_start_idx = i
        print(f"✓ Comentarios empiezan en línea {i:,}")
        break

if comments_start_idx == -1:
    print("⚠️  No se encontró sección de comentarios, buscando 'COMENTARIO' en cualquier parte...")
    for i, line in enumerate(all_lines):
        if "COMENTARIO" in line.upper():
            comments_start_idx = i
            print(f"✓ Primera mención de 'COMENTARIO' en línea {i:,}")
            break

# PASO 2: Extraer comentarios
print("\nExtrayendo comentarios...")
comments_dict = {}  # {(book, chapter, verse): comment_text}

if comments_start_idx != -1:
    i = comments_start_idx
    current_comment = []
    current_ref = None
    
    while i < len(all_lines):
        line = all_lines[i].strip()
        
        # Nueva sección de comentario
        if "COMENTARIO" in line.upper():
            # Guardar comentario anterior
            if current_ref and current_comment:
                comments_dict[current_ref] = ' '.join(current_comment)
            
            # Buscar referencia (ej: "1,1" o "GEN 1:1")
            # La referencia suele estar en la misma línea o la siguiente
            ref_text = line
            if i+1 < len(all_lines):
                ref_text += " " + all_lines[i+1]
            
            # Intentar extraer libro:capítulo:versículo
            # Por ahora, marca como pendiente
            current_comment = []
            current_ref = None  # Se determinará después
        else:
            if line:
                current_comment.append(line)
        
        i += 1
    
    print(f"✓ {len(comments_dict)} comentarios extraídos")

# PASO 3: Extraer versículos
print("\nExtrayendo versículos...")
all_verses = []
current_book = 'GEN'
current_chapter = 1
current_verse = 0
verse_lines = []
pending_titles = []

processing = False
verse_count = 0

# Procesar solo hasta donde empiezan los comentarios
end_idx = comments_start_idx if comments_start_idx != -1 else len(all_lines)

i = 0
while i < end_idx:
    line = all_lines[i].strip()
    
    if i % 50000 == 0 and i > 0:
        print(f"  {i:,} líneas... ({verse_count} versículos)")
    
    # Buscar inicio
    if not processing:
        if line == "1" and i+1 < len(all_lines) and "principio creó" in all_lines[i+1].lower():
            processing = True
            print(f"✓ Inicio en línea {i}")
            current_verse = 1
            verse_lines = [all_lines[i+1]]
            i += 2
            continue
        i += 1
        continue
    
    # Número solo en una línea
    if line.isdigit():
        verse_num = int(line)
        
        # Guardar versículo anterior
        if verse_lines and current_verse > 0:
            text = ' '.join(verse_lines).strip()
            v = {
                'book': current_book,
                'chapter': current_chapter,
                'verse': current_verse,
                'text': text
            }
            # Añadir títulos como comentario inline
            if pending_titles:
                v['comment'] = '<br>'.join(pending_titles)
                pending_titles = []
            
            all_verses.append(v)
            verse_count += 1
        
        # Nuevo versículo/capítulo
        if verse_num == 1 and current_verse > 5:
            current_chapter += 1
        
        current_verse = verse_num
        verse_lines = []
        i += 1
        continue
    
    # Título (mayúsculas, >10 chars)
    if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,;:-]+$', line) and len(line) > 10:
        pending_titles.append(f"<strong>{line}</strong>")
        i += 1
        continue
    
    # Referencia
    if re.match(r'^(Gn|Ex|Lv|Nm|Dt|Mt|Mc|Lc|Jn)', line):
        pending_titles.append(f"<em>{line}</em>")
        i += 1
        continue
    
    # Texto del versículo
    if line and len(line) > 0:
        verse_lines.append(line)
    
    i += 1

# Último versículo
if verse_lines:
    text = ' '.join(verse_lines).strip()
    v = {
        'book': current_book,
        'chapter': current_chapter,
        'verse': current_verse,
        'text': text
    }
    if pending_titles:
        v['comment'] = '<br>'.join(pending_titles)
    all_verses.append(v)
    verse_count += 1

print(f"\n✅ Extracción completada:")
print(f"   Versículos: {verse_count:,}")
print(f"   Comentarios al final: {len(comments_dict):,}")

# Guardar
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"💾 Guardado en: {OUTPUT_FILE}")
print("\nNota: Los comentarios de la sección final necesitan ser asociados")
print("manualmente con sus versículos correspondientes.")

import PyPDF2
import re
import json

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_FILE = "scripts/biblia_navarra_desde_pdf_completa.json"

print("="*70)
print("EXTRACCIÓN COMPLETA DESDE PDF LOCAL")
print("="*70)

print(f"\nAbriendo: {PDF_FILE}")
with open(PDF_FILE, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    print(f"Total páginas: {total_pages:,}")
    
    # Extraer TODO el texto
    print("\nExtrayendo texto de todas las páginas...")
    all_text_lines = []
    
    for page_num in range(total_pages):
        if page_num % 500 == 0:
            print(f"  Página {page_num:,}/{total_pages:,}...")
        
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        if text:
            lines = text.split('\n')
            all_text_lines.extend(lines)

print(f"\n✓ Extracción completada: {len(all_text_lines):,} líneas")

# Ahora aplicar TU lógica simple
print("\nAplicando lógica de parsing...")

current_book = None
current_chapter = 0
current_verse = 0
verse_buffer = ""
pending_comments = []
all_verses = []

verse_count = 0
comment_count = 0

# Empezar cuando veamos "GEN 1:1" o "1 En el principio"
processing = False

for i, line in enumerate(all_text_lines):
    line = line.strip()
    
    if not line:
        continue
    
    if i % 50000 == 0 and i > 0:
        print(f"  Procesadas {i:,} líneas... ({verse_count} versículos)")
    
    # Buscar inicio (Génesis 1:1)
    if not processing:
        if "GEN 1:1" in line or (re.match(r'^1\s+', line) and "principio" in line.lower() and "creó" in line.lower()):
            processing = True
            current_book = 'GEN'
            current_chapter = 1
            current_verse = 1
            verse_buffer = line
            print(f"\n✓ Inicio encontrado: {line[:60]}")
            continue
        else:
            continue
    
    # TU LÓGICA: Si empieza con número → versículo
    verse_match = re.match(r'^(\d+)\s+', line)
    
    if verse_match:
        new_verse_num = int(verse_match.group(1))
        
        # Versículo 1 → nuevo capítulo
        if new_verse_num == 1 and current_verse > 5:
            # Guardar versículo anterior
            if verse_buffer:
                all_verses.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': current_verse,
                    'text': re.sub(r'^\d+\s+', '', verse_buffer).strip(),
                    'comment': '<br>'.join(pending_comments) if pending_comments else ''
                })
                verse_count += 1
                if pending_comments:
                    comment_count += 1
                    pending_comments = []
            
            current_chapter += 1
            current_verse = 1
            verse_buffer = line
        
        # Versículo siguiente
        elif new_verse_num == current_verse + 1:
            # Guardar anterior
            if verse_buffer:
                all_verses.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': current_verse,
                    'text': re.sub(r'^\d+\s+', '', verse_buffer).strip(),
                    'comment': '<br>'.join(pending_comments) if pending_comments else ''
                })
                verse_count += 1
                if pending_comments:
                    comment_count += 1
                    pending_comments = []
            
            current_verse = new_verse_num
            verse_buffer = line
        else:
            # Continuar buffer
            verse_buffer += " " + line
    
    # TU LÓGICA: Sin número → título o comentario
    else:
        # ¿Es título? (mayúsculas)
        if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,;:-]+$', line) and len(line) > 10:
            pending_comments.append(f"<strong>{line}</strong>")
        # ¿Es referencia?
        elif re.match(r'^(Gn|Ex|Lv|Nm|Dt|Mt|Mc|Lc|Jn)', line):
            pending_comments.append(f"<em>{line}</em>")
        # Texto normal → continuar buffer
        elif verse_buffer:
            verse_buffer += " " + line

# Guardar último
if verse_buffer:
    all_verses.append({
        'book': current_book,
        'chapter': current_chapter,
        'verse': current_verse,
        'text': re.sub(r'^\d+\s+', '', verse_buffer).strip(),
        'comment': '<br>'.join(pending_comments) if pending_comments else ''
    })
    verse_count += 1

print(f"\n✅ Completado:")
print(f"   Versículos: {verse_count:,}")
print(f"   Con comentarios: {comment_count:,}")

# Guardar
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"\n💾 Guardado en: {OUTPUT_FILE}")

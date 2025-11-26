import PyPDF2
import re
import json

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_FILE = "scripts/biblia_desde_pdf_final.json"

print("="*70)
print("PARSER FINAL - Formato correcto del PDF")
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

# Parser con formato correcto
all_verses = []
current_book = 'GEN'
current_chapter = 1
current_verse = 0
verse_lines = []
pending_comments = []

processing = False
verse_count = 0

print("\nParsing...")

i = 0
while i < len(all_lines):
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
    
    # Formato: número solo en una línea, texto en la siguiente
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
            if pending_comments:
                v['comment'] = '<br>'.join(pending_comments)
                pending_comments = []
            all_verses.append(v)
            verse_count += 1
        
        # Nuevo versículo
        if verse_num == 1 and current_verse > 5:
            current_chapter += 1
        
        current_verse = verse_num
        verse_lines = []
        i += 1
        continue
    
    # Título (mayúsculas)
    if re.match(r'^[A-ZÁÉÍÓÚÑ\s\.,;:-]+$', line) and len(line) > 10:
        pending_comments.append(f"<strong>{line}</strong>")
        i += 1
        continue
    
    # Referencia
    if re.match(r'^(Gn|Ex|Lv|Nm|Dt|Mt|Mc|Lc|Jn)', line):
        pending_comments.append(f"<em>{line}</em>")
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
    if pending_comments:
        v['comment'] = '<br>'.join(pending_comments)
    all_verses.append(v)
    verse_count += 1

print(f"\n✅ Completado:")
print(f"   Versículos: {verse_count:,}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(all_verses, f, ensure_ascii=False, indent=2)

print(f"💾 Guardado en: {OUTPUT_FILE}")

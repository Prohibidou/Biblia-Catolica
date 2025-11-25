import PyPDF2
import re
import json

# Cargar versículos del AT que ya tenemos
with open('scripts/navarra_at.json', 'r', encoding='utf-8') as f:
    at_verses = json.load(f)

print(f"Cargados {len(at_verses)} versículos del AT")

# Crear índice por book:chapter:verse para búsqueda rápida
verse_index = {}
for v in at_verses:
    key = f"{v['book']}_{v['chapter']}_{v['verse']}"
    verse_index[key] = v

print(f"Procesando PDF para extraer comentarios del AT...")

pdf_path = "BibliaPDF/Sagrada Biblia Navarra.pdf"

comments_found = 0
current_book = None
current_chapter = None

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    
    print(f"Total páginas del PDF: {total_pages}")
    print("Procesando páginas 100-5000 (zona estimada del AT)...")
    
    # Solo procesar zona del AT
    for page_num in range(100, min(5000, total_pages)):
        if page_num % 500 == 0:
            print(f"  Página {page_num}... ({comments_found} comentarios encontrados)")
        
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        if not text:
            continue
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Detectar cambio de libro/capítulo por patrón "GEN 1:1"
            book_pattern = re.match(r'([A-Z]{3})\s+(\d+):(\d+)', line)
            if book_pattern:
                current_book = book_pattern.group(1)
                current_chapter = int(book_pattern.group(2))
            
            # Detectar títulos de sección (líneas en mayúsculas)
            if len(line) > 10 and line.isupper() and not any(char.isdigit() for char in line[:10]):
                # Es un posible título
                title = f"<strong>{line}</strong>"
                
                # Buscar el siguiente versículo en las próximas 10 líneas
                for j in range(i+1, min(i+10, len(lines))):
                    next_line = lines[j].strip()
                    verse_match = re.match(r'([A-Z]{3})\s+(\d+):(\d+)', next_line)
                    
                    if verse_match:
                        book = verse_match.group(1)
                        chapter = int(verse_match.group(2))
                        verse = int(verse_match.group(3))
                        
                        key = f"{book}_{chapter}_{verse}"
                        if key in verse_index:
                            # Añadir comentario
                            existing = verse_index[key].get('comment', '')
                            if existing:
                                verse_index[key]['comment'] = existing + "<br>" + title
                            else:
                                verse_index[key]['comment'] = title
                            comments_found += 1
                        break
            
            # Detectar referencias cruzadas (ej: "Gn 1,1-5" o "Ex 3,14")
            ref_pattern = re.match(r'^([A-Za-z]{2,4})\s+\d+,\d+', line)
            if ref_pattern and len(line) < 50:  # Referencias suelen ser cortas
                reference = f"<em>{line}</em>"
                
                # Asociar al siguiente versículo
                for j in range(i+1, min(i+10, len(lines))):
                    next_line = lines[j].strip()
                    verse_match = re.match(r'([A-Z]{3})\s+(\d+):(\d+)', next_line)
                    
                    if verse_match:
                        book = verse_match.group(1)
                        chapter = int(verse_match.group(2))
                        verse = int(verse_match.group(3))
                        
                        key = f"{book}_{chapter}_{verse}"
                        if key in verse_index:
                            existing = verse_index[key].get('comment', '')
                            if existing:
                                verse_index[key]['comment'] = existing + "<br>" + reference
                            else:
                                verse_index[key]['comment'] = reference
                            comments_found += 1
                        break

print(f"\n✓ Procesamiento completado")
print(f"  Comentarios encontrados y asociados: {comments_found}")

# Reconstruir lista de versículos con comentarios
at_with_comments = list(verse_index.values())

# Guardar
output_file = 'scripts/navarra_at_con_comentarios.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(at_with_comments, f, ensure_ascii=False, indent=2)

print(f"  Guardado en: {output_file}")

# Estadísticas
verses_with_comments = len([v for v in at_with_comments if v.get('comment')])
print(f"\nEstadísticas:")
print(f"  Versículos totales: {len(at_with_comments)}")
print(f"  Versículos con comentarios: {verses_with_comments}")

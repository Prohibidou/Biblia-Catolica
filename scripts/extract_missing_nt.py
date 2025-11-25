import PyPDF2
import re
import json

# Libros que nos faltan (estimación de páginas basada en estructura típica)
# Solo extraeremos 1 Corintios como prueba
TARGET_BOOKS = ['1CO', '2CO', '1TH', '2TH', '1TI', '2TI']

pdf_path = "BibliaPDF/Sagrada Biblia Navarra.pdf"
output_file = "scripts/missing_nt_books.json"

print(f"Abriendo PDF: {pdf_path}")
print(f"Buscando solo libros faltantes del NT...")

verses = []

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)
    
    print(f"Total páginas: {total_pages}")
    print("Buscando en páginas 5000-7000 (zona estimada NT)...")
    
    # Buscar solo en zona del NT
    for page_num in range(5000, 7000):
        if page_num >= total_pages: break
        
        if page_num % 100 == 0:
            print(f"  Página {page_num}...")
        
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        # Buscar patrón: "1CO 1:1 texto..."
        pattern = r'([12]?[A-Z]{2,3})\s+(\d+):(\d+)\s+(.+?)(?=\n|$)'
        
        for match in re.finditer(pattern, text):
            book = match.group(1)
            chapter = int(match.group(2))
            verse = int(match.group(3))
            text_content = match.group(4).strip()
            
            if book in TARGET_BOOKS:
                verses.append({
                    'book': book,
                    'chapter': chapter,
                    'verse': verse,
                    'text': text_content,
                    'comment': ''
                })

print(f"\n✓ Encontrados {len(verses)} versículos de los libros faltantes")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(verses, f, ensure_ascii=False, indent=2)

print(f"Guardado en: {output_file}")

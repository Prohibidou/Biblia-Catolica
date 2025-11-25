import PyPDF2
import re
import json

# Configuración
PDF_PATH = 'BibliaPDF/Sagrada Biblia Navarra.pdf'
START_PAGE = 5500  # Aprox inicio NT (ajustar según búsqueda)
END_PAGE = 9000    # Aprox fin NT

# Mapeo de libros
BOOK_CODES = {
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN',
    'HECHOS': 'ACT', 'ROMANOS': 'ROM',
    '1 CORINTIOS': '1CO', '2 CORINTIOS': '2CO',
    'GÁLATAS': 'GAL', 'EFESIOS': 'EPH', 'FILIPENSES': 'PHP', 'COLOSENSES': 'COL',
    '1 TESALONICENSES': '1TH', '2 TESALONICENSES': '2TH',
    '1 TIMOTEO': '1TI', '2 TIMOTEO': '2TI',
    'TITO': 'TIT', 'FILEMÓN': 'PHM', 'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS',
    '1 PEDRO': '1PE', '2 PEDRO': '2PE',
    '1 JUAN': '1JN', '2 JUAN': '2JN', '3 JUAN': '3JN',
    'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

def clean_text(text):
    """Limpia el texto de caracteres extraños."""
    return text.replace('\r', ' ').replace('\n', ' ').strip()

def extract_nt_from_pdf():
    print(f"Abriendo PDF: {PDF_PATH}")
    pdf = open(PDF_PATH, 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print(f"Total páginas en PDF: {len(reader.pages)}")
    print(f"Extrayendo del NT (páginas {START_PAGE} a {END_PAGE})...")
    
    # Extraer texto completo del rango de páginas
    full_text = ""
    for page_num in range(START_PAGE - 1, min(END_PAGE, len(reader.pages))):
        if page_num % 100 == 0:
            print(f"  Página {page_num + 1}...")
        
        page = reader.pages[page_num]
        text = page.extract_text()
        full_text += text + "\n"
    
    pdf.close()
    
    print(f"✓ Texto extraído: {len(full_text)} caracteres")
    
    # Guardar texto completo para análisis
    with open('scripts/nt_pdf_full_extract.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print("✓ Guardado en scripts/nt_pdf_full_extract.txt")
    
    # Ahora parsear el texto
    return parse_nt_text(full_text)

def parse_nt_text(text):
    """Parsea el texto del NT extraído."""
    lines = text.split('\n')
    
    verses = []
    current_book = None
    current_chapter = 0
    current_section_title = None
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if not line:
            i += 1
            continue
        
       # TODO: Implementar lógica de parseo similar a parse_nt_complete.py
        # pero adaptada al formato específico del PDF
        
        i += 1
    
    return verses

if __name__ == '__main__':
    verses = extract_nt_from_pdf()
    print(f"\n✓ Total: {len(verses)} versículos extraídos")

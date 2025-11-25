import PyPDF2
import re
import json
import sys

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    print(f"Abriendo PDF: {pdf_path}")
    text = ""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"Total de páginas: {total_pages}")
        
        for page_num in range(total_pages):
            if page_num % 50 == 0:
                print(f"Procesando página {page_num + 1}/{total_pages}...")
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    return text

def detect_bible_structure(text):
    """
    Analiza el texto para detectar la estructura de la Biblia.
    Devuelve información sobre el formato detectado.
    """
    # Guardar una muestra más grande para análisis
    sample_size = 20000
    with open('scripts/pdf_full_sample.txt', 'w', encoding='utf-8') as f:
        f.write(text[:sample_size])
    
    print("\n" + "="*70)
    print("ANÁLISIS DE ESTRUCTURA")
    print("="*70)
    
    # Buscar patrones comunes de versículos
    patterns = {
        'numero_solo': re.compile(r'^\s*(\d+)\s+([A-Z][^.?!]+[.?!])', re.MULTILINE),
        'numero_punto': re.compile(r'^\s*(\d+)\.\s+([A-Z][^.?!]+[.?!])', re.MULTILINE),
        'superindice': re.compile(r'(\d+)\s*([A-ZÁ-Ú][^\d]+?)(?=\s*\d+\s*[A-ZÁ-Ú]|\n|$)', re.MULTILINE),
        'capitulo_versiculo': re.compile(r'(\d+):(\d+)\s+([^0-9]+?)(?=\d+:\d+|\n|$)', re.MULTILINE),
    }
    
    # Buscar encabezados de libros
    book_patterns = {
        'genesis': re.compile(r'(GÉNESIS|Génesis|GENESIS|Genesis)', re.IGNORECASE),
        'exodo': re.compile(r'(ÉXODO|Éxodo|EXODO|Exodo)', re.IGNORECASE),
        'levitico': re.compile(r'(LEVÍTICO|Levítico|LEVITICO|Levitico)', re.IGNORECASE),
    }
    
    print("\n1. Buscando encabezados de libros...")
    for book_name, pattern in book_patterns.items():
        matches = pattern.findall(text[:50000])
        if matches:
            print(f"   ✓ Encontrado: {book_name} ({len(matches)} veces)")
    
    print("\n2. Analizando patrones de versículos...")
    for pattern_name, pattern in patterns.items():
        matches = pattern.findall(text[:50000])
        if matches:
            print(f"   ✓ Patrón '{pattern_name}': {len(matches)} coincidencias")
            if matches:
                print(f"     Ejemplo: {matches[0]}")
    
    # Buscar patrones de capítulos
    chapter_patterns = {
        'capitulo_numero': re.compile(r'CAPÍTULO\s+(\d+)', re.IGNORECASE),
        'solo_numero_grande': re.compile(r'\n\s*(\d+)\s*\n', re.MULTILINE),
    }
    
    print("\n3. Analizando patrones de capítulos...")
    for pattern_name, pattern in chapter_patterns.items():
        matches = pattern.findall(text[:50000])
        if matches:
            print(f"   ✓ Patrón '{pattern_name}': {len(matches)} coincidencias")
            if matches:
                print(f"     Ejemplos: {matches[:5]}")
    
    print("\n" + "="*70)
    print("Muestra guardada en scripts/pdf_full_sample.txt")
    print("Por favor, revisa este archivo para entender el formato exacto.")
    print("="*70)
    
    return text

def parse_bible_generic(text, output_file='bible_parsed.json'):
    """
    Parser genérico que intenta extraer versículos usando múltiples estrategias.
    Este es un punto de partida que debe ajustarse según el formato específico.
    """
    verses = []
    
    # Mapa de libros bíblicos a códigos
    book_codes = {
        'génesis': 'GEN',
        'genesis': 'GEN',
        'éxodo': 'EXO',
        'exodo': 'EXO',
        'levítico': 'LEV',
        'levitico': 'LEV',
        'números': 'NUM',
        'numeros': 'NUM',
        'deuteronomio': 'DEU',
        'josué': 'JOS',
        'josue': 'JOS',
        'jueces': 'JDG',
        'rut': 'RUT',
        '1 samuel': '1SA',
        '2 samuel': '2SA',
        '1 reyes': '1KI',
        '2 reyes': '2KI',
        # Añadir más según sea necesario
    }
    
    # Este es un parser de ejemplo que debe ajustarse
    # según la estructura real del PDF
    current_book = None
    current_chapter = 1
    
    # Dividir en líneas para procesar
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        # Buscar nombre de libro
        for book_name, book_code in book_codes.items():
            if book_name in line.lower():
                current_book = book_code
                print(f"Encontrado libro: {book_name} -> {book_code}")
                break
        
        # Intentar extraer versículos (patrón simple)
        # Formato: "1 Texto del versículo..."
        verse_match = re.match(r'^(\d+)\s+(.+)$', line.strip())
        if verse_match and current_book:
            verse_num = int(verse_match.group(1))
            verse_text = verse_match.group(2).strip()
            
            if verse_text and len(verse_text) > 10:  # Evitar líneas demasiado cortas
                verses.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': verse_num,
                    'text': verse_text
                })
    
    print(f"\nTotal de versículos extraídos: {len(verses)}")
    
    if verses:
        with open(f'scripts/{output_file}', 'w', encoding='utf-8') as f:
            json.dump(verses, f, ensure_ascii=False, indent=2)
        print(f"Versículos guardados en scripts/{output_file}")
    else:
        print("⚠️  No se pudieron extraer versículos con el parser genérico.")
        print("   Es necesario ajustar el script según el formato específico del PDF.")
    
    return verses

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python parse_bible_pdf.py <ruta_al_pdf> [--parse]")
        print("\nOpciones:")
        print("  Sin --parse: Solo analiza la estructura del PDF")
        print("  Con --parse: Intenta extraer y parsear los versículos")
        print("\nEjemplo:")
        print('  python parse_bible_pdf.py "BibliaPDF/AT Navarra.pdf"')
        print('  python parse_bible_pdf.py "BibliaPDF/AT Navarra.pdf" --parse')
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    should_parse = '--parse' in sys.argv
    
    # Extraer texto
    text = extract_text_from_pdf(pdf_path)
    
    # Analizar estructura
    detect_bible_structure(text)
    
    # Si se solicita, intentar parsear
    if should_parse:
        print("\n" + "="*70)
        print("INTENTANDO PARSEAR VERSÍCULOS...")
        print("="*70)
        verses = parse_bible_generic(text)
        
        if verses:
            print("\n✓ Parseo completado. Revisa el archivo JSON generado.")
        else:
            print("\n⚠️  No se pudieron parsear versículos automáticamente.")
            print("   Revisa pdf_full_sample.txt y ajusta el parser según el formato.")
    else:
        print("\n💡 Tip: Ejecuta con --parse para intentar extraer los versículos")
        print("   después de revisar la estructura en pdf_full_sample.txt")

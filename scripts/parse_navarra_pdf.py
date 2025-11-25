import PyPDF2
import re
import json
import sys

# Mapa de códigos de libros bíblicos
BOOK_CODES = {
    'GEN': 'GEN', 'EXO': 'EXO', 'LEV': 'LEV', 'NUM': 'NUM', 'DEU': 'DEU',
    'JOS': 'JOS', 'JDG': 'JDG', 'RUT': 'RUT', '1SA': '1SA', '2SA': '2SA',
    '1KI': '1KI', '2KI': '2KI', '1CH': '1CH', '2CH': '2CH', 'EZR': 'EZR',
    'NEH': 'NEH', 'TOB': 'TOB', 'JDT': 'JDT', 'EST': 'EST', '1MA': '1MA',
    '2MA': '2MA', 'JOB': 'JOB', 'PSA': 'PSA', 'PRO': 'PRO', 'ECC': 'ECC',
    'SNG': 'SNG', 'WIS': 'WIS', 'SIR': 'SIR', 'ISA': 'ISA', 'JER': 'JER',
    'LAM': 'LAM', 'BAR': 'BAR', 'EZK': 'EZK', 'DAN': 'DAN', 'HOS': 'HOS',
    'JOL': 'JOL', 'AMO': 'AMO', 'OBA': 'OBA', 'JON': 'JON', 'MIC': 'MIC',
    'NAM': 'NAM', 'HAB': 'HAB', 'ZEP': 'ZEP', 'HAG': 'HAG', 'ZEC': 'ZEC',
    'MAL': 'MAL', 'MAT': 'MAT', 'MRK': 'MRK', 'LUK': 'LUK', 'JHN': 'JHN',
    'ACT': 'ACT', 'ROM': 'ROM', '1CO': '1CO', '2CO': '2CO', 'GAL': 'GAL',
    'EPH': 'EPH', 'PHP': 'PHP', 'COL': 'COL', '1TH': '1TH', '2TH': '2TH',
    '1TI': '1TI', '2TI': '2TI', 'TIT': 'TIT', 'PHM': 'PHM', 'HEB': 'HEB',
    'JAS': 'JAS', '1PE': '1PE', '2PE': '2PE', '1JN': '1JN', '2JN': '2JN',
    '3JN': '3JN', 'JUD': 'JUD', 'REV': 'REV'
}

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    print(f"Abriendo PDF: {pdf_path}")
    text = ""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"Total de páginas: {total_pages}")
        
        for page_num in range(total_pages):
            if page_num % 100 == 0:
                print(f"Procesando página {page_num + 1}/{total_pages}...")
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
    
    print("✓ Extracción completada")
    return text

def parse_navarra_bible(text, output_file='navarra_full.json'):
    """
    Parser específico para la Biblia de Navarra.
    Formato: GEN 1:1 Texto del versículo...
    """
    print("\nParseando versículos...")
    verses = []
    
    # Patrón para detectar versículos: CODIGO CAPITULO:VERSICULO Texto
    # Ejemplo: GEN 1:1 En el principio...
    # Soporta códigos de 2-3 caracteres: GEN, 1SA, 2KI, etc.
    verse_pattern = re.compile(
        r'(\d?[A-Z]{2,3})\s+(\d+):(\d+)\s+(.+?)(?=\s+\d?[A-Z]{2,3}\s+\d+:\d+|\Z)',
        re.DOTALL
    )
    
    matches = verse_pattern.findall(text)
    
    print(f"Encontrados {len(matches)} versículos")
    
    for match in matches:
        book_code, chapter, verse, text_content = match
        
        # Limpiar el texto
        text_content = text_content.strip()
        
        # Eliminar saltos de línea extra
        text_content = re.sub(r'\s+', ' ', text_content)
        
        # Eliminar caracteres extraños al final
        text_content = re.sub(r'\s+$', '', text_content)
        
        # Verificar que el código del libro sea válido
        if book_code in BOOK_CODES and len(text_content) > 5:
            verses.append({
                'book': book_code,
                'chapter': int(chapter),
                'verse': int(verse),
                'text': text_content
            })
    
    # Mostrar estadísticas
    books_found = set(v['book'] for v in verses)
    print(f"\n📚 Resumen:")
    print(f"   - Total de versículos: {len(verses)}")
    print(f"   - Libros encontrados: {len(books_found)}")
    print(f"   - Códigos de libros: {', '.join(sorted(books_found))}")
    
    # Guardar JSON
    output_path = f'scripts/{output_file}'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Versículos guardados en {output_path}")
    
    # Mostrar algunos ejemplos
    if verses:
        print(f"\n📖 Primeros 3 versículos:")
        for v in verses[:3]:
            print(f"   {v['book']} {v['chapter']}:{v['verse']} - {v['text'][:80]}...")
    
    return verses

def main():
    if len(sys.argv) < 2:
        print("Uso: python parse_navarra_pdf.py <ruta_al_pdf> [nombre_output]")
        print("\nEjemplo:")
        print('  python parse_navarra_pdf.py "BibliaPDF/AT Navarra.pdf" navarra_at')
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else 'navarra_full'
    output_file = f'{output_name}.json'
    
    # Extraer texto
    text = extract_text_from_pdf(pdf_path)
    
    # Parsear
    verses = parse_navarra_bible(text, output_file)
    
    if verses:
        print(f"\n✅ PROCESO COMPLETADO EXITOSAMENTE")
        print(f"\n📝 Siguiente paso:")
        print(f'   python scripts/convert_to_sqlite.py scripts/{output_file} {output_name}')
    else:
        print(f"\n❌ No se pudieron extraer versículos")
        sys.exit(1)

if __name__ == "__main__":
    main()

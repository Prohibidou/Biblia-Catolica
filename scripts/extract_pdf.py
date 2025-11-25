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

def parse_bible_text(text):
    """
    Parse the extracted text into structured verses.
    This is a basic parser - you may need to adjust based on the PDF structure.
    """
    verses = []
    
    # This regex pattern needs to be adjusted based on actual PDF format
    # Common patterns:
    # "1. En el principio..." (verse number followed by text)
    # "Génesis 1" (book and chapter headers)
    
    # Try to detect verse patterns
    # Example: "1 En el principio creó Dios..."
    verse_pattern = re.compile(r'^(\d+)\s+(.+)$', re.MULTILINE)
    
    # Save first 5000 characters to a sample file for inspection
    with open('scripts/pdf_sample.txt', 'w', encoding='utf-8') as f:
        f.write(text[:5000])
    
    print("\nPrimeras 500 caracteres del PDF:")
    print(text[:500])
    print("\n" + "="*50)
    print("Sample guardado en scripts/pdf_sample.txt para inspección")
    
    return verses

if __name__ == "__main__":
    pdf_path = r"C:\Users\veram\OneDrive\Documentos\projects\BibliaCatolica3\BibliaPDF\AT Navarra.pdf"
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    # Parse (first pass - just to see structure)
    verses = parse_bible_text(text)
    
    print(f"\nExtracción completada. Ver scripts/pdf_sample.txt para analizar el formato.")

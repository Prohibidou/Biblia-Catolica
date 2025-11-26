import PyPDF2

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"

print("Analizando primeras 50 páginas del PDF para ver el formato real...")

with open(PDF_FILE, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    
    # Buscar "En el principio" en las primeras 200 páginas
    for page_num in range(min(200, len(pdf_reader.pages))):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        
        if "en el principio" in text.lower() or "principio creó" in text.lower():
            print(f"\n✓ Encontrado en página {page_num}")
            print("="*60)
            print(text[:1000])  # Primeros 1000 caracteres
            print("="*60)
            break
    else:
        print("\n❌ No encontrado en las primeras 200 páginas")
        print("\nMostrando página 100 como ejemplo:")
        page = pdf_reader.pages[100]
        text = page.extract_text()
        print("="*60)
        print(text[:800])
        print("="*60)

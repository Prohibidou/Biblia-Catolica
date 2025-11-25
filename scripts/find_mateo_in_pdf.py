import PyPDF2

pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

print("Buscando inicio de Mateo en el PDF...\n")

# Buscar entre páginas 4600-4800
for page_num in range(4600, 4800):
    page = reader.pages[page_num]
    text = page.extract_text()
    
    # Buscar "EVANGELIO SEGÚN SAN MATEO" o "Mt 1" o "Mateo 1"
    if any(term in text.upper() for term in ['EVANGELIO SEGÚN SAN MATEO', 'EVANGELIO DE MATEO', 'MATEO 1']):
        print(f"✓ ENCONTRADO en página {page_num + 1}")
        print(f"\n--- CONTENIDO ---")
        print(text[:2000])
        break
    
    if page_num % 20 == 0:
        print(f"  Revisando página {page_num + 1}...")

pdf.close()

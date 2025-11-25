import PyPDF2

pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

# Extraer páginas del inicio de Mateo (aprox pág 4500-4502)
print("=== MUESTRA DE MATEO (Páginas 4500-4502) ===\n")

for page_num in range(4500, 4503):
    page = reader.pages[page_num]
    text = page.extract_text()
    print(f"\n--- PÁGINA {page_num + 1} ---")
    print(text[:1500])  # Primeros 1500 caracteres
    print("...")

pdf.close()

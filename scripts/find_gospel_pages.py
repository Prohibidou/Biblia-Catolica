import PyPDF2

pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

print("Buscando páginas con texto de evangelios...\n")

# Buscar páginas que contengan el patrón típico: número de versículo + texto largo
# y la estructura de capítulos

found_pages = []

for page_num in range(0, len(reader.pages), 100):  # Cada 100 páginas
    page = reader.pages[page_num]
    text = page.extract_text()
    
    # Buscar si tiene el patrón de Lucas o Mateo con versículos numerados
    # Patrón: Lc\n51\nTexto... (como vimos en nt_inicio_muestra.txt)
    if '\nLc\n' in text or '\nMt\n' in text or '\nMc\n' in text or '\nJn\n' in text:
        # Verificar que tiene números de versículos
        lines = text.split('\n')
        verse_numbers = sum(1 for line in lines if line.strip().isdigit() and len(line.strip()) <= 2)
        
        if verse_numbers >= 5:  # Al menos 5 números de versículos
            found_pages.append(page_num + 1)
            print(f"✓ Página {page_num + 1}: {verse_numbers} números de versículos")
            
            if len(found_pages) >= 10:  # Mostrar primeras 10
                break

pdf.close()

if found_pages:
    print(f"\n📖 Páginas con contenido de evangelios: {found_pages[0]} - {found_pages[-1]}")
    print(f"   Rango sugerido para extracción completa: {found_pages[0]} - {found_pages[-1] + 3000}")
else:
    print("\n⚠️ No se encontraron páginas con el patrón de evangelios.")
    print("   El texto de los evangelios puede estar en un formato diferente en el PDF.")

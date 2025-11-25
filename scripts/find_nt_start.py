import PyPDF2
import re

# Abrir PDF
pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
print("Abriendo PDF...")
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total de páginas: {len(pdf.pages)}")

# Buscar el inicio del Nuevo Testamento
print("\nBuscando inicio del Nuevo Testamento...")

# El NT probablemente está después de la página 2000
for i in range(2000, min(len(pdf.pages), 4000), 50):
    text = pdf.pages[i].extract_text()
    
    # Buscar "Mateo" o "EVANGELIO SEGÚN SAN MATEO"
    if ('MATEO' in text.upper() or 'EVANGELIO' in text.upper() and 'MATEO' in text.upper() or
        'Mt 1' in text or 'MAT 1:1' in text or 'MT 1:1' in text):
        print(f"\n¡Posible inicio del NT encontrado en página {i+1}!")
        
        # Extraer muestra de esta zona
        sample_text = ''
        for j in range(i-2, min(i+10, len(pdf.pages))):
            sample_text += pdf.pages[j].extract_text() + '\n\n' + '='*70 + f' PÁGINA {j+1} ' + '='*70 + '\n\n'
        
        with open('scripts/nt_inicio_muestra.txt', 'w', encoding='utf-8') as f:
            f.write(sample_text[:15000])
        
        print(f"Muestra guardada en scripts/nt_inicio_muestra.txt")
        print(f"\nPrimeros 1000 caracteres de la página {i+1}:")
        print(text[:1000])
        print(f"\nRevisando estructura alrededor de la página {i+1}...")
        break

# También verificar páginas específicas que probablemente contengan Mateo
test_pages = [2500, 3000, 3500, 4000, 4500]
print("\n\nVerificando páginas específicas...")
for page_num in test_pages:
    if page_num < len(pdf.pages):
        text = pdf.pages[page_num].extract_text()
        if 'Mt' in text[:200] or 'MAT' in text[:200] or 'MATEO' in text[:200].upper():
            print(f"\n¡Encontrado en página {page_num+1}!")
            print(text[:500])

print("\n\nProceso completado.")

import PyPDF2
import re

pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

print("Buscando patrón 'Mt 1' en el PDF...\n")

# El NT debería estar después del AT (aprox después página 5000)
for page_num in range(5000, 6000):
    page = reader.pages[page_num]
    text = page.extract_text()
    
    # Buscar "Mt 1" al inicio de línea
    if re.search(r'Mt\s+1[,:]', text):
        print(f"✓ ENCONTRADO 'Mt 1' en página {page_num + 1}")
        print(f"\n--- MUESTRA DE CONTENIDO ---")
        print(text[:3000])
        break
    
    if page_num % 50 == 0:
        print(f"  Revisando página {page_num + 1}...")

pdf.close()

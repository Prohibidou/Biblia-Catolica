import PyPDF2
import re

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

# Revisar página 5 (índice)
print("ÍNDICE - Página 5:")
print("="*70)
text_p5 = pdf.pages[4].extract_text()  # página 5 = índice 4
print(text_p5)

print("\n\nPágina 28:")
print("="*70)
text_p28 = pdf.pages[27].extract_text()
print(text_p28)

# Buscar números de página asociados con NT
numbers = re.findall(r'(\d{3,4})', text_p5)
print(f"\n\nNúmeros encontrados en índice: {numbers[:20]}")

# Probar algunas páginas específicas
test_pages = [100, 200, 500, 1000, 1500, 2000, 2500, 2600]
print("\n\nBuscando 'Mt 1:1' en páginas específicas:")
for page_num in test_pages:
    text = pdf.pages[page_num].extract_text()
    if 'Mt 1:1' in text or 'MAT 1:1' in text or ('Genealog' in text and 'Jesús' in text):
        print(f"  ¡Encontrado en página {page_num+1}!")
        print(text[:500])
        break
    else:
        # Buscar solo el inicio
        if 'Mt' in text[:100]:
            print(f"  'Mt' en página {page_num+1}: {text[:200]}")

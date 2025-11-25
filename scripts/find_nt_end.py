import PyPDF2
import re

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print("Buscando final del Nuevo Testamento (Apocalipsis)...\n")

# Apocalipsis es el último libro del NT
# Buscar "Apocalipsis" o "Ap 22" (último capítulo)

for i in range(2700, 3100, 10):
    text = pdf.pages[i].extract_text()
    
    if 'APOCALIPSIS' in text.upper() or 'APOCALIPSI' in text.upper():
        print(f"Página {i+1}: Texto relacionado con Apocalipsis")
    
    # Buscar el final (Apocalipsis 22:21 es el último versículo de la Biblia)
    if 'Amén' in text and 'gracia' in text.lower() and i > 2950:
        print(f"\n*** Posible final del NT en página {i+1} ***")
        print(text[:1000])
        print("\n" + "="*70)

# Probar páginas específicas
test_pages = [3000, 3050, 3100, 3150]
print("\nVerificando páginas específicas...")
for p in test_pages:
    if p < len(pdf.pages):
        text = pdf.pages[p].extract_text()[:300]
        print(f"\nPágina {p+1}:")
        print(text)

print(f"\nNT aproximadamente: páginas 2530 - 3100 (570 páginas)")

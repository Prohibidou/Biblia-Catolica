import PyPDF2
import re

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total páginas: {len(pdf.pages)}\n")

# Sabemos que Lucas está en página 2700
# Mateo debe estar antes
# Buscar patrón "Mt 1:1" o "MAT 1:1"

print("Buscando patrón de versículos en rango 2400-2700...")
for i in range(2400, 2700, 5):
    text = pdf.pages[i].extract_text()
    
    # Buscar patrón Mt X:Y
    if re.search(r'\bMt\s+\d+:\d+', text) or re.search(r'\bMAT\s+\d+:\d+', text):
        print(f"\n¡Patrón 'Mt X:Y' encontrado en página {i+1}!")
        print(text[:1000])
        
        # Guardar muestra extensa
        sample = ''
        for j in range(max(0, i-2), min(i+25, len(pdf.pages))):
            sample += f'\n\n{"="*70} PÁGINA {j+1} {"="*70}\n\n'
            sample += pdf.pages[j].extract_text()
        
        with open('scripts/mateo_encontrado.txt', 'w', encoding='utf-8') as f:
            f.write(sample)
        
        print(f"\nMuestra completa guardada en scripts/mateo_encontrado.txt")
        break

print("\nProceso completado.")

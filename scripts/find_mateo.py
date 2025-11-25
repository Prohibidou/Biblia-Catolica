import PyPDF2
import re

# Abrir PDF
pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
print("Abriendo Biblia completa de Navarra...")
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total de páginas: {len(pdf.pages)}")

# Buscar el evangelio de Mateo (debe estar antes de Lucas)
print("\nBuscando Evangelio de Mateo...")

for i in range(2400, 2700, 10):
    text = pdf.pages[i].extract_text()
    
    # Buscar "MATEO" o  "Mt 1:1"
    if ('EVANGELIO SEGÚN SAN MATEO' in text.upper() or 
        'Mt 1' in text[:200] or 
        'MATEO' in text[:300].upper() and '1:1' in text[:500]):
        print(f"\n¡Evangelio de Mateo encontrado en página {i+1}!")
        
        # Extraer muestra amplia
        sample_text = ''
        for j in range(i, min(i+20, len(pdf.pages))):
            sample_text += f'\n\n{"="*70} PÁGINA {j+1} {"="*70}\n\n'
            sample_text += pdf.pages[j].extract_text()
        
        with open('scripts/mateo_inicio_completo.txt', 'w', encoding='utf-8') as f:
            f.write(sample_text)
        
        print(f"Muestra guardada en scripts/mateo_inicio_completo.txt")
        print(f"\nPrimeros 2000 caracteres:")
        print(pdf.pages[i].extract_text()[:2000])
        break

print("\n\nVerificando estructura de comentarios...")

# Buscar páginas con comentarios (usualmente tienen notas al pie o secciones especiales)
for i in range(2450, 2470):
    text = pdf.pages[i].extract_text()
    
    # Buscar patrones de comentarios
    if ('1.' in text and '2.' in text and '3.' in text) or '#' in text or '●' in text:
        print(f"\nPosibles comentarios en página {i+1}")
        print(text[:800])
        print("\n" + "-"*70 + "\n")

print("\nProceso completado.")

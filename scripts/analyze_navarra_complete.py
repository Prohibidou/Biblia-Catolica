import PyPDF2
import re

# Abrir PDF
pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total de páginas: {len(pdf.pages)}")

# Extraer muestra de diferentes secciones
print("\n" + "="*70)
print("ANALIZANDO ESTRUCTURA DE LA BIBLIA DE NAVARRA")
print("="*70)

# Páginas iniciales (probablemente introducción)
print("\n1. PÁGINAS INICIALES (1-10):")
text_inicio = ''
for i in range(10):
    text_inicio += pdf.pages[i].extract_text()

print(text_inicio[:1000])

# Páginas del medio (probablemente parte del AT)
print("\n2. PÁGINAS DEL MEDIO (500-510):")
text_medio = ''
for i in range(500, 510):
    text_medio += pdf.pages[i].extract_text()

print(text_medio[:1000])

# Buscar dónde empieza el Nuevo Testamento
print("\n3. BUSCANDO INICIO DEL NUEVO TESTAMENTO...")
for i in range(len(pdf.pages)):
    text = pdf.pages[i].extract_text()
    if 'NUEVO TESTAMENTO' in text or 'Nuevo Testamento' in text or 'MATEO' in text and i > 1000:
        print(f"   Posible inicio del NT en página {i+1}")
        print(f"   Muestra:")
        print(text[:500])
        print("\n")
        if i > 1000:  # Solo mostrar si está en la segunda mitad
            break

# Páginas finales (probablemente NT o Apocalipsis)
print("\n4. PÁGINAS FINALES (últimas 20):")
text_final = ''
start = len(pdf.pages) - 20
for i in range(start, len(pdf.pages)):
    text_final += pdf.pages[i].extract_text()

print(text_final[:1000])

# Guardar muestras más grandes para análisis
with open('scripts/biblia_navarra_inicio.txt', 'w', encoding='utf-8') as f:
    f.write(text_inicio[:10000])

with open('scripts/biblia_navarra_medio.txt', 'w', encoding='utf-8') as f:
    f.write(text_medio[:10000])

with open('scripts/biblia_navarra_final.txt', 'w', encoding='utf-8') as f:
    f.write(text_final[:10000])

print("\n" + "="*70)
print("Muestras guardadas en scripts/biblia_navarra_*.txt")
print("="*70)

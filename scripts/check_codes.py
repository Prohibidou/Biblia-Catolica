import PyPDF2
import re

# Abrir PDF
pdf = PyPDF2.PdfReader(open('BibliaPDF/AT Navarra.pdf', 'rb'))

# Buscar en páginas 400-600 (donde deberían estar los libros históricos)
text = ''
for i in range(400, 600):
    text += pdf.pages[i].extract_text()

# Buscar todos los códigos de libros usados
codes = re.findall(r'\b([A-Z0-9]{2,4})\s+\d+:\d+', text)
unique_codes = sorted(set(codes))

print("Códigos encontrados en páginas 400-600:")
print(unique_codes)

# Buscar específicamente menciones de "Reyes", "Samuel", "Crónicas"
print("\n\nBuscando menciones de libros históricos:")
print("'1 RE' en texto:", '1 RE' in text or '1RE' in text)
print("'2 RE' en texto:", '2 RE' in text or '2RE' in text)
print("'1 SAM' en texto:", '1 SAM' in text or '1SAM' in text)
print("'2 SAM' en texto:", '2 SAM' in text or '2SAM' in text)
print("'1 CR' en texto:", '1 CR' in text or '1CR' in text)
print("'2 CR' en texto:", '2 CR' in text or '2CR' in text)

# Mostrar muestra del texto
print("\n\nPrimeros 2000 caracteres:")
print(text[:2000])

import PyPDF2

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print("Extractando páginas 2528-2540 (inicio de Mateo)...\n")

output = ''
for p in range(2527, 2541):  # páginas 2528-2541
    output += f'\n\n{"="*70} PÁGINA {p+1} {"="*70}\n\n'
    output += pdf.pages[p].extract_text()

with open('scripts/mateo_cap1_cap2.txt', 'w', encoding='utf-8') as f:
    f.write(output)

print("Guardado en scripts/mateo_cap1_cap2.txt")

# Mostrar primeras 3 páginas
for p in [2527, 2528, 2529]:
    print(f'\n{"="*70} PÁGINA {p+1} {"="*70}\n')
    print(pdf.pages[p].extract_text()[:1500])

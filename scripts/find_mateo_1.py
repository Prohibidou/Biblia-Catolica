import PyPDF2

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print("Buscando genealogía de Jesús (Mateo 1)...")

for i in range(2450, 2550):
    text = pdf.pages[i].extract_text().lower()
    
    # Mateo 1 tiene: "Libro de la genealogía de Jesucristo, hijo de David, hijo de Abraham"
    if ('genealog' in text and 'abraham' in text and 'david' in text):
        print(f"\n¡ENCONTRADO en página {i+1}!")
        
        # Extraer muestra amplia
        sample = ''
        for j in range(max(0, i-1), min(i+30, len(pdf.pages))):
            sample += f'\n\n{"="*70} PÁGINA {j+1} {"="*70}\n\n'
            sample += pdf.pages[j].extract_text()
        
        with open('scripts/mateo_cap1_completo.txt', 'w', encoding='utf-8') as f:
            f.write(sample)
        
        print(f"Muestra guardada en scripts/mateo_cap1_completo.txt")
        print(f"\nPrimeros 1500 caracteres de página {i+1}:")
        print(pdf.pages[i].extract_text()[:1500])
        break

print("\nProceso terminado.")

import PyPDF2

# Abrir PDF
pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
print("Abriendo Biblia completa de Navarra...")
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total de páginas: {len(pdf.pages)}\n")

# Buscar en las primeras 100 páginas (probablemente índice)
print("Buscando índice en primeras 100 páginas...")
for i in range(100):
    text = pdf.pages[i].extract_text()
    if 'MATEO' in text.upper() or 'Mt' in text[:500]:
        print(f"Página {i+1}: 'MATEO' o 'Mt' encontrado")
        if 'pág' in text.lower() or 'página' in text.lower():
            print(text[:1000])
            print("\n" + "="*70 + "\n")

# Buscar en rangos amplios
print("\nBuscando Mateo en todo el documento (cada 100 páginas)...")
for i in range(0, len(pdf.pages), 100):
    text = pdf.pages[i].extract_text()
    if 'Mt 1:1' in text or ('MATEO' in text.upper() and ('Genealog' in text or 'José' in text)):
        print(f"\n¡Posible Mateo en página {i+1}!")
        print(text[:1500])
        
        # Guardar muestra
        sample = ''
        for j in range(max(0, i-2), min(i+15, len(pdf.pages))):
            sample += f'\n\n{"="*70} PÁGINA {j+1} {"="*70}\n\n'
            sample += pdf.pages[j].extract_text()
        
        with open(f'scripts/mateo_pag_{i+1}.txt', 'w', encoding='utf-8') as f:
            f.write(sample)
        
        print(f"\nMuestra guardada en scripts/mateo_pag_{i+1}.txt")
        break

print("\nProceso completado.")

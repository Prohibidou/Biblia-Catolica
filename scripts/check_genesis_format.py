import PyPDF2

pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
reader = PyPDF2.PdfReader(pdf)

# Buscar las primeras páginas con Génesis
for i in range(10, 20):
    text = reader.pages[i].extract_text()
    lines = text.split('\n')
    
    print(f"\n{'='*70}")
    print(f"PÁGINA {i+1}")
    print('='*70)
    
    # Mostrar las primeras 30 líneas
    for j, line in enumerate(lines[:30]):
        print(f"{j:3d}: {line}")
    
    # Buscar "principio" y "creó"
    if 'principio' in text.lower() and 'creó' in text.lower():
        print(f"\n✓ ENCONTRADO en página {i+1}")
        print(f"\nLíneas con 'principio':")
        for j, line in enumerate(lines):
            if 'principio' in line.lower():
                print(f"  {j}: {line}")
        break

pdf.close()

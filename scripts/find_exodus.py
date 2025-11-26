import PyPDF2

def find_transition():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando transición Gn -> Ex...")
    
    # Genesis tiene 50 capítulos. Debería estar por la página 100-150
    for i in range(100, 160):
        text = reader.pages[i].extract_text()
        lines = text.split('\n')
        
        # Buscar "ÉXODO" o cambio de header
        header = lines[1] if len(lines) > 1 else ""
        
        print(f"Página {i}: Header='{header}'")
        
        if 'ÉXODO' in text or 'EXODO' in text:
            print(f"\n!!! ENCONTRADO ÉXODO EN PÁGINA {i} !!!")
            print("-" * 40)
            print(text[:500])
            print("-" * 40)
            
    pdf.close()

find_transition()

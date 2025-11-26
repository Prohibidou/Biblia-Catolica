import PyPDF2

def find_mal_mat_transition():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando transición Mal -> Mt...")
    
    # Scan headers
    for i in range(2500, 3500):
        text = reader.pages[i].extract_text()
        lines = text.split('\n')
        if len(lines) > 2:
            header = lines[1].strip()
            if header in ['Ml', 'Mal', 'Malaquías']:
                # Found Malachi, check next few pages for Matthew
                pass
            elif header in ['Mt', 'Mateo']:
                print(f"!!! ENCONTRADO MATEO EN PÁGINA {i} !!!")
                print(text[:500])
                return

find_mal_mat_transition()

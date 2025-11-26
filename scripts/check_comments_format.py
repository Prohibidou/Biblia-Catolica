import PyPDF2

def find_comments():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando 'COMENTARIO' o 'COMENTARIOS'...")
    
    count = 0
    for i in range(0, 10513, 50): # Muestreo
        text = reader.pages[i].extract_text()
        if 'COMENTARIO' in text or 'COMENTARIOS' in text:
            print(f"\nPágina {i}:")
            # Mostrar contexto
            lines = text.split('\n')
            for j, line in enumerate(lines):
                if 'COMENTARIO' in line or 'COMENTARIOS' in line:
                    print(f"  {j}: {line}")
                    # Mostrar siguientes 5 líneas
                    for k in range(1, 6):
                        if j+k < len(lines):
                            print(f"    {lines[j+k]}")
            count += 1
            if count > 5: break

find_comments()

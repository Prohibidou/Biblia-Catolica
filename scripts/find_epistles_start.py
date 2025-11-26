import PyPDF2

def find_acts_rom_transition():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando transición Hch -> Rm...")
    
    for i in range(2800, 3500):
        text = reader.pages[i].extract_text()
        lines = text.split('\n')
        if len(lines) > 2:
            header = lines[1].strip()
            if header in ['Rm', 'Rom', 'Romanos']:
                print(f"!!! ENCONTRADO ROMANOS EN PÁGINA {i} !!!")
                print(text[:500])
                return

find_acts_rom_transition()

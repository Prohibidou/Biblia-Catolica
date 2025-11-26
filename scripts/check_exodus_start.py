import PyPDF2

def check_exodus_start():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    for i in range(125, 140):
        text = reader.pages[i].extract_text()
        print(f"\n{'='*60}")
        print(f"PÁGINA {i}")
        print('='*60)
        print(text[:500])
        
        if 'Estos son los nombres' in text or 'Éstos son los nombres' in text:
            print("\n!!! ENCONTRADO INICIO DE ÉXODO !!!")

check_exodus_start()

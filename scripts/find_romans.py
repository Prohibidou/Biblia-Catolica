import PyPDF2

def find_romans():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando título de ROMANOS...")
    
    for i in range(8800, 9200):
        text = reader.pages[i].extract_text()
        if 'ROMANOS' in text.upper():
            print(f"\n{'='*60}")
            print(f"PÁGINA {i}")
            print('='*60)
            print(text[:500])

find_romans()

import PyPDF2

def find_romans_text():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando 'Pablo, siervo de Cristo Jesús'...")
    
    for i in range(8800, 9200):
        text = reader.pages[i].extract_text()
        if 'Pablo' in text and 'siervo' in text and 'Cristo' in text:
            print(f"\n{'='*60}")
            print(f"PÁGINA {i}")
            print('='*60)
            print(text[:500])

find_romans_text()

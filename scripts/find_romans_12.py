import PyPDF2

def find_romans_12():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando texto de Romanos 12...")
    
    for i in range(9080, 9100):
        text = reader.pages[i].extract_text()
        if 'exhorto' in text and 'misericordia' in text:
            print(f"\n{'='*60}")
            print(f"PÁGINA {i}")
            print('='*60)
            print(text[:500])

find_romans_12()

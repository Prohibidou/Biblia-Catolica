import PyPDF2

def check_romans_start():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    for i in range(9030, 9040):
        text = reader.pages[i].extract_text()
        print(f"\n{'='*60}")
        print(f"PÁGINA {i}")
        print('='*60)
        print(text[:500])

check_romans_start()

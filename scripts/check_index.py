import PyPDF2

def check_index():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    for i in range(0, 10):
        text = reader.pages[i].extract_text()
        print(f"\n{'='*60}")
        print(f"PÁGINA {i}")
        print('='*60)
        print(text)

check_index()

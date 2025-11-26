import PyPDF2

def check_exodus_start_v2():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    for i in range(125, 130):
        text = reader.pages[i].extract_text()
        print(f"\n{'='*60}")
        print(f"PÁGINA {i}")
        print('='*60)
        print(text)

check_exodus_start_v2()

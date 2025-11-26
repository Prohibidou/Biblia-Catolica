import PyPDF2
import re

def find_titles():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    titles_to_find = [
        'GÉNESIS', 'ÉXODO', 'LEVÍTICO', 'NÚMEROS', 'DEUTERONOMIO',
        'JOSUÉ', 'JUECES', 'RUT', 'SAMUEL', 'REYES',
        'MATEO', 'MARCOS', 'LUCAS', 'JUAN', 'HECHOS', 'ROMANOS'
    ]
    
    print("Buscando páginas de título...")
    
    for i in range(0, 10513, 10): # Muestreo rápido
        try:
            text = reader.pages[i].extract_text()
            lines = text.split('\n')
            
            # Check first few lines for uppercase title
            for line in lines[:5]:
                line = line.strip()
                if line in titles_to_find:
                    print(f"Página {i}: ENCONTRADO TÍTULO '{line}'")
                    # Check context for index tabs
                    print(text[:200])
                    print("-" * 40)
        except:
            pass

find_titles()

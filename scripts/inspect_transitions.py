import PyPDF2
import re

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"

def find_book_transitions():
    print(f"Abriendo {PDF_FILE}...")
    with open(PDF_FILE, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total = len(reader.pages)
        
        # Vamos a buscar transiciones específicas
        # Gen -> Ex (alrededor de página 100-200?)
        # Oseas (HOS) parece haber absorbido mucho. Busquemos dónde empieza HOS y qué sigue
        
        print("Buscando patrones de inicio de libros...")
        
        books_to_find = ['Ex', 'Lev', 'Num', 'Dt', 'Jos', 'Jue', 'Rt', '1 S', 'Sal', 'Is', 'Mt', 'Mc']
        
        for i in range(total):
            if i % 500 == 0:
                print(f"Escaneando página {i}...")
                
            text = reader.pages[i].extract_text()
            lines = text.split('\n')
            
            for j, line in enumerate(lines):
                line = line.strip()
                
                # Posible código de libro
                if len(line) < 10 and any(b in line for b in books_to_find):
                    # Verificar si parece un título de libro
                    # A menudo seguido por "CAPÍTULO 1" o "1" y texto
                    if line in ['Ex', 'Éxodo', 'EXODO', 'Lv', 'Levítico', 'Nm', 'Números']:
                        print(f"Posible libro en pág {i+1}, línea {j}: '{line}'")
                        # Mostrar contexto
                        for k in range(max(0, j-2), min(len(lines), j+10)):
                            print(f"  {k}: {lines[k]}")
                        print("-" * 40)

find_book_transitions()

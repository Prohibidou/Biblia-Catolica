import PyPDF2

def find_acts_end():
    pdf = open('BibliaPDF/Sagrada Biblia Navarra.pdf', 'rb')
    reader = PyPDF2.PdfReader(pdf)
    
    print("Buscando final de Hechos...")
    
    # Acts text should be before comments start (before page 3000? No, comments start at 3950 for Genesis)
    # Wait, NT text is usually after OT.
    # If Genesis comments start at 3950, then OT text is 1-3950.
    # Where is NT text?
    
    # Let's search in the whole PDF for Acts 28 text
    for i in range(0, 10513, 100):
        text = reader.pages[i].extract_text()
        if 'Pablo permaneció' in text:
            print(f"Página {i} (aprox): ENCONTRADO")
            # Refine search
            for j in range(i-50, i+50):
                t = reader.pages[j].extract_text()
                if 'Pablo permaneció' in t:
                    print(f"\n{'='*60}")
                    print(f"PÁGINA {j}")
                    print('='*60)
                    print(t[:500])
                    
                    # Check next pages for Romans
                    for k in range(j+1, j+10):
                        print(f"\n--- PÁGINA {k} ---")
                        print(reader.pages[k].extract_text()[:200])
                    return

find_acts_end()

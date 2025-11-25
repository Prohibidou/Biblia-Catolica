import PyPDF2

pdf_path = r"BibliaPDF/Sagrada Biblia Navarra.pdf"
print("Abriendo Biblia de Navarra completa...")
pdf = PyPDF2.PdfReader(open(pdf_path, 'rb'))

print(f"Total páginas: {len(pdf.pages)}")

# Buscar inicio del NT en rango amplio
print("\nBuscando 'EVANGELIO' o 'MATEO' en títulos...")

for i in range(2400, 2600, 5):
    text = pdf.pages[i].extract_text()
    
    # Buscar títulos de secciones
    if 'EVANGELIO' in text.upper() or ('MATEO' in text.upper() and 'SEGÚN' in text.upper()):
        print(f"\nPágina {i+1}:")
        print(text[:800])
        print("\n" + "-"*70)
    
    # También buscar el inicio del capítulo 1
    if text.strip().startswith('1\n') or '\n1\n' in text[:100]:
        first_lines = text[:500]
        if any(word in first_lines.lower() for word in ['libro', 'genealog', 'abraham', 'generación']):
            print(f"\n*** POSIBLE MATEO 1 en página {i+1} ***")
            print(first_lines)
            print("\n" + "="*70)
            
            # Guardar muestra extensa
            sample = ''
            for j in range(max(0, i-5), min(i+35, len(pdf.pages))):
                sample += f'\n\n{"="*70} PÁGINA {j+1} {"="*70}\n\n'
                page_text = pdf.pages[j].extract_text()
                sample += page_text
                
                # También revisar si hay anotaciones/hipervínculos
                if '/Annots' in pdf.pages[j]:
                    sample += f"\n\n[NOTA: Esta página tiene anotaciones/enlaces]\n"
            
            with open('scripts/mateo_completo_analisis.txt', 'w', encoding='utf-8') as f:
                f.write(sample)
            
            print(f"\nAnálisis completo guardado en scripts/mateo_completo_analisis.txt")
            
            # Analizar anotaciones en las primeras páginas de Mateo
            print(f"\nAnalizando hipervínculos en páginas {i+1} a {i+10}...")
            for k in range(i, min(i+10, len(pdf.pages))):
                page = pdf.pages[k]
                if '/Annots' in page:
                    print(f"  Página {k+1}: Tiene anotaciones/enlaces")
                    try:
                        annots = page['/Annots']
                        print(f"    Cantidad de anotaciones: {len(annots) if hasattr(annots, '__len__') else 'N/A'}")
                    except:
                        print(f"    (No se puede determinar cantidad)")
            
            break
    
print("\nBúsqueda completada.")

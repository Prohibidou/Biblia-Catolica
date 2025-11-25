import sys
import os
import win32com.client as win32

try:
    doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
    output_path = os.path.abspath(r"scripts/nt_doc_extracted.txt")
    
    print(f"Abriendo {doc_path}...")
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    
    doc = word.Documents.Open(doc_path)
    print(f"Documento abierto.")
    
    # Intentar leer todo el texto de una vez
    print("Extrayendo todo el texto...")
    try:
        full_text = doc.Content.Text
        # Limpiar
        full_text = full_text.replace('\r', '\n').replace('\x0b', '\n')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
            
        print(f"✓ ÉXITO: Texto guardado en {output_path}")
        print(f"  Tamaño: {len(full_text)} caracteres")
        
    except Exception as e:
        print(f"Error leyendo todo el texto: {e}")
        print("Intentando método alternativo (copiar al portapapeles)...")
        try:
            doc.Content.Copy()
            # Leer del portapapeles (requiere win32clipboard)
            # Si no, volver a iterar pero por páginas
            print("Copiado al portapapeles. (No implementado lectura desde clipboard)")
        except:
            pass

    doc.Close(False)
    word.Quit()
    
except Exception as e:
    print(f"Error fatal: {e}")

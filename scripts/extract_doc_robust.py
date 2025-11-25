import sys
import os
import win32com.client as win32

try:
    # Ruta absoluta
    doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
    output_path = os.path.abspath(r"scripts/nt_doc_extracted.txt")
    
    print(f"Abriendo {doc_path}...")
    
    word = win32.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        doc = word.Documents.Open(doc_path)
        print(f"Documento abierto. Párrafos: {doc.Paragraphs.Count}")
        
        # Extraer texto párrafo por párrafo para evitar problemas de memoria con archivos grandes
        print("Extrayendo texto...")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            count = doc.Paragraphs.Count
            for i in range(1, count + 1):
                try:
                    text = doc.Paragraphs(i).Range.Text
                    # Limpiar caracteres extraños de Word
                    text = text.replace('\r', '\n').replace('\x0b', '\n')
                    f.write(text)
                    
                    if i % 1000 == 0:
                        print(f"Procesado {i}/{count} párrafos...")
                except Exception as e:
                    print(f"Error en párrafo {i}: {e}")
        
        print(f"✓ Texto guardado en {output_path}")
        
        doc.Close(False)
    except Exception as e:
        print(f"Error procesando documento: {e}")
        if 'doc' in locals():
            doc.Close(False)
            
    word.Quit()
    
except Exception as e:
    print(f"Error fatal: {e}")

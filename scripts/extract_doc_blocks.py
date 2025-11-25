import win32com.client as win32
import os

doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
output_path = os.path.abspath(r"scripts/nt_doc_extracted_blocks.txt")

print(f"Abriendo {doc_path}...")
word = win32.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(doc_path)
    count = doc.Paragraphs.Count
    print(f"Total párrafos: {count}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Procesar en bloques de 500
        block_size = 500
        for start in range(1, count + 1, block_size):
            end = min(start + block_size - 1, count)
            print(f"  Extrayendo párrafos {start} a {end}...")
            
            # Obtener rango de párrafos
            rng = doc.Range(
                doc.Paragraphs(start).Range.Start,
                doc.Paragraphs(end).Range.End
            )
            text = rng.Text
            
            # Limpiar
            text = text.replace('\r', '\n').replace('\x0b', '\n').replace('\x07', '')
            f.write(text)
            f.flush() # Asegurar escritura
            
    print(f"✓ Texto guardado en {output_path}")

except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        doc.Close(False)
        word.Quit()
    except:
        pass

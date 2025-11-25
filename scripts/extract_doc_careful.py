import win32com.client as win32
import os

doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
output_path = os.path.abspath(r"scripts/nt_doc_extracted_careful.txt")

print(f"Abriendo {doc_path}...")
word = win32.Dispatch("Word.Application")
word.Visible = False

doc = word.Documents.Open(doc_path)
print(f"Documento abierto. Total párrafos: {doc.Paragraphs.Count}")

# Estrategia: Extraer párrafo por párrafo, en orden
print("Extrayendo párrafo por párrafo...")

with open(output_path, 'w', encoding='utf-8') as f:
    for i, para in enumerate(doc.Paragraphs):
        if i % 1000 == 0:
            print(f"  Procesando párrafo {i}/{doc.Paragraphs.Count}...")
        
        text = para.Range.Text
        # Limpiar caracteres especiales de Word
        text = text.replace('\r', '\n').replace('\x0b', '\n').replace('\x07', '')
        f.write(text)

print(f"✓ Texto guardado en {output_path}")

doc.Close(False)
word.Quit()

# Verificar tamaño
size = os.path.getsize(output_path)
print(f"  Tamaño: {size/1024/1024:.2f} MB")

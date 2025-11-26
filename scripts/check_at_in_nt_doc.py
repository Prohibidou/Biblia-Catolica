import win32com.client as win32
import os
import json
import re

doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")

print(f"Buscando comentarios del AT en: {doc_path}")

word = win32.Dispatch("Word.Application")
word.Visible = False

try:
    doc = word.Documents.Open(doc_path)
    full_text = doc.Range().Text
    
    print(f"Texto extraído: {len(full_text)} caracteres")
    
    # Buscar menciones de libros del AT
    at_books = ['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio', 
                'Josué', 'Jueces', 'Samuel', 'Reyes', 'Crónicas',
                'Esdras', 'Nehemías', 'Tobías', 'Judit', 'Ester',
                'Macabeos', 'Job', 'Salmos', 'Proverbios', 'Eclesiastés',
                'Cantar', 'Sabiduría', 'Eclesiástico', 'Isaías', 'Jeremías',
                'Lamentaciones', 'Baruc', 'Ezequiel', 'Daniel',
                'Oseas', 'Joel', 'Amós', 'Abdías', 'Jonás', 'Miqueas',
                'Nahúm', 'Habacuc', 'Sofonías', 'Ageo', 'Zacarías', 'Malaquías']
    
    mentions = {}
    for book in at_books:
        count = full_text.count(book)
        if count > 0:
            mentions[book] = count
    
    print("\nLibros del AT mencionados:")
    for book, count in sorted(mentions.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {book}: {count} veces")
    
    # Buscar patrones de referencias del AT (ej: "Gn 1,1" o "Ex 3,14")
    at_refs = re.findall(r'(Gn|Ex|Lv|Nm|Dt|Jos|Jue|Rt|1S|2S|1R|2R|Sal|Is|Jr|Ez|Dan)\s+\d+,\d+', full_text)
    
    print(f"\nReferencias del AT encontradas: {len(at_refs)}")
    if at_refs:
        print("Ejemplos:")
        for ref in at_refs[:10]:
            print(f"  - {ref}")
    
    doc.Close(False)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    try:
        word.Quit()
    except:
        pass

print("\nConclusión: Este archivo parece ser solo del NT (como dice el nombre).")
print("Los comentarios del AT probablemente están en el PDF 'Sagrada Biblia Navarra.pdf'")

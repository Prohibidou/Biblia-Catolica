#!/usr/bin/env python3
"""
Extractor de Comentarios para Sagrada Biblia Navarra
Busca bloques "COMENTARIO" y extrae referencias y texto.
"""
import PyPDF2
import re
import json

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_comments.json"

def extract_comments():
    print(f"📖 Extrayendo Comentarios de: {PDF_FILE}")
    
    comments = []
    current_comment = None
    
    with open(PDF_FILE, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        
        # Empezar a buscar desde donde sabemos que hay comentarios
        # Génesis empieza aprox en 3950
        # Pero escaneamos todo por si acaso
        
        for i in range(3000, total_pages):
            if i % 500 == 0: print(f"   Escaneando página {i}...")
            
            text = reader.pages[i].extract_text()
            if not text: continue
            
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Detectar inicio de comentario
                if line == "COMENTARIO" or line == "COMENTARIOS":
                    # Guardar anterior si existe
                    if current_comment:
                        comments.append(current_comment)
                    
                    current_comment = {
                        'page': i,
                        'ref_raw': '',
                        'text': []
                    }
                    continue
                
                # Si estamos dentro de un comentario
                if current_comment:
                    # La primera línea después de COMENTARIO suele ser la referencia
                    if not current_comment['ref_raw']:
                        # Validar si parece referencia (tiene números)
                        if any(c.isdigit() for c in line):
                            current_comment['ref_raw'] = line
                        else:
                            # A veces hay líneas intermedias?
                            pass
                    else:
                        # Acumular texto
                        # Ignorar "Volver a..."
                        if "Volver a" in line:
                            continue
                        current_comment['text'].append(line)

    # Guardar último
    if current_comment:
        comments.append(current_comment)
        
    print(f"✅ Extraídos {len(comments)} comentarios")
    
    # Procesar referencias
    processed_comments = []
    for c in comments:
        ref = c['ref_raw']
        text = " ".join(c['text']).strip()
        
        # Intentar extraer libro, cap, vers
        # Ej: "Gn 1,1-5", "Mt 21,28-46", "1 Co 7,39-40"
        
        # Separar libro de números
        # Buscar el primer dígito
        match = re.search(r'\d', ref)
        if match:
            idx = match.start()
            book_code = ref[:idx].strip()
            nums = ref[idx:].strip()
            
            processed_comments.append({
                'book_code': book_code,
                'reference': nums,
                'text': text
            })
            
    print(f"💾 Guardando en {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(processed_comments, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_comments()

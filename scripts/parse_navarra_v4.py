#!/usr/bin/env python3
"""
Parser v4 para Sagrada Biblia Navarra
- Códigos cortos corregidos (Rm, 1 Co, etc.)
- Extracción de Texto y Comentarios
"""
import PyPDF2
import re
import json
from collections import defaultdict

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_v4_complete.json"

# Códigos cortos EXACTOS del PDF (según índice)
SHORT_CODES = {
    'Gn': 'GEN', 'Ex': 'EXO', 'Lv': 'LEV', 'Nm': 'NUM', 'Dt': 'DEU',
    'Jos': 'JOS', 'Jc': 'JDG', 'Rt': 'RUT', '1 S': '1SA', '2 S': '2SA',
    '1 R': '1KI', '2 R': '2KI', '1 Cro': '1CH', '2 Cro': '2CH',
    'Esd': 'EZR', 'Ne': 'NEH', 'Tb': 'TOB', 'Jdt': 'JDT', 'Est': 'EST',
    '1 M': '1MA', '2 M': '2MA', 'Jb': 'JOB', 'Sal': 'PSA', 'Pr': 'PRO',
    'Qo': 'ECC', 'Ct': 'SNG', 'Sb': 'WIS', 'Si': 'SIR', 'Is': 'ISA',
    'Jr': 'JER', 'Lm': 'LAM', 'Ba': 'BAR', 'Ez': 'EZK', 'Dn': 'DAN',
    'Os': 'HOS', 'Jl': 'JOL', 'Am': 'AMO', 'Ab': 'OBA', 'Jon': 'JON',
    'Mi': 'MIC', 'Na': 'NAM', 'Ha': 'HAB', 'So': 'ZEP', 'Ag': 'HAG',
    'Za': 'ZEC', 'Ml': 'MAL',
    'Mt': 'MAT', 'Mc': 'MRK', 'Lc': 'LUK', 'Jn': 'JHN', 'Hch': 'ACT',
    'Rm': 'ROM', '1 Co': '1CO', '2 Co': '2CO', 'Ga': 'GAL', 'Ef': 'EPH',
    'Flp': 'PHP', 'Col': 'COL', '1 Ts': '1TH', '2 Ts': '2TH',
    '1 Tm': '1TI', '2 Tm': '2TI', 'Tt': 'TIT', 'Flm': 'PHM', 'Hb': 'HEB',
    'St': 'JAS', '1 P': '1PE', '2 P': '2PE', '1 Jn': '1JN', '2 Jn': '2JN',
    '3 Jn': '3JN', 'Jds': 'JUD', 'Ap': 'REV'
}

BIBLE_ORDER = [
    'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA',
    '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'TOB', 'JDT', 'EST', '1MA',
    '2MA', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG', 'WIS', 'SIR', 'ISA', 'JER',
    'LAM', 'BAR', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC',
    'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL',
    'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH',
    'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS',
    '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'
]

def extract_pdf(pdf_path):
    print(f"📖 Extrayendo PDF: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        lines = []
        for i, page in enumerate(reader.pages):
            if i % 1000 == 0: print(f"   Página {i}...")
            text = page.extract_text()
            if text:
                lines.append(f"___PAGE_START_{i}___")
                lines.extend(text.split('\n'))
        return lines

def parse_v4(lines):
    print("🔍 Parsing v4 (Texto + Comentarios)...")
    
    verses = []
    comments = []
    
    current_book = None
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    title_buffer = []
    pending_verse_num = None
    
    # Estado
    is_header = False
    lines_since_page_start = 0
    in_comments_section = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        if line.startswith("___PAGE_START_"):
            lines_since_page_start = 0
            is_header = True
            # Detectar cambio a sección de comentarios (aprox pág 3200+)
            # Pero mejor detectarlo por contenido "COMENTARIO"
            continue
            
        lines_since_page_start += 1
        if lines_since_page_start > 2:
            is_header = False
            
        # DETECCIÓN DE COMENTARIOS
        if line == "COMENTARIO" or line == "COMENTARIOS":
            in_comments_section = True
            # La siguiente línea suele ser la referencia
            # Pero la procesaremos en la siguiente iteración
            continue
            
        if in_comments_section:
            # Intentar parsear referencia: "Gn 1,1-5" o "Mt 21,28-46"
            # Patrón: [Código] [Cap],[Vers]-[Vers]
            # O simplemente capturar todo el bloque hasta el próximo COMENTARIO
            
            # Por ahora, guardamos la línea como posible comentario
            # Necesitamos una lógica más robusta para asociar comentarios
            # Pero primero aseguremos el TEXTO
            pass

        # DETECCIÓN DE LIBRO (Header)
        if is_header and line in SHORT_CODES:
            code_book = SHORT_CODES[line]
            if current_book != code_book:
                # Validar orden
                curr_idx = BIBLE_ORDER.index(current_book) if current_book in BIBLE_ORDER else -1
                new_idx = BIBLE_ORDER.index(code_book) if code_book in BIBLE_ORDER else -1
                
                # Permitir saltos si es razonable (ej: JHN -> ACT -> ROM)
                if new_idx > curr_idx:
                     print(f"📘 CAMBIO DE LIBRO (Header): {current_book} -> {code_book}")
                     current_book = code_book
                     current_chapter = 0
                     current_verse = 0
                     pending_verse_num = None
                     verse_buffer = ""
            continue

        # PARSING DE VERSÍCULOS
        if not current_book: 
            # Caso especial Génesis
            if line == 'Gn':
                 if i+10 < len(lines) and "principio" in " ".join(lines[i:i+10]):
                     current_book = 'GEN'
                     print("✓ Inicio GÉNESIS")
            continue
        
        # Si es número de versículo
        if line.isdigit() and 1 <= len(line) <= 3:
            num = int(line)
            
            if pending_verse_num is not None and verse_buffer:
                if pending_verse_num == 1 and current_verse > 1:
                    current_chapter += 1
                elif current_chapter == 0:
                    current_chapter = 1
                
                verses.append({
                    'book': current_book,
                    'chapter': current_chapter,
                    'verse': pending_verse_num,
                    'text': verse_buffer.strip(),
                    'title': ' | '.join(title_buffer) if title_buffer else ''
                })
                current_verse = pending_verse_num
                verse_buffer = ""
                title_buffer = []
            
            pending_verse_num = num
            continue
            
        # Texto
        if pending_verse_num is not None:
            # Detectar título (mayúsculas)
            letters = [c for c in line if c.isalpha()]
            if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.8:
                title_buffer.append(line)
            else:
                verse_buffer += " " + line
            
    # Guardar último
    if verse_buffer and pending_verse_num:
        verses.append({
            'book': current_book,
            'chapter': current_chapter,
            'verse': pending_verse_num,
            'text': verse_buffer.strip()
        })

    return verses

def save(verses):
    print(f"💾 Guardando {len(verses)} versículos...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump({'data': verses}, f, ensure_ascii=False, indent=2)
        
    # Stats
    counts = defaultdict(int)
    for v in verses: counts[v['book']] += 1
    print("\nEstadísticas:")
    for book in BIBLE_ORDER:
        if counts[book] > 0:
            print(f"  {book}: {counts[book]}")

if __name__ == "__main__":
    lines = extract_pdf(PDF_FILE)
    verses = parse_v4(lines)
    save(verses)

#!/usr/bin/env python3
"""
Parser CORRECTO para Sagrada Biblia Navarra
Maneja el formato real: número de versículo en una línea, texto en la siguiente
"""
import PyPDF2
import re
import json
from collections import defaultdict

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_completa_final.json"

# Mapeo de códigos bíblicos
BOOK_CODES = {
    'Gn': 'GEN', 'Ex': 'EXO', 'Lv': 'LEV', 'Nm': 'NUM', 'Dt': 'DEU',
    'Jos': 'JOS', 'Jue': 'JDG', 'Rt': 'RUT', 
    '1 S': '1SA', '2 S': '2SA', '1 R': '1KI', '2 R': '2KI',
    '1 Cro': '1CH', '2 Cro': '2CH', 'Esd': 'EZR', 'Neh': 'NEH',
    'Tob': 'TOB', 'Jdt': 'JDT', 'Est': 'EST', '1 Mac': '1MA', '2 Mac': '2MA',
    'Job': 'JOB', 'Sal': 'PSA', 'Pr': 'PRO', 'Ecl': 'ECC', 'Cant': 'SNG',
    'Sab': 'WIS', 'Eclo': 'SIR', 'Is': 'ISA', 'Jer': 'JER', 'Lam': 'LAM',
    'Bar': 'BAR', 'Ez': 'EZK', 'Dan': 'DAN', 'Os': 'HOS', 'Jl': 'JOL',
    'Am': 'AMO', 'Abd': 'OBA', 'Jon': 'JON', 'Miq': 'MIC', 'Nah': 'NAM',
    'Hab': 'HAB', 'Sof': 'ZEP', 'Ag': 'HAG', 'Zac': 'ZEC', 'Mal': 'MAL',
    'Mt': 'MAT', 'Mc': 'MRK', 'Lc': 'LUK', 'Jn': 'JHN', 'Hch': 'ACT',
    'Rom': 'ROM', '1 Cor': '1CO', '2 Cor': '2CO', 'Gal': 'GAL', 'Ef': 'EPH',
    'Flp': 'PHP', 'Col': 'COL', '1 Tes': '1TH', '2 Tes': '2TH',
    '1 Tim': '1TI', '2 Tim': '2TI', 'Tit': 'TIT', 'Flm': 'PHM',
    'Heb': 'HEB', 'Sant': 'JAS', '1 Pe': '1PE', '2 Pe': '2PE',
    '1 Jn': '1JN', '2 Jn': '2JN', '3 Jn': '3JN', 'Jud': 'JUD', 'Ap': 'REV'
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

EXPECTED_CHAPTERS = {
    'GEN': 50, 'EXO': 40, 'LEV': 27, 'NUM': 36, 'DEU': 34, 'JOS': 24, 'JDG': 21,
    'RUT': 4, '1SA': 31, '2SA': 24, '1KI': 22, '2KI': 25, '1CH': 29, '2CH': 36,
    'EZR': 10, 'NEH': 13, 'TOB': 14, 'JDT': 16, 'EST': 10, '1MA': 16, '2MA': 15,
    'JOB': 42, 'PSA': 150, 'PRO': 31, 'ECC': 12, 'SNG': 8, 'WIS': 19, 'SIR': 51,
    'ISA': 66, 'JER': 52, 'LAM': 5, 'BAR': 6, 'EZK': 48, 'DAN': 14, 'HOS': 14,
    'JOL': 4, 'AMO': 9, 'OBA': 1, 'JON': 4, 'MIC': 7, 'NAM': 3, 'HAB': 3,
    'ZEP': 3, 'HAG': 2, 'ZEC': 14, 'MAL': 3,
    'MAT': 28, 'MRK': 16, 'LUK': 24, 'JHN': 21, 'ACT': 28, 'ROM': 16,
    '1CO': 16, '2CO': 13, 'GAL': 6, 'EPH': 6, 'PHP': 4, 'COL': 4, '1TH': 5,
    '2TH': 3, '1TI': 6, '2TI': 4, 'TIT': 3, 'PHM': 1, 'HEB': 13, 'JAS': 5,
    '1PE': 5, '2PE': 3, '1JN': 5, '2JN': 1, '3JN': 1, 'JUD': 1, 'REV': 22
}


def extract_pdf(pdf_path):
    """Extrae texto del PDF"""
    print(f"📖 Extrayendo PDF: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total = len(reader.pages)
        print(f"   Páginas: {total:,}")
        
        lines = []
        for i in range(total):
            if i % 500 == 0:
                print(f"   Página {i+1}/{total}...")
            text = reader.pages[i].extract_text()
            if text:
                lines.extend(text.split('\n'))
        
        print(f"✅ Extraídas {len(lines):,} líneas\n")
        return lines


def is_verse_number(line):
    """Verifica si es un número de versículo (solo dígitos, 1-3 dígitos)"""
    line = line.strip()
    return line.isdigit() and 1 <= len(line) <= 3


def is_title(line):
    """Detecta títulos (mayúsculas)"""
    line = line.strip()
    if not line or len(line) < 3:
        return False
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    return sum(1 for c in letters if c.isupper()) / len(letters) > 0.6


def parse_correct(lines):
    """Parser que maneja el formato correcto del PDF"""
    print("🔍 Parsing Biblia Navarra (formato correcto)...\n")
    
    verses = []
    current_book = None
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    title_buffer = []
    pending_verse_num = None  # Número de versículo detectado
    
    verse_count = 0
    title_count = 0
    chapter_count = defaultdict(int)
    
    processing = False
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Ignorar vacías
        if not line:
            i += 1
            continue
        
        # Progreso
        if i % 50000 == 0 and i > 0:
            print(f"   Línea {i:,}/{len(lines):,} - Libros: {len(chapter_count)}, Versículos: {verse_count}")
        
        # Buscar inicio (Génesis)
        if not processing:
            # Buscar "Gn" seguido eventualmente por "1" y "En el principio"
            if line == 'Gn':
                # Verificar las siguientes líneas
                for j in range(i+1, min(i+20, len(lines))):
                    if 'principio' in lines[j].lower() and 'creó' in lines[j].lower():
                        processing = True
                        current_book = 'GEN'
                        current_chapter = 1
                        chapter_count['GEN'] = 1
                        print(f"✓ Inicio en Génesis (línea {i})\n")
                        break
            i += 1
            continue
        
        # Detectar código de libro (solo en línea)
        if line in BOOK_CODES:
            detected_book = BOOK_CODES[line]
            
            # Verificar si es siguiente en orden bíblico
            if current_book:
                current_idx = BIBLE_ORDER.index(current_book) if current_book in BIBLE_ORDER else -1
                detected_idx = BIBLE_ORDER.index(detected_book) if detected_book in BIBLE_ORDER else -1
                
                if detected_idx > current_idx:
                    # Guardar versículo pendiente
                    if verse_buffer and current_verse > 0:
                        verses.append({
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': current_verse,
                            'text': verse_buffer.strip(),
                            'title': ' | '.join(title_buffer) if title_buffer else ''
                        })
                        verse_count += 1
                        if title_buffer:
                            title_count += 1
                        verse_buffer = ""
                        title_buffer = []
                        pending_verse_num = None
                    
                    current_book = detected_book
                    current_chapter = 0
                    current_verse = 0
                    print(f"📕 Libro: {detected_book}")
            i += 1
            continue
        
        # Detectar número de versículo
        if is_verse_number(line):
            verse_num = int(line)
            
            # Si tenemos un número pendiente, guardar el versículo anterior
            if pending_verse_num is not None and verse_buffer:
                # Determinar capítulo
                if pending_verse_num == 1 and current_verse > 1:
                    # Guardar versículo anterior
                    verses.append({
                        'book': current_book,
                        'chapter': current_chapter,
                        'verse': current_verse,
                        'text': verse_buffer.strip(),
                        'title': ' | '.join(title_buffer) if title_buffer else ''
                    })
                    verse_count += 1
                    if title_buffer:
                        title_count += 1
                    
                    # Nuevo capítulo
                    current_chapter += 1
                    chapter_count[current_book] += 1
                    current_verse = pending_verse_num
                    verse_buffer = ""
                    title_buffer = []
                
                elif pending_verse_num == current_verse + 1 or (current_verse == 0 and pending_verse_num == 1):
                    # Guardar anterior
                    if current_verse > 0:
                        verses.append({
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': current_verse,
                            'text': verse_buffer.strip(),
                            'title': ' | '.join(title_buffer) if title_buffer else ''
                        })
                        verse_count += 1
                        if title_buffer:
                            title_count += 1
                    
                    if current_chapter == 0:
                        current_chapter = 1
                        chapter_count[current_book] = 1
                    
                    current_verse = pending_verse_num
                    verse_buffer = ""
                    title_buffer = []
            
            # Guardar nuevo número pendiente
            pending_verse_num = verse_num
            i += 1
            continue
        
        # Detectar título
        if is_title(line) and not pending_verse_num:
            title_buffer.append(line)
            i += 1
            continue
        
        # Texto normal - agregar al buffer del versículo actual
        if pending_verse_num is not None:
            if verse_buffer:
                verse_buffer += " " + line
            else:
                verse_buffer = line
        
        i += 1
    
    # Guardar último versículo
    if verse_buffer and pending_verse_num and current_book:
        verses.append({
            'book': current_book,
            'chapter': current_chapter,
            'verse': pending_verse_num,
            'text': verse_buffer.strip(),
            'title': ' | '.join(title_buffer) if title_buffer else ''
        })
        verse_count += 1
    
    print(f"\n✅ Parsing completado:")
    print(f"   Versículos: {verse_count:,}")
    print(f"   Con títulos: {title_count:,}")
    print(f"   Libros: {len(chapter_count)}")
    
    return verses, chapter_count


def save_json(verses, chapter_count):
    """Guarda en JSON"""
    structure = defaultdict(lambda: defaultdict(list))
    for v in verses:
        structure[v['book']][v['chapter']].append(v)
    
    output = {
        'version': 'Sagrada Biblia Navarra',
        'source': 'PDF completo - formato correcto',
        'total_verses': len(verses),
        'total_books': len(chapter_count),
        'data': verses
    }
    
    print(f"\n💾 Guardando en {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n📚 Resumen por libro:")
    for book in BIBLE_ORDER:
        if book in structure:
            ch = len(structure[book])
            vv = sum(len(structure[book][c]) for c in structure[book])
            expected = EXPECTED_CHAPTERS.get(book, '?')
            status = "✅" if ch == expected else f"⚠️ ({ch}/{expected})"
            print(f"   {status:15s} {book:6s}: {vv:5d} vers")


def main():
    print("="*70)
    print("NAVARRA BIBLE - PARSER CORRECTO")
    print("Formato: Número en una línea, texto en la siguiente")
    print("="*70)
    print()
    
    lines = extract_pdf(PDF_FILE)
    verses, chapter_count = parse_correct(lines)
    save_json(verses, chapter_count)
    
    print(f"\n✅ ¡COMPLETADO! Archivo: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()

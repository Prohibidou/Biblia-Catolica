#!/usr/bin/env python3
"""
Parser v3 para Sagrada Biblia Navarra
Estrategia: Detectar Títulos Completos para cambio de libro
"""
import PyPDF2
import re
import json
from collections import defaultdict

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_v3.json"

# Mapeo de Nombres Completos a Códigos
BOOK_NAMES = {
    'GÉNESIS': 'GEN', 'ÉXODO': 'EXO', 'LEVÍTICO': 'LEV', 'NÚMEROS': 'NUM', 'DEUTERONOMIO': 'DEU',
    'JOSUÉ': 'JOS', 'JUECES': 'JDG', 'RUT': 'RUT', 
    'SAMUEL': '1SA', # Cuidado con 1 y 2
    'REYES': '1KI', # Cuidado
    'CRÓNICAS': '1CH', # Cuidado
    'ESDRAS': 'EZR', 'NEHEMÍAS': 'NEH', 'TOBÍAS': 'TOB', 'JUDIT': 'JDT', 'ESTER': 'EST',
    'MACABEOS': '1MA', # Cuidado
    'JOB': 'JOB', 'SALMOS': 'PSA', 'PROVERBIOS': 'PRO', 'ECLESIASTÉS': 'ECC', 
    'CANTAR DE LOS CANTARES': 'SNG', 'SABIDURÍA': 'WIS', 'ECLESIÁSTICO': 'SIR',
    'ISAÍAS': 'ISA', 'JEREMÍAS': 'JER', 'LAMENTACIONES': 'LAM', 'BARUC': 'BAR',
    'EZEQUIEL': 'EZK', 'DANIEL': 'DAN', 'OSEAS': 'HOS', 'JOEL': 'JOL', 'AMÓS': 'AMO',
    'ABDÍAS': 'OBA', 'JONÁS': 'JON', 'MIQUEAS': 'MIC', 'NAHÚM': 'NAM', 'HABACUC': 'HAB',
    'SOFONÍAS': 'ZEP', 'AGEO': 'HAG', 'ZACARÍAS': 'ZEC', 'MALAQUÍAS': 'MAL',
    'MATEO': 'MAT', 'MARCOS': 'MRK', 'LUCAS': 'LUK', 'JUAN': 'JHN', 
    'HECHOS DE LOS APÓSTOLES': 'ACT', 'HECHOS': 'ACT',
    'ROMANOS': 'ROM', 'CORINTIOS': '1CO', 'GÁLATAS': 'GAL', 'EFESIOS': 'EPH',
    'FILIPENSES': 'PHP', 'COLOSENSES': 'COL', 'TESALONICENSES': '1TH',
    'TIMOTEO': '1TI', 'TITO': 'TIT', 'FILEMÓN': 'PHM', 'HEBREOS': 'HEB',
    'SANTIAGO': 'JAS', 'PEDRO': '1PE', 'JUDAS': 'JUD', 'APOCALIPSIS': 'REV'
}

# Códigos cortos para validación
SHORT_CODES = {
    'Gn': 'GEN', 'Ex': 'EXO', 'Lv': 'LEV', 'Nm': 'NUM', 'Dt': 'DEU',
    'Jos': 'JOS', 'Jue': 'JDG', 'Rt': 'RUT', '1 S': '1SA', '2 S': '2SA',
    '1 R': '1KI', '2 R': '2KI', '1 Cro': '1CH', '2 Cro': '2CH',
    'Esd': 'EZR', 'Neh': 'NEH', 'Tob': 'TOB', 'Jdt': 'JDT', 'Est': 'EST',
    '1 Mac': '1MA', '2 Mac': '2MA', 'Job': 'JOB', 'Sal': 'PSA', 'Pr': 'PRO',
    'Ecl': 'ECC', 'Cant': 'SNG', 'Sab': 'WIS', 'Eclo': 'SIR', 'Is': 'ISA',
    'Jer': 'JER', 'Lam': 'LAM', 'Bar': 'BAR', 'Ez': 'EZK', 'Dan': 'DAN',
    'Os': 'HOS', 'Jl': 'JOL', 'Am': 'AMO', 'Abd': 'OBA', 'Jon': 'JON',
    'Miq': 'MIC', 'Nah': 'NAM', 'Hab': 'HAB', 'Sof': 'ZEP', 'Ag': 'HAG',
    'Zac': 'ZEC', 'Mal': 'MAL',
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

def extract_pdf(pdf_path):
    print(f"📖 Extrayendo PDF: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        lines = []
        for i, page in enumerate(reader.pages):
            if i % 1000 == 0: print(f"   Página {i}...")
            text = page.extract_text()
            if text:
                # Marcar inicio de página para lógica de headers
                lines.append(f"___PAGE_START_{i}___")
                lines.extend(text.split('\n'))
        return lines

def is_verse_number(line):
    return line.strip().isdigit() and 1 <= len(line.strip()) <= 3

def parse_v3(lines):
    print("🔍 Parsing v3 (Detección por Títulos)...")
    
    verses = []
    current_book = None
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    title_buffer = []
    pending_verse_num = None
    
    # Estado
    is_header = False
    lines_since_page_start = 0
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        # Detectar inicio de página
        if line.startswith("___PAGE_START_"):
            lines_since_page_start = 0
            is_header = True
            continue
        
        lines_since_page_start += 1
        if lines_since_page_start > 2:
            is_header = False
            
        # 1. DETECCIÓN DE LIBRO POR TÍTULO COMPLETO
        if line in BOOK_NAMES:
            # Caso especial para libros numerados (1 Samuel, etc)
            # Necesitamos ver si hay un número antes o después
            # Por ahora simplificamos: si encontramos "ÉXODO", es EXO
            new_book = BOOK_NAMES[line]
            
            # Validar cambio de libro
            if current_book != new_book:
                # Verificar orden
                curr_idx = BIBLE_ORDER.index(current_book) if current_book in BIBLE_ORDER else -1
                new_idx = BIBLE_ORDER.index(new_book) if new_book in BIBLE_ORDER else -1
                
                if new_idx > curr_idx:
                    print(f"📕 CAMBIO DE LIBRO (Título): {current_book} -> {new_book}")
                    current_book = new_book
                    current_chapter = 0
                    current_verse = 0
                    pending_verse_num = None
                    verse_buffer = ""
            continue
            
        # 2. DETECCIÓN POR CÓDIGO CORTO (Solo en Header)
        if is_header and line in SHORT_CODES:
            code_book = SHORT_CODES[line]
            if current_book and code_book != current_book:
                # Solo cambiar si es el SIGUIENTE libro lógico
                # Y no es una página de índice (evitar falsos positivos)
                curr_idx = BIBLE_ORDER.index(current_book) if current_book in BIBLE_ORDER else -1
                new_idx = BIBLE_ORDER.index(code_book) if code_book in BIBLE_ORDER else -1
                
                # Si es el libro inmediatamente siguiente, aceptarlo
                if new_idx == curr_idx + 1:
                     print(f"📘 CAMBIO DE LIBRO (Header): {current_book} -> {code_book}")
                     current_book = code_book
                     current_chapter = 0
                     current_verse = 0
                     pending_verse_num = None
                     verse_buffer = ""
            continue

        # 3. INICIO DE GÉNESIS (Caso especial)
        if not current_book and line == 'Gn':
            # Verificar contexto
            if i+10 < len(lines):
                context = " ".join(lines[i:i+10])
                if "principio" in context and "creó" in context:
                    current_book = 'GEN'
                    print("✓ Inicio GÉNESIS detectado")
            continue

        # 4. PARSING DE VERSÍCULOS
        if not current_book: continue
        
        # Si es número de versículo
        if is_verse_number(line):
            num = int(line)
            
            # Lógica de guardado del anterior
            if pending_verse_num is not None and verse_buffer:
                # Determinar si es nuevo capítulo
                if pending_verse_num == 1 and current_verse > 1:
                    current_chapter += 1
                elif current_chapter == 0:
                    current_chapter = 1
                
                # Guardar
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
            
        # Si es texto
        if pending_verse_num is not None:
            # Verificar si es título (mayúsculas)
            # Pero cuidado, a veces el texto empieza con mayúsculas
            # Mejor: si tenemos versículo pendiente, asumimos que es texto
            # A MENOS que sea claramente un título de sección
            
            # Acumular texto
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

if __name__ == "__main__":
    lines = extract_pdf(PDF_FILE)
    verses = parse_v3(lines)
    save(verses)

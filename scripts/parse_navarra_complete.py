#!/usr/bin/env python3
"""
Parser completo para Sagrada Biblia Navarra.pdf
Extrae capítulos, versículos, títulos y comentarios para AT y NT
"""
import PyPDF2
import re
import json
from collections import defaultdict

# Configuración
PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_FILE = "scripts/navarra_biblia_completa_con_comentarios.json"

# Mapeo de códigos de libros y nombres completos
BOOK_MAPPING = {
    # Antiguo Testamento
    'Gn': 'GEN', 'Génesis': 'GEN', 'GÉNESIS': 'GEN',
    'Ex': 'EXO', 'Éxodo': 'EXO', 'ÉXODO': 'EXO',
    'Lv': 'LEV', 'Levítico': 'LEV', 'LEVÍTICO': 'LEV',
    'Nm': 'NUM', 'Números': 'NUM', 'NÚMEROS': 'NUM',
    'Dt': 'DEU', 'Deuteronomio': 'DEU', 'DEUTERONOMIO': 'DEU',
    'Jos': 'JOS', 'Josué': 'JOS', 'JOSUÉ': 'JOS',
    'Jue': 'JDG', 'Jueces': 'JDG', 'JUECES': 'JDG',
    'Rt': 'RUT', 'Rut': 'RUT', 'RUT': 'RUT',
    '1 S': '1SA', '1 Sam': '1SA', '1 Samuel': '1SA', '1 SAMUEL': '1SA',
    '2 S': '2SA', '2 Sam': '2SA', '2 Samuel': '2SA', '2 SAMUEL': '2SA',
    '1 R': '1KI', '1 Re': '1KI', '1 Reyes': '1KI', '1 REYES': '1KI',
    '2 R': '2KI', '2 Re': '2KI', '2 Reyes': '2KI', '2 REYES': '2KI',
    '1 Cro': '1CH', '1 Crónicas': '1CH', '1 CRÓNICAS': '1CH',
    '2 Cro': '2CH', '2 Crónicas': '2CH', '2 CRÓNICAS': '2CH',
    'Esd': 'EZR', 'Esdras': 'EZR', 'ESDRAS': 'EZR',
    'Neh': 'NEH', 'Nehemías': 'NEH', 'NEHEMÍAS': 'NEH',
    'Tob': 'TOB', 'Tobías': 'TOB', 'TOBÍAS': 'TOB',
    'Jdt': 'JDT', 'Judit': 'JDT', 'JUDIT': 'JDT',
    'Est': 'EST', 'Ester': 'EST', 'ESTER': 'EST',
    '1 Mac': '1MA', '1 Macabeos': '1MA', '1 MACABEOS': '1MA',
    '2 Mac': '2MA', '2 Macabeos': '2MA', '2 MACABEOS': '2MA',
    'Job': 'JOB', 'JOB': 'JOB',
    'Sal': 'PSA', 'Salmos': 'PSA', 'SALMOS': 'PSA',
    'Pr': 'PRO', 'Prov': 'PRO', 'Proverbios': 'PRO', 'PROVERBIOS': 'PRO',
    'Ecl': 'ECC', 'Eclesiastés': 'ECC', 'ECLESIASTÉS': 'ECC',
    'Cant': 'SNG', 'Cantar': 'SNG', 'Cantar de los Cantares': 'SNG', 'CANTAR': 'SNG',
    'Sab': 'WIS', 'Sabiduría': 'WIS', 'SABIDURÍA': 'WIS',
    'Eclo': 'SIR', 'Eclesiástico': 'SIR', 'ECLESIÁSTICO': 'SIR',
    'Is': 'ISA', 'Isaías': 'ISA', 'ISAÍAS': 'ISA',
    'Jer': 'JER', 'Jeremías': 'JER', 'JEREMÍAS': 'JER',
    'Lam': 'LAM', 'Lamentaciones': 'LAM', 'LAMENTACIONES': 'LAM',
    'Bar': 'BAR', 'Baruc': 'BAR', 'BARUC': 'BAR',
    'Ez': 'EZK', 'Ezequiel': 'EZK', 'EZEQUIEL': 'EZK',
    'Dan': 'DAN', 'Daniel': 'DAN', 'DANIEL': 'DAN',
    'Os': 'HOS', 'Oseas': 'HOS', 'OSEAS': 'HOS',
    'Jl': 'JOL', 'Joel': 'JOL', 'JOEL': 'JOL',
    'Am': 'AMO', 'Amós': 'AMO', 'AMÓS': 'AMO',
    'Abd': 'OBA', 'Abdías': 'OBA', 'ABDÍAS': 'OBA',
    'Jon': 'JON', 'Jonás': 'JON', 'JONÁS': 'JON',
    'Miq': 'MIC', 'Miqueas': 'MIC', 'MIQUEAS': 'MIC',
    'Nah': 'NAM', 'Nahúm': 'NAM', 'NAHÚM': 'NAM',
    'Hab': 'HAB', 'Habacuc': 'HAB', 'HABACUC': 'HAB',
    'Sof': 'ZEP', 'Sofonías': 'ZEP', 'SOFONÍAS': 'ZEP',
    'Ag': 'HAG', 'Ageo': 'HAG', 'AGEO': 'HAG',
    'Zac': 'ZEC', 'Zacarías': 'ZEC', 'ZACARÍAS': 'ZEC',
    'Mal': 'MAL', 'Malaquías': 'MAL', 'MALAQUÍAS': 'MAL',
    
    # Nuevo Testamento
    'Mt': 'MAT', 'Mateo': 'MAT', 'MATEO': 'MAT',
    'Mc': 'MRK', 'Marcos': 'MRK', 'MARCOS': 'MRK',
    'Lc': 'LUK', 'Lucas': 'LUK', 'LUCAS': 'LUK',
    'Jn': 'JHN', 'Juan': 'JHN', 'JUAN': 'JHN',
    'Hch': 'ACT', 'Hechos': 'ACT', 'HECHOS': 'ACT',
    'Rom': 'ROM', 'Romanos': 'ROM', 'ROMANOS': 'ROM',
    '1 Cor': '1CO', '1 Corintios': '1CO', '1 CORINTIOS': '1CO',
    '2 Cor': '2CO', '2 Corintios': '2CO', '2 CORINTIOS': '2CO',
    'Gal': 'GAL', 'Gálatas': 'GAL', 'GÁLATAS': 'GAL',
    'Ef': 'EPH', 'Efesios': 'EPH', 'EFESIOS': 'EPH',
    'Flp': 'PHP', 'Filipenses': 'PHP', 'FILIPENSES': 'PHP',
    'Col': 'COL', 'Colosenses': 'COL', 'COLOSENSES': 'COL',
    '1 Tes': '1TH', '1 Tesalonicenses': '1TH', '1 TESALONICENSES': '1TH',
    '2 Tes': '2TH', '2 Tesalonicenses': '2TH', '2 TESALONICENSES': '2TH',
    '1 Tim': '1TI', '1 Timoteo': '1TI', '1 TIMOTEO': '1TI',
    '2 Tim': '2TI', '2 Timoteo': '2TI', '2 TIMOTEO': '2TI',
    'Tit': 'TIT', 'Tito': 'TIT', 'TITO': 'TIT',
    'Flm': 'PHM', 'Filemón': 'PHM', 'FILEMÓN': 'PHM',
    'Heb': 'HEB', 'Hebreos': 'HEB', 'HEBREOS': 'HEB',
    'Sant': 'JAS', 'Santiago': 'JAS', 'SANTIAGO': 'JAS',
    '1 Pe': '1PE', '1 Pedro': '1PE', '1 PEDRO': '1PE',
    '2 Pe': '2PE', '2 Pedro': '2PE', '2 PEDRO': '2PE',
    '1 Jn': '1JN', '1 Juan': '1JN', '1 JUAN': '1JN',
    '2 Jn': '2JN', '2 Juan': '2JN', '2 JUAN': '2JN',
    '3 Jn': '3JN', '3 Juan': '3JN', '3 JUAN': '3JN',
    'Jud': 'JUD', 'Judas': 'JUD', 'JUDAS': 'JUD',
    'Ap': 'REV', 'Apocalipsis': 'REV', 'APOCALIPSIS': 'REV',
}

# Orden de libros de la Biblia
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


def extract_text_from_pdf(pdf_path):
    """Extrae todo el texto del PDF"""
    print(f"📖 Abriendo PDF: {pdf_path}")
    all_text_lines = []
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        total_pages = len(pdf_reader.pages)
        print(f"   Total de páginas: {total_pages:,}")
        
        for page_num in range(total_pages):
            if page_num % 100 == 0:
                print(f"   Procesando página {page_num + 1}/{total_pages}...")
            
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            if text:
                lines = text.split('\n')
                all_text_lines.extend(lines)
    
    print(f"✅ Extracción completada: {len(all_text_lines):,} líneas\n")
    return all_text_lines


def detect_book_code(line):
    """Detecta el código de libro bíblico en una línea"""
    for book_name, book_code in BOOK_MAPPING.items():
        # Buscar el nombre del libro al inicio de la línea
        if line.startswith(book_name) or line.startswith(f"{book_name} "):
            return book_code
    return None


def is_title(line):
    """Determina si una línea es un título (texto en mayúsculas o diferente fuente)"""
    # Títulos suelen estar en mayúsculas, tener longitud significativa, y no empezar con número
    if not line or len(line) < 3:
        return False
    
    # Si empieza con número, no es título
    if re.match(r'^\d+\s', line):
        return False
    
    # Si es todo mayúsculas (ignorando espacios y puntuación)
    text_only = re.sub(r'[^A-ZÁÉÍÓÚÑa-záéíóúñ]', '', line)
    if text_only and text_only.isupper():
        return True
    
    # Patrones comunes de títulos
    title_patterns = [
        r'^[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ\s]+$',  # Todo mayúsculas
        r'^\d+\.\s+[A-ZÁÉÍÓÚÑ]',  # Número seguido de mayúscula
        r'^[IVXLCDM]+\.\s+',  # Números romanos
    ]
    
    for pattern in title_patterns:
        if re.match(pattern, line):
            return True
    
    return False


def is_comment_marker(line):
    """Detecta si una línea marca el inicio de un comentario"""
    return 'COMENTARIO' in line.upper()


def is_verse_start(line):
    """Detecta si una línea es el inicio de un versículo"""
    # Los versículos empiezan con un número seguido de espacio
    return bool(re.match(r'^\d+\s+', line))


def parse_navarra_bible(text_lines):
    """
    Parser principal que extrae libros, capítulos, versículos, títulos y comentarios
    """
    print("🔍 Iniciando parsing de la Biblia Navarra...\n")
    
    # Estado del parser
    current_book = None
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    title_buffer = []
    comment_buffer = []
    in_comment_section = False
    
    # Almacenamiento
    all_verses = []
    verse_count = 0
    comment_count = 0
    title_count = 0
    
    # Comenzar a procesar
    processing = False
    
    for i, line in enumerate(text_lines):
        line = line.strip()
        
        if not line:
            continue
        
        # Progreso
        if i % 10000 == 0 and i > 0:
            print(f"   Procesadas {i:,} líneas... ({verse_count} versículos, {comment_count} comentarios)")
        
        # Detectar inicio (Génesis capítulo 1)
        if not processing:
            # Buscar inicio de Génesis
            if detect_book_code(line) == 'GEN' or (re.match(r'^1\s+', line) and 'principio' in line.lower()):
                processing = True
                current_book = 'GEN'
                current_chapter = 1
                current_verse = 1
                verse_buffer = line
                print(f"✓ Inicio encontrado en Génesis: {line[:50]}...\n")
                continue
            else:
                continue
        
        # Detectar cambio de libro
        detected_book = detect_book_code(line)
        if detected_book and detected_book != current_book:
            # Guardar versículo anterior si existe
            if verse_buffer:
                save_verse(all_verses, current_book, current_chapter, current_verse, 
                          verse_buffer, title_buffer, comment_buffer)
                verse_count += 1
                if comment_buffer:
                    comment_count += 1
                if title_buffer:
                    title_count += 1
                verse_buffer = ""
                title_buffer = []
                comment_buffer = []
            
            current_book = detected_book
            current_chapter = 0  # Se incrementará con el primer versículo 1
            print(f"📕 Nuevo libro detectado: {current_book}")
            continue
        
        # Detectar marcador de comentario
        if is_comment_marker(line):
            in_comment_section = True
            continue
        
        # Si estamos en sección de comentarios
        if in_comment_section:
            # Los comentarios se acumulan hasta el próximo versículo o título
            if is_verse_start(line):
                in_comment_section = False
                # El comentario acumulado se asignará al último versículo
                # (ya procesado en el paso anterior)
            else:
                comment_buffer.append(line)
                continue
        
        # Detectar inicio de versículo
        if is_verse_start(line):
            verse_match = re.match(r'^(\d+)\s+(.*)$', line)
            if verse_match:
                new_verse_num = int(verse_match.group(1))
                verse_text = verse_match.group(2)
                
                # Si es versículo 1, es un nuevo capítulo
                if new_verse_num == 1 and current_verse > 1:
                    # Guardar versículo anterior
                    if verse_buffer:
                        save_verse(all_verses, current_book, current_chapter, current_verse,
                                  verse_buffer, title_buffer, comment_buffer)
                        verse_count += 1
                        if comment_buffer:
                            comment_count += 1
                        if title_buffer:
                            title_count += 1
                    
                    current_chapter += 1
                    current_verse = 1
                    verse_buffer = verse_text
                    title_buffer = []
                    comment_buffer = []
                    
                # Si es el versículo siguiente consecutivo
                elif new_verse_num == current_verse + 1 or (current_verse == 0 and new_verse_num == 1):
                    # Guardar versículo anterior
                    if verse_buffer and current_verse > 0:
                        save_verse(all_verses, current_book, current_chapter, current_verse,
                                  verse_buffer, title_buffer, comment_buffer)
                        verse_count += 1
                        if comment_buffer:
                            comment_count += 1
                        if title_buffer:
                            title_count += 1
                    
                    if current_chapter == 0:
                        current_chapter = 1
                    
                    current_verse = new_verse_num
                    verse_buffer = verse_text
                    title_buffer = []
                    comment_buffer = []
                    
                # Si el número no es consecutivo, continuar con el buffer actual
                else:
                    verse_buffer += " " + line
        
        # Detectar título
        elif is_title(line):
            title_buffer.append(line)
        
        # Continuación del versículo actual
        else:
            if verse_buffer:
                verse_buffer += " " + line
            elif title_buffer:
                # Si tenemos títulos acumulados pero no versículo, podría ser más título
                if is_title(line):
                    title_buffer.append(line)
    
    # Guardar último versículo
    if verse_buffer:
        save_verse(all_verses, current_book, current_chapter, current_verse,
                  verse_buffer, title_buffer, comment_buffer)
        verse_count += 1
    
    print(f"\n✅ Parsing completado:")
    print(f"   📊 Total versículos: {verse_count:,}")
    print(f"   💬 Versículos con comentarios: {comment_count:,}")
    print(f"   📌 Versículos con títulos: {title_count:,}")
    
    return all_verses


def save_verse(all_verses, book, chapter, verse, text, titles, comments):
    """Guarda un versículo con sus títulos y comentarios"""
    verse_data = {
        'book': book,
        'chapter': chapter,
        'verse': verse,
        'text': clean_text(text),
    }
    
    if titles:
        verse_data['title'] = ' | '.join(clean_text(t) for t in titles)
    
    if comments:
        verse_data['comment'] = '<br>'.join(clean_text(c) for c in comments)
    
    all_verses.append(verse_data)


def clean_text(text):
    """Limpia el texto eliminando espacios extras y normalizando"""
    # Remover números de versículo al inicio
    text = re.sub(r'^\d+\s+', '', text)
    # Normalizar espacios
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def organize_by_structure(verses):
    """Organiza los versículos por libro > capítulo > versículo"""
    structure = defaultdict(lambda: defaultdict(list))
    
    for verse in verses:
        book = verse['book']
        chapter = verse['chapter']
        structure[book][chapter].append(verse)
    
    return structure


def main():
    print("="*70)
    print("PARSER COMPLETO DE SAGRADA BIBLIA NAVARRA")
    print("="*70)
    print()
    
    # 1. Extraer texto del PDF
    text_lines = extract_text_from_pdf(PDF_FILE)
    
    # 2. Parsear la Biblia
    verses = parse_navarra_bible(text_lines)
    
    # 3. Organizar por estructura
    structure = organize_by_structure(verses)
    
    # 4. Guardar resultado en JSON
    output = {
        'version': 'Sagrada Biblia Navarra',
        'total_verses': len(verses),
        'books': len(structure),
        'data': verses
    }
    
    print(f"\n💾 Guardando en {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("✅ ¡Completado exitosamente!")
    print(f"\n📊 Estadísticas finales:")
    print(f"   Libros procesados: {len(structure)}")
    print(f"   Total versículos: {len(verses):,}")
    
    # Mostrar libros procesados
    print(f"\n📚 Libros encontrados:")
    for book in BIBLE_ORDER:
        if book in structure:
            chapters = len(structure[book])
            total_verses = sum(len(structure[book][ch]) for ch in structure[book])
            print(f"   {book}: {chapters} capítulos, {total_verses} versículos")
    
    print(f"\n✅ Archivo guardado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

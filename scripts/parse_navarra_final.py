#!/usr/bin/env python3
"""
Parser Final para Sagrada Biblia Navarra PDF
Extrae libros, capítulos, versículos, títulos y comentarios completos

Basado en el análisis del formato real del PDF:
- Código de libro (ej: "Gn", "Mt")  
- Títulos en mayúsculas
- Versículos numerados
- Comentarios pueden estar al final de capítulos o intercalados
"""
import PyPDF2
import re
import json
from collections import defaultdict

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_completa_parsed.json"

# Mapeo de códigos bíblicos
BOOK_CODES = {
    # AT
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
    # NT
    'Mt': 'MAT', 'Mc': 'MRK', 'Lc': 'LUK', 'Jn': 'JHN', 'Hch': 'ACT',
    'Rom': 'ROM', '1 Cor': '1CO', '2 Cor': '2CO', 'Gal': 'GAL', 'Ef': 'EPH',
    'Flp': 'PHP', 'Col': 'COL', '1 Tes': '1TH', '2 Tes': '2TH',
    '1 Tim': '1TI', '2 Tim': '2TI', 'Tit': 'TIT', 'Flm': 'PHM',
    'Heb': 'HEB', 'Sant': 'JAS', '1 Pe': '1PE', '2 Pe': '2PE',
    '1 Jn': '1JN', '2 Jn': '2JN', '3 Jn': '3JN', 'Jud': 'JUD', 'Ap': 'REV'
}


def extract_pdf(pdf_path):
    """Extrae todo el texto del PDF"""
    print(f"📖 Opening: {pdf_path}")
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total = len(reader.pages)
        print(f"   Pages: {total:,}")
        
        lines = []
        for i in range(total):
            if i % 500 == 0:
                print(f"   Extracting page {i+1}/{total}...")
            text = reader.pages[i].extract_text()
            if text:
                lines.extend(text.split('\n'))
        
        print(f"✅ Extracted {len(lines):,} lines\n")
        return lines


def is_book_code(line):
    """Check if line is a book code"""
    line_clean = line.strip()
    return line_clean in BOOK_CODES


def is_verse_start(line):
    """Check if line starts with verse number"""
    return bool(re.match(r'^\d+\s+\w', line.strip()))


def is_title(line):
    """Check if line is a title (uppercase, no verse number)"""
    line = line.strip()
    if not line or len(line) < 3:
        return False
    if re.match(r'^\d+\s', line):
        return False
    
    # Check if mostly uppercase
    letters = [c for c in line if c.isalpha()]
    if not letters:
        return False
    uppercase_count = sum(1 for c in letters if c.isupper())
    return uppercase_count / len(letters) > 0.6


def clean_verse_text(text):
    """Clean verse text"""
    # Remove leading verse number
    text = re.sub(r'^\d+\s+', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_bible(lines):
    """Main parser"""
    print("🔍 Parsing Bible content...\n")
    
    verses = []
    current_book = None
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    title_buffer = []
    
    # Stats
    stats = {
        'verses': 0,
        'with_titles': 0,
        'books': set()
    }
    
    # Find Genesis start
    processing = False
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        # Progress
        if i % 25000 == 0 and i > 0:
            print(f"   Line {i:,}/{len(lines):,} - Books: {len(stats['books'])}, Verses: {stats['verses']}")
        
        # Find start (Genesis)
        if not processing:
            if line == 'Gn' or (is_verse_start(line) and 'principio' in line.lower() and 'creó' in line.lower()):
                processing = True
                current_book = 'GEN'
                current_chapter = 1
                current_verse = 1
                if is_verse_start(line):
                    verse_buffer = line
                print(f"✓ Found Genesis start\n")
                continue
            continue
        
        # Check for book code
        if is_book_code(line):
            new_book = BOOK_CODES.get(line)
            if new_book and new_book != current_book:
                # Save current verse
                if verse_buffer:
                    verses.append({
                        'book': current_book,
                        'chapter': current_chapter,
                        'verse': current_verse,
                        'text': clean_verse_text(verse_buffer),
                        'title': ' | '.join(title_buffer) if title_buffer else ''
                    })
                    stats['verses'] += 1
                    if title_buffer:
                        stats['with_titles'] += 1
                    title_buffer = []
                    verse_buffer = ""
                
                current_book = new_book
                current_chapter = 0
                current_verse = 0
                stats['books'].add(new_book)
                print(f"📕 Book: {new_book}")
                continue
        
        # Check for verse start
        if is_verse_start(line):
            match = re.match(r'^(\d+)\s+(.*)$', line)
            if match:
                new_verse = int(match.group(1))
                text = match.group(2)
                
                # New chapter (verse 1)
                if new_verse == 1 and current_verse > 1:
                    # Save previous verse
                    if verse_buffer:
                        verses.append({
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': current_verse,
                            'text': clean_verse_text(verse_buffer),
                            'title': ' | '.join(title_buffer) if title_buffer else ''
                        })
                        stats['verses'] += 1
                        if title_buffer:
                            stats['with_titles'] += 1
                        title_buffer = []
                    
                    current_chapter += 1
                    current_verse = 1
                    verse_buffer = text
                
                # Next consecutive verse
                elif new_verse == current_verse + 1 or (current_verse == 0 and new_verse == 1):
                    # Save previous
                    if verse_buffer and current_verse > 0:
                        verses.append({
                            'book': current_book,
                            'chapter': current_chapter,
                            'verse': current_verse,
                            'text': clean_verse_text(verse_buffer),
                            'title': ' | '.join(title_buffer) if title_buffer else ''
                        })
                        stats['verses'] += 1
                        if title_buffer:
                            stats['with_titles'] += 1
                        title_buffer = []
                    
                    if current_chapter == 0:
                        current_chapter = 1
                    current_verse = new_verse
                    verse_buffer = text
                
                # Continuation
                else:
                    verse_buffer += " " + line
                continue
        
        # Check for title
        if is_title(line):
            title_buffer.append(line)
            continue
        
        # Continuation of current verse
        if verse_buffer:
            verse_buffer += " " + line
    
    # Save last verse
    if verse_buffer:
        verses.append({
            'book': current_book,
            'chapter': current_chapter,
            'verse': current_verse,
            'text': clean_verse_text(verse_buffer),
            'title': ' | '.join(title_buffer) if title_buffer else ''
        })
        stats['verses'] += 1
    
    print(f"\n✅ Parsing complete:")
    print(f"   Books: {len(stats['books'])}")
    print(f"   Verses: {stats['verses']:,}")
    print(f"   With titles: {stats['with_titles']:,}")
    
    return verses, stats


def save_json(verses, stats):
    """Save to JSON"""
    # Group by structure
    structure = defaultdict(lambda: defaultdict(list))
    for v in verses:
        structure[v['book']][v['chapter']].append(v)
    
    output = {
        'version': 'Sagrada Biblia Navarra',
        'source': 'PDF extraction',
        'total_verses': len(verses),
        'total_books': len(stats['books']),
        'verses_with_titles': stats['with_titles'],
        'data': verses
    }
    
    print(f"\n💾 Saving to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    # Book statistics
    print(f"\n📚 Books extracted:")
    for book in sorted(structure.keys()):
        ch_count = len(structure[book])
        v_count = sum(len(structure[book][ch]) for ch in structure[book])
        print(f"   {book:6s}: {ch_count:3d} chapters, {v_count:5d} verses")


def main():
    print("="*70)
    print("NAVARRA BIBLE - FINAL PARSER")
    print("="*70)
    print()
    
    # Extract
    lines = extract_pdf(PDF_FILE)
    
    # Parse
    verses, stats = parse_bible(lines)
    
    # Save
    save_json(verses, stats)
    
    print(f"\n✅ DONE! File: {OUTPUT_JSON}")


if __name__ == "__main__":
    main()

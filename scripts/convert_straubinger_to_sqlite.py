import json
import sys
import os

# Add current directory to path to import convert_to_sqlite
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from convert_to_sqlite import convert_json_to_sqlite

BOOK_MAPPING = {
    "Genesis": "GEN", "Exodus": "EXO", "Leviticus": "LEV", "Numbers": "NUM", "Deuteronomy": "DEU",
    "Joshua": "JOS", "Judges": "JDG", "Ruth": "RUT", "1 Samuel": "1SA", "2 Samuel": "2SA",
    "1 Kings": "1KI", "2 Kings": "2KI", "1 Chronicles": "1CH", "2 Chronicles": "2CH",
    "Ezra": "EZR", "Nehemiah": "NEH", "Esther": "EST", "Job": "JOB", "Psalms": "PSA",
    "Proverbs": "PRO", "Ecclesiastes": "ECC", "Song of Solomon": "SNG", "Isaiah": "ISA",
    "Jeremiah": "JER", "Lamentations": "LAM", "Ezekiel": "EZK", "Daniel": "DAN",
    "Hosea": "HOS", "Joel": "JOL", "Amos": "AMO", "Obadiah": "OBA", "Jonah": "JON",
    "Micah": "MIC", "Nahum": "NAM", "Habakkuk": "HAB", "Zephaniah": "ZEP", "Haggai": "HAG",
    "Zechariah": "ZEC", "Malachi": "MAL",
    "Matthew": "MAT", "Mark": "MRK", "Luke": "LUK", "John": "JHN", "Acts": "ACT",
    "Romans": "ROM", "1 Corinthians": "1CO", "2 Corinthians": "2CO", "Galatians": "GAL",
    "Ephesians": "EPH", "Philippians": "PHP", "Colossians": "COL", "1 Thessalonians": "1TH",
    "2 Thessalonians": "2TH", "1 Timothy": "1TI", "2 Timothy": "2TI", "Titus": "TIT",
    "Philemon": "PHM", "Hebrews": "HEB", "James": "JAS", "1 Peter": "1PE", "2 Peter": "2PE",
    "1 John": "1JN", "2 John": "2JN", "3 John": "3JN", "Jude": "JUD", "Revelation": "REV",
    # Deuterocanonical / Apocrypha
    "Tobit": "TOB", "Judith": "JDT", "Wisdom": "WIS", "Sirach": "SIR", "Baruch": "BAR",
    "1 Maccabees": "1MA", "2 Maccabees": "2MA",
    # Roman numerals
    "I Samuel": "1SA", "II Samuel": "2SA", "I Kings": "1KI", "II Kings": "2KI",
    "I Chronicles": "1CH", "II Chronicles": "2CH",
    "I Corinthians": "1CO", "II Corinthians": "2CO",
    "I Thessalonians": "1TH", "II Thessalonians": "2TH",
    "I Timothy": "1TI", "II Timothy": "2TI",
    "I Peter": "1PE", "II Peter": "2PE",
    "I John": "1JN", "II John": "2JN", "III John": "3JN",
    "Revelation of John": "REV",
    "I Maccabees": "1MA", "II Maccabees": "2MA",
    
    # Spanish names just in case
    "Génesis": "GEN", "Éxodo": "EXO", "Levítico": "LEV", "Números": "NUM", "Deuteronomio": "DEU",
    "Josué": "JOS", "Jueces": "JDG", "Rut": "RUT", "1 Reyes": "1KI", "2 Reyes": "2KI",
    "1 Crónicas": "1CH", "2 Crónicas": "2CH", "Esdras": "EZR", "Nehemías": "NEH", "Tobías": "TOB",
    "Judit": "JDT", "Ester": "EST", "1 Macabeos": "1MA", "2 Macabeos": "2MA", "Salmos": "PSA",
    "Proverbios": "PRO", "Eclesiastés": "ECC", "Cantares": "SNG", "Sabiduría": "WIS",
    "Eclesiástico": "SIR", "Isaías": "ISA", "Jeremías": "JER", "Lamentaciones": "LAM",
    "Ezequiel": "EZK", "Oseas": "HOS", "Amós": "AMO", "Abdías": "OBA", "Jonás": "JON",
    "Miqueas": "MIC", "Nahúm": "NAM", "Habacuc": "HAB", "Sofonías": "ZEP", "Hageo": "HAG",
    "Zacarías": "ZEC", "Malaquías": "MAL", "Mateo": "MAT", "Marcos": "MRK", "Lucas": "LUK",
    "Juan": "JHN", "Hechos": "ACT", "Romanos": "ROM", "1 Corintios": "1CO", "2 Corintios": "2CO",
    "Gálatas": "GAL", "Efesios": "EPH", "Filipenses": "PHP", "Colosenses": "COL",
    "1 Tesalonicenses": "1TH", "2 Tesalonicenses": "2TH", "1 Timoteo": "1TI", "2 Timoteo": "2TI",
    "Filemón": "PHM", "Hebreos": "HEB", "Santiago": "JAS", "1 Pedro": "1PE", "2 Pedro": "2PE",
    "1 Juan": "1JN", "2 Juan": "2JN", "3 Juan": "3JN", "Judas": "JUD", "Apocalipsis": "REV"
}

def process_straubinger(input_path, output_json_path):
    print(f"Reading {input_path}...")
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    formatted_verses = []
    
    # Check structure
    if 'books' not in data:
        print("Error: 'books' key not found in JSON")
        return
        
    for book in data['books']:
        book_name = book.get('name')
        book_id = BOOK_MAPPING.get(book_name)
        
        if not book_id:
            print(f"Warning: Could not map book '{book_name}'")
            continue
            
        for chapter in book.get('chapters', []):
            chapter_num = chapter.get('chapter')
            for verse in chapter.get('verses', []):
                verse_num = verse.get('verse')
                text = verse.get('text')
                
                formatted_verses.append({
                    "book": book_id,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "text": text
                })
                
    print(f"Processed {len(formatted_verses)} verses.")
    
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(formatted_verses, f, ensure_ascii=False, indent=2)
        
    print(f"Saved formatted JSON to {output_json_path}")
    
    # Create SQLite
    convert_json_to_sqlite(output_json_path, "public/bibles/straubinger")

if __name__ == "__main__":
    input_file = "scripts/SpaPlatense.json"
    output_file = "scripts/straubinger_formatted.json"
    
    # Ensure public/bibles exists
    os.makedirs("public/bibles", exist_ok=True)
    
    process_straubinger(input_file, output_file)

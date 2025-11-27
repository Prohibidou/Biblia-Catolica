import bs4
from bs4 import BeautifulSoup
import json
import re
import sys
import os

# Add current directory to path to import convert_to_sqlite
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from convert_to_sqlite import convert_json_to_sqlite

HTML_FILE = "scripts/SagradaBibliaStraubinger.html"
OUTPUT_JSON = "scripts/straubinger_full.json"

BOOK_MAP = {
    'idxGn': 'GEN', 'idxEx': 'EXO', 'idxLv': 'LEV', 'idxNm': 'NUM', 'idxDt': 'DEU',
    'idxJos': 'JOS', 'idxJue': 'JDG', 'idxRut': 'RUT', 'idxUnoRe': '1SA', 'idxDosRe': '2SA',
    'idxTresRe': '1KI', 'idxCuatroRe': '2KI', 'idxUnoPar': '1CH', 'idxDosPar': '2CH',
    'idxEsd': 'EZR', 'idxNeh': 'NEH', 'idxTob': 'TOB', 'idxJdt': 'JDT', 'idxEst': 'EST',
    'idxUnoMac': '1MA', 'idxDosMac': '2MA', 'idxJob': 'JOB', 'idxSal': 'PSA', 'idxProv': 'PRO',
    'idxEcl': 'ECC', 'idxCant': 'SNG', 'idxSab': 'WIS', 'idxEcli': 'SIR', 'idxIs': 'ISA',
    'idxJr': 'JER', 'idxLam': 'LAM', 'idxBar': 'BAR', 'idxEz': 'EZK', 'idxDan': 'DAN',
    'idxOs': 'HOS', 'idxJoel': 'JOL', 'idxAmo': 'AMO', 'idxAbd': 'OBA', 'idxJon': 'JON',
    'idxMiq': 'MIC', 'idxNah': 'NAM', 'idxHab': 'HAB', 'idxSof': 'ZEP', 'idxAg': 'HAG',
    'idxZac': 'ZEC', 'idxMal': 'MAL',
    'idxMateo': 'MAT', 'idxMarcos': 'MRK', 'idxLucas': 'LUK', 'idxJuan': 'JHN',
    'idxHechos': 'ACT', 'idxRomanos': 'ROM', 'idxUnoCor': '1CO', 'idxDosCor': '2CO',
    'idxGalatas': 'GAL', 'idxEfesios': 'EPH', 'idxFilipenses': 'PHP', 'idxColosenses': 'COL',
    'idxUnoTes': '1TH', 'idxDosTes': '2TH', 'idxUnoTimoteo': '1TI', 'idxDosTimoteo': '2TI',
    'idxTito': 'TIT', 'idxFilemon': 'PHM', 'idxHebreos': 'HEB', 'idxSantiago': 'JAS',
    'idxUnoPedro': '1PE', 'idxDosPedro': '2PE', 'idxUnoJuan': '1JN', 'idxDosJuan': '2JN',
    'idxTresJuan': '3JN', 'idxJudas': 'JUD', 'idxApocalipsis': 'REV'
}

def parse_html():
    print(f"Reading {HTML_FILE}...")
    with open(HTML_FILE, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    soup = BeautifulSoup(content, 'html.parser')
    
    # 1. Extract Comments
    print("Extracting comments...")
    comments_map = {}
    footnotes = soup.find_all('p', class_='ftn')
    for p in footnotes:
        # Find anchor with id
        anchor = p.find('a', id=True)
        if anchor:
            c_id = anchor['id']
            # Text is everything after the anchor?
            # Usually format: [1] 1. Text...
            # We want to remove the [1] part.
            text = p.get_text().strip()
            # Remove the [1] marker if present
            text = re.sub(r'^\[\d+\]\s*', '', text)
            comments_map[c_id] = text
            
    print(f"Found {len(comments_map)} comments.")
    
    # 2. Parse Content
    print("Parsing verses...")
    verses = []
    current_book = None
    current_chapter = 0
    
    # Iterate through all elements? Or just headers and paragraphs?
    # It's safer to iterate through all children of body or main container.
    # But finding them linearly is hard with BS4 if they are not siblings.
    # Let's try finding all h4, h6, and p in order.
    
    elements = soup.find_all(['h4', 'h6', 'p'])
    
    for el in elements:
        if el.name == 'h4' or el.name == 'h6':
            # Check for Book ID
            anchor = el.find('a', id=True)
            if anchor and anchor['id'] in BOOK_MAP:
                current_book = BOOK_MAP[anchor['id']]
                current_chapter = 0 # Reset chapter
                print(f"Entered Book: {current_book}")
                continue
                
            # Check for Chapter
            # Usually <h6 id="Gn1" class="Capitulo">... GÉNESIS 1 ...</h6>
            # Also check if it has an ID that ends in digits, even if class is missing?
            # Or if text contains "CAPÍTULO" or Book Name + Number?
            
            is_chapter = False
            if 'Capitulo' in el.get('class', []):
                is_chapter = True
            elif el.get('id') and re.search(r'\d+$', el['id']):
                # Heuristic: if ID ends in number and we are in a book
                # But be careful of other IDs.
                # Usually chapter IDs are like Gn1, Ex1.
                # Let's check if the ID starts with something related to the book?
                # Hard to know the prefix.
                is_chapter = True
                
            if is_chapter:
                text = el.get_text()
                # Try to extract number from text
                match = re.search(r'(\d+)$', text.strip())
                if match:
                    current_chapter = int(match.group(1))
                    print(f"  Chapter {current_chapter} (Text: {text.strip()})")
                else:
                    # Fallback: try to parse ID? e.g. Gn1 -> 1
                    if el.get('id'):
                        id_match = re.search(r'(\d+)$', el['id'])
                        if id_match:
                            current_chapter = int(id_match.group(1))
                            print(f"  Chapter {current_chapter} (ID: {el['id']})")
                            
        elif el.name == 'p':
            if 'ftn' in el.get('class', []):
                continue # Skip footnote definitions
                
            if not current_book or current_chapter == 0:
                continue
                
            # Check if it's a verse
            # Verses usually start with <sup>
            # Handle multiple verses in one paragraph
            # Iterate through contents
            current_verse_num = None
            current_verse_text = ""
            current_verse_comment = None
            
            for content in el.contents:
                if content.name == 'sup':
                    # Save previous verse if exists
                    if current_verse_num is not None:
                        verses.append({
                            "book": current_book,
                            "chapter": current_chapter,
                            "verse": current_verse_num,
                            "text": current_verse_text.strip(),
                            "comment": current_verse_comment
                        })
                    
                    # Start new verse
                    verse_num_str = content.get_text().strip()
                    match = re.match(r'(\d+)', verse_num_str)
                    if match:
                        current_verse_num = int(match.group(1))
                        current_verse_text = ""
                        current_verse_comment = None
                    else:
                        current_verse_num = None # Skip non-verse sups
                        
                elif current_verse_num is not None:
                    # Add content to current verse
                    if content.name == 'a':
                        # Check for comment
                        href = content.get('href')
                        if href and href.startswith('#') and href[1:] in comments_map:
                            c_id = href[1:]
                            if current_verse_comment:
                                current_verse_comment += " " + comments_map[c_id]
                            else:
                                current_verse_comment = comments_map[c_id]
                            continue
                        # Skip [1] markers
                        if content.get_text().strip().startswith('[') and content.get_text().strip().endswith(']'):
                            continue
                            
                    if isinstance(content, bs4.element.NavigableString):
                        current_verse_text += str(content)
                    else:
                        current_verse_text += content.get_text()
            
            # Save last verse in paragraph
            if current_verse_num is not None:
                verses.append({
                    "book": current_book,
                    "chapter": current_chapter,
                    "verse": current_verse_num,
                    "text": current_verse_text.strip(),
                    "comment": current_verse_comment
                })
                    
    print(f"Parsed {len(verses)} verses.")
    
    # Save to JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(verses, f, ensure_ascii=False, indent=2)
        
    # Convert to SQLite
    convert_json_to_sqlite(OUTPUT_JSON, "public/bibles/straubinger")

if __name__ == "__main__":
    parse_html()

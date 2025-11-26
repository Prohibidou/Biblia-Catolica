#!/usr/bin/env python3
"""
Comment Extractor for Sagrada Biblia Navarra
Searches for "COMENTARIO" blocks and extracts references and text.
"""
import PyPDF2
import re
import json

PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_JSON = "scripts/navarra_comments.json"

def extract_comments():
    print(f"📖 Extracting Comments from: {PDF_FILE}")
    
    comments = []
    current_comment = None
    
    with open(PDF_FILE, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        total_pages = len(reader.pages)
        
        # Start searching from where we know there are comments
        # Genesis starts approx at page 3950
        # But we scan everything just in case
        
        for i in range(3000, total_pages):
            if i % 500 == 0: print(f"   Scanning page {i}...")
            
            text = reader.pages[i].extract_text()
            if not text: continue
            
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                # Detect comment start
                if line == "COMENTARIO" or line == "COMENTARIOS":
                    # Save previous if exists
                    if current_comment:
                        comments.append(current_comment)
                    
                    current_comment = {
                        'page': i,
                        'ref_raw': '',
                        'text': []
                    }
                    continue
                
                # If we're inside a comment
                if current_comment:
                    # First line after COMENTARIO is usually the reference
                    if not current_comment['ref_raw']:
                        # Validate if it looks like a reference (has numbers)
                        if any(c.isdigit() for c in line):
                            current_comment['ref_raw'] = line
                        else:
                            # Sometimes there are intermediate lines?
                            pass
                    else:
                        # Accumulate text
                        # Ignore "Volver a..."
                        if "Volver a" in line:
                            continue
                        current_comment['text'].append(line)

    # Save last comment
    if current_comment:
        comments.append(current_comment)
        
    print(f"✅ Extracted {len(comments)} comments")
    
    # Process references
    processed_comments = []
    for c in comments:
        ref = c['ref_raw']
        text = " ".join(c['text']).strip()
        
        # Try to extract book, ch, vs
        # Ex: "Gn 1,1-5", "Mt 21,28-46", "1 Co 7,39-40"
        
        # Separate book from numbers
        # Find first digit
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
            
    print(f"💾 Saving to {OUTPUT_JSON}...")
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(processed_comments, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract_comments()

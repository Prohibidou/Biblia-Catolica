#!/usr/bin/env python3
"""
Merge Text and Comments for Navarra Bible
"""
import json
import re

TEXT_FILE = "scripts/navarra_v4_complete.json"
COMMENTS_FILE = "scripts/navarra_comments.json"
OUTPUT_FILE = "scripts/navarra_final_merged.json"

# Mapeo de códigos de comentarios a códigos de libro estándar
COMMENT_BOOK_MAP = {
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

def parse_range(ref_str):
    """
    Parsea rangos como: "1,1-5", "1,1", "12,1-16,27"
    Devuelve lista de (cap, vers)
    """
    # Simplificación: extraer capítulo inicial y versículo inicial
    # El soporte completo de rangos complejos es difícil sin saber cuántos versículos tiene cada capítulo
    
    try:
        # Formato estándar: Cap,Vers-Vers
        if ',' in ref_str:
            parts = ref_str.split(',')
            chapter = int(parts[0].strip())
            
            verses_part = parts[1].strip()
            if '-' in verses_part:
                v_start = int(verses_part.split('-')[0].strip())
                # v_end = ...
                return chapter, v_start
            else:
                return chapter, int(verses_part)
        else:
            # Solo capítulo?
            return int(ref_str), 1
    except:
        return None, None

def merge():
    print("Cargando textos...")
    with open(TEXT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        verses = data['data']
        
    print("Cargando comentarios...")
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        comments = json.load(f)
        
    # Indexar versículos para búsqueda rápida
    # Key: BOOK_CAP_VERS
    verse_map = {}
    for v in verses:
        key = f"{v['book']}_{v['chapter']}_{v['verse']}"
        verse_map[key] = v
        
    print(f"Procesando {len(comments)} comentarios...")
    matched = 0
    
    for c in comments:
        book_code_raw = c['book_code']
        ref = c['reference']
        text = c['text']
        
        # Mapear libro
        if book_code_raw in COMMENT_BOOK_MAP:
            book = COMMENT_BOOK_MAP[book_code_raw]
            
            # Parsear referencia
            chapter, verse_start = parse_range(ref)
            
            if chapter and verse_start:
                # Asignar al versículo inicial
                key = f"{book}_{chapter}_{verse_start}"
                if key in verse_map:
                    v = verse_map[key]
                    if 'comment' in v:
                        v['comment'] += "<br><br>" + text
                    else:
                        v['comment'] = text
                    matched += 1
                else:
                    # print(f"No encontrado: {key}")
                    pass
            
    print(f"✅ Comentarios asignados: {matched}")
    
    print(f"💾 Guardando {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    merge()

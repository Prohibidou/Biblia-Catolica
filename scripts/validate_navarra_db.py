#!/usr/bin/env python3
"""
Validación completa de la base de datos Navarra
Verifica versículos, capítulos y comentarios por testamento
"""
import sqlite3

DB_FILE = "navarra_complete.sqlite"

# Capítulos esperados por libro (Biblia Católica completa)
EXPECTED_CHAPTERS = {
    # Antiguo Testamento
    'GEN': 50, 'EXO': 40, 'LEV': 27, 'NUM': 36, 'DEU': 34,
    'JOS': 24, 'JDG': 21, 'RUT': 4, '1SA': 31, '2SA': 24,
    '1KI': 22, '2KI': 25, '1CH': 29, '2CH': 36, 'EZR': 10,
    'NEH': 13, 'TOB': 14, 'JDT': 16, 'EST': 10, '1MA': 16,
    '2MA': 15, 'JOB': 42, 'PSA': 150, 'PRO': 31, 'ECC': 12,
    'SNG': 8, 'WIS': 19, 'SIR': 51, 'ISA': 66, 'JER': 52,
    'LAM': 5, 'BAR': 6, 'EZK': 48, 'DAN': 14, 'HOS': 14,
    'JOL': 4, 'AMO': 9, 'OBA': 1, 'JON': 4, 'MIC': 7,
    'NAM': 3, 'HAB': 3, 'ZEP': 3, 'HAG': 2, 'ZEC': 14,
    'MAL': 3,
    # Nuevo Testamento
    'MAT': 28, 'MRK': 16, 'LUK': 24, 'JHN': 21, 'ACT': 28,
    'ROM': 16, '1CO': 16, '2CO': 13, 'GAL': 6, 'EPH': 6,
    'PHP': 4, 'COL': 4, '1TH': 5, '2TH': 3, '1TI': 6,
    '2TI': 4, 'TIT': 3, 'PHM': 1, 'HEB': 13, 'JAS': 5,
    '1PE': 5, '2PE': 3, '1JN': 5, '2JN': 1, '3JN': 1,
    'JUD': 1, 'REV': 22
}

OT_BOOKS = [
    'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA',
    '1KI', '2KI', '1CH', '2CH', 'EZR', 'NEH', 'TOB', 'JDT', 'EST', '1MA',
    '2MA', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG', 'WIS', 'SIR', 'ISA', 'JER',
    'LAM', 'BAR', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC',
    'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL'
]

NT_BOOKS = [
    'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH',
    'PHP', 'COL', '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS',
    '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'
]

def validate():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    print("=" * 70)
    print("VALIDACIÓN DE BASE DE DATOS NAVARRA")
    print("=" * 70)
    
    # Total general
    c.execute("SELECT count(*) FROM verses")
    total = c.fetchone()[0]
    print(f"\n📊 TOTAL GENERAL: {total:,} versículos")
    
    # Comentarios totales
    c.execute("SELECT count(*) FROM verses WHERE comment != ''")
    comments_total = c.fetchone()[0]
    print(f"💬 COMENTARIOS TOTALES: {comments_total:,}")
    
    # Títulos totales
    c.execute("SELECT count(*) FROM verses WHERE title != ''")
    titles_total = c.fetchone()[0]
    print(f"📑 TÍTULOS TOTALES: {titles_total:,}")
    
    print("\n" + "=" * 70)
    print("ANTIGUO TESTAMENTO")
    print("=" * 70)
    
    ot_verses = 0
    ot_comments = 0
    ot_issues = []
    
    for book in OT_BOOKS:
        c.execute("SELECT count(*) FROM verses WHERE book = ?", (book,))
        count = c.fetchone()[0]
        
        c.execute("SELECT count(*) FROM verses WHERE book = ? AND comment != ''", (book,))
        book_comments = c.fetchone()[0]
        
        c.execute("SELECT max(chapter) FROM verses WHERE book = ?", (book,))
        max_chap = c.fetchone()[0]
        
        ot_verses += count
        ot_comments += book_comments
        
        expected = EXPECTED_CHAPTERS.get(book, 0)
        status = "✅" if max_chap == expected else f"⚠️ ({max_chap}/{expected})"
        
        if max_chap != expected:
            ot_issues.append(f"{book}: tiene {max_chap} caps, esperado {expected}")
        
        if count == 0:
            print(f"  ❌ {book:6} - NO ENCONTRADO")
            ot_issues.append(f"{book}: NO ENCONTRADO")
        else:
            print(f"  {status} {book:6} - {count:5} vers, {book_comments:3} coments, {max_chap:3} caps")
    
    print(f"\n📊 TOTAL AT: {ot_verses:,} versículos, {ot_comments:,} comentarios")
    
    print("\n" + "=" * 70)
    print("NUEVO TESTAMENTO")
    print("=" * 70)
    
    nt_verses = 0
    nt_comments = 0
    nt_issues = []
    
    for book in NT_BOOKS:
        c.execute("SELECT count(*) FROM verses WHERE book = ?", (book,))
        count = c.fetchone()[0]
        
        c.execute("SELECT count(*) FROM verses WHERE book = ? AND comment != ''", (book,))
        book_comments = c.fetchone()[0]
        
        c.execute("SELECT max(chapter) FROM verses WHERE book = ?", (book,))
        max_chap = c.fetchone()[0]
        
        nt_verses += count
        nt_comments += book_comments
        
        expected = EXPECTED_CHAPTERS.get(book, 0)
        status = "✅" if max_chap == expected else f"⚠️ ({max_chap}/{expected})"
        
        if max_chap != expected:
            nt_issues.append(f"{book}: tiene {max_chap} caps, esperado {expected}")
        
        if count == 0:
            print(f"  ❌ {book:6} - NO ENCONTRADO")
            nt_issues.append(f"{book}: NO ENCONTRADO")
        else:
            print(f"  {status} {book:6} - {count:5} vers, {book_comments:3} coments, {max_chap:3} caps")
    
    print(f"\n📊 TOTAL NT: {nt_verses:,} versículos, {nt_comments:,} comentarios")
    
    print("\n" + "=" * 70)
    print("RESUMEN DE PROBLEMAS")
    print("=" * 70)
    
    if ot_issues or nt_issues:
        if ot_issues:
            print("\n⚠️  ANTIGUO TESTAMENTO:")
            for issue in ot_issues:
                print(f"    - {issue}")
        
        if nt_issues:
            print("\n⚠️  NUEVO TESTAMENTO:")
            for issue in nt_issues:
                print(f"    - {issue}")
    else:
        print("\n✅ NO SE ENCONTRARON PROBLEMAS")
    
    print("\n" + "=" * 70)
    print("LIBROS SIN COMENTARIOS")
    print("=" * 70)
    
    for book in OT_BOOKS + NT_BOOKS:
        c.execute("SELECT count(*) FROM verses WHERE book = ? AND comment != ''", (book,))
        book_comments = c.fetchone()[0]
        if book_comments == 0:
            print(f"  ⚠️  {book} - Sin comentarios")
    
    conn.close()

if __name__ == "__main__":
    validate()

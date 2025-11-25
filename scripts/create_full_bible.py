import json
import sqlite3
import os
import gzip
import shutil

def create_full_bible():
    print("Creando Biblia Navarra Completa...")
    
    # 1. Cargar AT
    at_path = 'scripts/navarra_at.json'
    verses = []
    
    if os.path.exists(at_path):
        print(f"Cargando AT de {at_path}...")
        with open(at_path, 'r', encoding='utf-8') as f:
            at_verses = json.load(f)
            print(f"  {len(at_verses)} versículos del AT cargados.")
            verses.extend(at_verses)
    else:
        print("⚠️ ADVERTENCIA: No se encontró navarra_at.json")
    
    # 2. Cargar NT (Merged)
    nt_path = 'scripts/navarra_nt_merged.json'
    if os.path.exists(nt_path):
        print(f"Cargando NT de {nt_path}...")
        with open(nt_path, 'r', encoding='utf-8') as f:
            nt_verses = json.load(f)
            print(f"  {len(nt_verses)} versículos del NT cargados.")
            
            # Adaptar formato: section_title -> comment
            for v in nt_verses:
                if 'section_title' in v and v['section_title']:
                    v['comment'] = f"<strong>{v['section_title']}</strong>"
                    del v['section_title']
            
            verses.extend(nt_verses)
    else:
        print("❌ ERROR: No se encontró navarra_nt_merged.json")
        return

    print(f"Total versículos combinados: {len(verses)}")
    
    # 3. Crear SQLite
    db_path = 'navarra_complete.sqlite'
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE verses (
            book TEXT,
            chapter INTEGER,
            verse INTEGER,
            text TEXT,
            comment TEXT,
            PRIMARY KEY (book, chapter, verse)
        )
    ''')
    
    c.execute('CREATE INDEX idx_book_chapter ON verses (book, chapter)')
    
    print("Insertando versículos en SQLite...")
    count = 0
    for v in verses:
        try:
            c.execute('INSERT OR REPLACE INTO verses (book, chapter, verse, text, comment) VALUES (?, ?, ?, ?, ?)',
                      (v['book'], v['chapter'], v['verse'], v['text'], v.get('comment')))
            count += 1
        except Exception as e:
            print(f"Error insertando {v.get('book')} {v.get('chapter')}:{v.get('verse')}: {e}")
            
    conn.commit()
    conn.close()
    
    print(f"✓ Base de datos creada con {count} versículos.")
    
    # 4. Comprimir
    gz_path = 'public/bibles/navarra.sqlite.gz'
    print(f"Comprimiendo a {gz_path}...")
    
    with open(db_path, 'rb') as f_in:
        with gzip.open(gz_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    print("✓ Archivo comprimido listo.")
    
    # Actualizar registro
    size_bytes = os.path.getsize(gz_path)
    print(f"Tamaño final: {size_bytes / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    create_full_bible()

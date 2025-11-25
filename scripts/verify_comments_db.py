import sqlite3
import gzip
import shutil
import os

# Descomprimir el archivo
gz_path = 'public/bibles/navarra.sqlite.gz'
temp_db = 'temp_check.sqlite'

print("Descomprimiendo base de datos...")
with gzip.open(gz_path, 'rb') as f_in:
    with open(temp_db, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

# Conectar y verificar
conn = sqlite3.connect(temp_db)
c = conn.cursor()

# Contar versículos con comentarios
c.execute("SELECT COUNT(*) FROM verses WHERE comment IS NOT NULL AND comment != ''")
count_with_comments = c.fetchone()[0]

c.execute("SELECT COUNT(*) FROM verses")
total_verses = c.fetchone()[0]

print(f"\nTotal versículos: {total_verses}")
print(f"Versículos con comentarios: {count_with_comments}")
print(f"Porcentaje: {count_with_comments/total_verses*100:.1f}%")

# Mostrar ejemplos del NT
print("\n--- Ejemplos de comentarios en Mateo ---")
c.execute("""
    SELECT chapter, verse, text, comment 
    FROM verses 
    WHERE book='MAT' AND comment IS NOT NULL 
    LIMIT 5
""")

for row in c.fetchall():
    chapter, verse, text, comment = row
    print(f"\nMateo {chapter}:{verse}")
    print(f"  Texto: {text[:80]}...")
    print(f"  Comentario: {comment[:150]}...")

conn.close()
os.remove(temp_db)
print("\n✓ Verificación completada")

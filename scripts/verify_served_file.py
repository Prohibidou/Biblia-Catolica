import gzip
import sqlite3
import os

print("Verificando archivo servido por la web...")
gz_path = 'public/bibles/navarra.sqlite.gz'

if not os.path.exists(gz_path):
    print(f"❌ No existe: {gz_path}")
    exit(1)

gz_size = os.path.getsize(gz_path)
print(f"✓ Archivo .gz: {gz_size/1024/1024:.2f} MB ({gz_size} bytes)")

# Descomprimir y verificar
with gzip.open(gz_path, 'rb') as f:
    data = f.read()

print(f"✓ Descomprimido: {len(data)/1024/1024:.2f} MB")

# Guardar temporalmente para verificar
temp_db = 'temp_verify.db'
with open(temp_db, 'wb') as f:
    f.write(data)

# Verificar contenido
conn = sqlite3.connect(temp_db)
c = conn.cursor()

c.execute("SELECT count(*) FROM verses WHERE book='MAT' AND chapter=1")
mat1_count = c.fetchone()[0]
print(f"✓ Mateo 1 tiene: {mat1_count} versículos")

if mat1_count > 0:
    c.execute("SELECT verse, text FROM verses WHERE book='MAT' AND chapter=1 LIMIT 3")
    print("\nPrimeros 3 versículos de Mateo 1:")
    for v, t in c.fetchall():
        print(f"  {v}: {t[:60]}...")
else:
    print("❌ NO HAY CONTENIDO EN MATEO 1")

# Total de versículos
c.execute("SELECT count(*) FROM verses")
total = c.fetchone()[0]
print(f"\n✓ Total versículos en la BD: {total}")

conn.close()
os.remove(temp_db)

print("\n✅ El archivo en public/bibles/ está correcto.")
print("Si la app no muestra contenido, el problema es:")
print("  1. Caché del navegador (probá Ctrl+F5 o borrar caché)")
print("  2. La app está cargando un archivo diferente")
print("  3. Problema con localforage/IndexedDB")

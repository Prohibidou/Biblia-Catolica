import sqlite3
import os

db_path = 'navarra_complete.sqlite'
if not os.path.exists(db_path):
    print(f"No se encuentra {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Verificar Mateo 1
print("Verificando Mateo 1...")
c.execute('SELECT count(*) FROM verses WHERE book="MAT" AND chapter=1')
count = c.fetchone()[0]
print(f"Total versículos en Mateo 1: {count}")

if count > 0:
    print("\nMuestra de versículos:")
    c.execute('SELECT verse, text, comment FROM verses WHERE book="MAT" AND chapter=1 ORDER BY verse LIMIT 5')
    for r in c.fetchall():
        print(f"  {r[0]}: {r[1][:50]}... [Comentario: {r[2]}]")
else:
    print("❌ NO HAY VERSÍCULOS EN MATEO 1")
    
    # Verificar si hay algo de Mateo
    c.execute('SELECT chapter, count(*) FROM verses WHERE book="MAT" GROUP BY chapter')
    print("\nCapítulos en Mateo:")
    for r in c.fetchall():
        print(f"  Cap {r[0]}: {r[1]} versículos")

conn.close()

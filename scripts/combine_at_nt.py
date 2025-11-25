import json

# Cargar AT (sin comentarios)
with open('scripts/navarra_at.json', 'r', encoding='utf-8') as f:
    at_data = json.load(f)

# Cargar NT (con comentarios)
with open('scripts/full_bible_final.json', 'r', encoding='utf-8') as f:
    bible_data = json.load(f)

# Separar AT y NT del archivo actual
nt_books = {'MAT', 'MRK', 'LUK', 'JHN', 'ACT', 'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', 
            '1TH', '2TH', '1TI', '2TI', 'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV'}

# Extraer solo NT del archivo actual (tiene algunos comentarios)
nt_current = [v for v in bible_data if v['book'] in nt_books]

# Combinar: AT nuevo + NT con comentarios
combined = at_data + nt_current

print(f"AT (nuevo): {len(at_data)} versículos")
print(f"NT (con comentarios): {len(nt_current)} versículos")
print(f"Total combinado: {len(combined)} versículos")

# Estadísticas de comentarios
at_with_comments = len([v for v in at_data if v.get('comment')])
nt_with_comments = len([v for v in nt_current if v.get('comment')])

print(f"\nComentarios:")
print(f"  AT: {at_with_comments} versículos con comentarios")
print(f"  NT: {nt_with_comments} versículos con comentarios")

# Guardar
output_file = 'scripts/biblia_navarra_completa.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f"\n✓ Guardado en: {output_file}")

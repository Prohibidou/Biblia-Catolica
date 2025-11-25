import json

# Cargar datos anteriores
with open('scripts/navarra_nt_final.json', encoding='utf-8') as f:
    old_verses = json.load(f)

# Cargar nuevos evangelios
with open('scripts/gospels_extracted.json', encoding='utf-8') as f:
    new_verses = json.load(f)

# Crear diccionario para acceso rápido
merged_dict = {}

# Primero cargar los viejos (base)
for v in old_verses:
    key = f"{v['book']}_{v['chapter']}_{v['verse']}"
    merged_dict[key] = v

# Luego mezclar los nuevos
added_count = 0
updated_count = 0

for v in new_verses:
    key = f"{v['book']}_{v['chapter']}_{v['verse']}"
    
    if key not in merged_dict:
        # Nuevo versículo que faltaba
        merged_dict[key] = v
        added_count += 1
    else:
        # Versículo existente. ¿Reemplazamos?
        # El nuevo viene del TXT full, el viejo del DOC.
        # El TXT full parece tener mejor texto en general, pero el DOC tenía mejor estructura de párrafos.
        # Vamos a conservar el viejo si existe, y solo añadir lo que falta.
        # Opcional: Si el viejo es muy corto y el nuevo largo, reemplazar.
        old_text = merged_dict[key]['text']
        new_text = v['text']
        
        if len(new_text) > len(old_text) + 10:
            merged_dict[key] = v
            updated_count += 1

# Convertir a lista
final_verses = list(merged_dict.values())

# Ordenar
def sort_key(v):
    book_order = {
        'MAT': 1, 'MRK': 2, 'LUK': 3, 'JHN': 4, 'ACT': 5, 'ROM': 6, '1CO': 7, '2CO': 8,
        'GAL': 9, 'EPH': 10, 'PHP': 11, 'COL': 12, '1TH': 13, '2TH': 14, '1TI': 15,
        '2TI': 16, 'TIT': 17, 'PHM': 18, 'HEB': 19, 'JAS': 20, '1PE': 21, '2PE': 22,
        '1JN': 23, '2JN': 24, '3JN': 25, 'JUD': 26, 'REV': 27
    }
    return (book_order.get(v['book'], 99), v['chapter'], v['verse'])

final_verses.sort(key=sort_key)

print(f"Versículos anteriores: {len(old_verses)}")
print(f"Nuevos versículos extraídos: {len(new_verses)}")
print(f"Versículos añadidos: {added_count}")
print(f"Versículos actualizados: {updated_count}")
print(f"Total final NT: {len(final_verses)}")

with open('scripts/navarra_nt_merged.json', 'w', encoding='utf-8') as f:
    json.dump(final_verses, f, ensure_ascii=False, indent=2)

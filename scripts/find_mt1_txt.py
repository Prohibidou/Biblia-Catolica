# Buscar inicio real de Mateo 1:1
with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

print("Buscando 'Libro de la genealogía' o 'Genealogía de Jesucristo'...\n")

for i in range(len(lines)):
    line = lines[i].strip()
    # Buscar inicio típico de Mateo
    if "Libro de la genealogía de Jesucristo" in line or ("Genealogía de Jesucristo" in line and "hijo de David" in lines[i+1]):
        print(f"✓ Encontrado en línea {i}")
        # Mostrar contexto amplio
        for j in range(i, min(i+100, len(lines))):
            print(f"{j}: {lines[j].strip()}")
        break

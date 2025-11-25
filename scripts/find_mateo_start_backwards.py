# Buscar inicio exacto de Mateo
with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

start_search = 135471
print(f"Buscando inicio de Mateo hacia atrás desde {start_search}...\n")

for i in range(start_search, start_search - 2000, -1):
    line = lines[i].strip()
    if "Libro de la" in line or "Genealogía" in line or "Abraham" in line or "1" == line:
        print(f"{i}: {line}")
        # Mostrar contexto
        for j in range(i, i+10):
            print(f"  {j}: {lines[j].strip()}")
        
        # Si encontramos algo muy prometedor, paramos
        if "Libro de la genealogía" in line or "Genealogía de Jesucristo" in line:
            break

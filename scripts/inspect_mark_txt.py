# Ver contexto de Marcos 1:1
with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

start_line = 139348
print(f"--- CONTEXTO MARCOS (Línea {start_line}) ---")
for i in range(start_line - 20, start_line + 50):
    print(f"{i}: {lines[i].strip()}")

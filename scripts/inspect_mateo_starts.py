# Inspeccionar posibles inicios de Mateo
with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

print("--- CONTEXTO 54310 ---")
for i in range(54310, 54360):
    print(f"{i}: {lines[i].strip()}")

print("\n--- CONTEXTO 163540 ---")
for i in range(163540, 163600):
    print(f"{i}: {lines[i].strip()}")

# Analizar el archivo descargado
with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total líneas: {len(lines)}")

print("\n--- PRIMERAS 50 LÍNEAS ---")
for i in range(50):
    print(f"{i}: {lines[i].strip()}")

print("\n--- BUSCANDO 'MATEO' ---")
for i in range(len(lines)):
    if "EVANGELIO SEGÚN SAN MATEO" in lines[i].upper() or "EVANGELIO DE MATEO" in lines[i].upper():
        print(f"Encontrado en línea {i}: {lines[i].strip()}")
        # Mostrar contexto
        for j in range(i, min(i+50, len(lines))):
            print(f"{j}: {lines[j].strip()}")
        break

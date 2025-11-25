import requests
import os

url = "https://archive.org/download/sagrada-biblia-navarra/Sagrada%20Biblia%20Navarra_djvu.txt"
output_file = "scripts/Sagrada_Biblia_Navarra_full.txt"

if not os.path.exists(output_file):
    print(f"Descargando {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✓ Descarga completada.")
    else:
        print("❌ Error en descarga.")
else:
    print("✓ El archivo ya existe.")

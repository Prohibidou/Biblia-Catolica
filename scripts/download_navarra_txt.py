import requests

url = "https://archive.org/download/sagrada-biblia-navarra/Sagrada%20Biblia%20Navarra_djvu.txt"
output_path = "scripts/Sagrada_Biblia_Navarra_full.txt"

print(f"Descargando {url}...")
try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            
    print(f"✓ Descarga completada: {output_path}")
except Exception as e:
    print(f"❌ Error en la descarga: {e}")

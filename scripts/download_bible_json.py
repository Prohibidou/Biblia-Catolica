import requests
import json

# Intentar estructura correcta del repositorio
possible_urls = [
    "https://raw.githubusercontent.com/MaatheusGois/bible/main/json/rv1960.json",
    "https://raw.githubusercontent.com/MaatheusGois/bible/main/json/es.json",
    "https://raw.githubusercontent.com/MaatheusGois/bible/main/json/spanish.json",
    "https://raw.githubusercontent.com/MaatheusGois/bible/master/json/rv1960.json"
]

for url in possible_urls:
    print(f"Intentando: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"  ✓ ¡Encontrado!")
            
            bible_data = response.json()
            
            output_file = "scripts/bible_rv1960_full.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(bible_data, f, ensure_ascii=False, indent=2)
            
            # Contar versículos
            if isinstance(bible_data, list):
                total = len(bible_data)
            else:
                total = "desconocido"
            
            print(f"  Guardado en: {output_file}")
            print(f"  Versículos/entries: {total}")
            break
        else:
            print(f"  ❌ {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
else:
    print("\nNo se pudo descargar. Intentando con otro repositorio...")
    # Usar alejandroch1202/biblia-api
    url = "https://biblia-api.vercel.app/api/books/all"
    print(f"Intentando API: {url}")
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        print("✓ API funcionó, procesando datos...")
        bible_data = response.json()
        
        output_file = "scripts/bible_rv1960_full.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(bible_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Guardado en: {output_file}")

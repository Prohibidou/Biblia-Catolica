import re

# Buscar el patrón del NT en el archivo extraído
with open('scripts/nt_pdf_full_extract.txt', encoding='utf-8') as f:
    lines = f.readlines()

print("Buscando inicio del texto de Mateo (no comentarios)...\n")

# Buscar "Mt" seguido de número de capítulo y versículo
# Patrón: línea que contiene solo "Mt" o "Mateo", seguida de líneas de versículos
for i in range(len(lines)):
    line = lines[i].strip()
    
    # Buscar líneas que parezcan inicio de Evangelio
    if line in ['Mt', 'Mateo', 'MATEO', 'Mc', 'Marcos', 'MARCOS']:
        print(f"✓ Encontrado '{line}' en línea {i}")
        # Mostrar contexto
        context_start = max(0, i-5)
        context_end = min(len(lines), i+20)
        
        print(f"\n--- CONTEXTO (líneas {context_start}-{context_end}) ---")
        for j in range(context_start, context_end):
            print(f"{j}: {lines[j].rstrip()[:100]}")
        
        # Solo mostrar el primer match
        break

print("\n\nBuscando patrón de versículo numérico...")
# Buscar números seguidos de texto (patrón de versículo)
verse_pattern_count = 0
for i in range(1000, min(2000, len(lines))):
    line = lines[i].strip()
    # Si la línea es solo un número de 1-2 dígitos
    if re.match(r'^\d{1,2}$', line) and i+1 < len(lines):
        next_line = lines[i+1].strip()
        # Y la siguiente línea tiene texto sustancial
        if len(next_line) > 20 and not next_line.startswith('COMENTARIO'):
            verse_pattern_count += 1
            if verse_pattern_count <= 3:
                print(f"\nVersículo potencial en línea {i}:")
                print(f"  Número: {line}")
                print(f"  Texto: {next_line[:80]}...")

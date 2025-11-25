# Extraer texto crudo de los evangelios
ranges = {
    'MAT': (135424, 139348),
    'MRK': (139348, 142103),
    'LUK': (142103, 146187),
    'JHN': (146187, 149265)
}

with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

for book, (start, end) in ranges.items():
    content = "".join(lines[start:end])
    filename = f'scripts/raw_{book}.txt'
    with open(filename, 'w', encoding='utf-8') as f_out:
        f_out.write(content)
    print(f"✓ {book} extraído a {filename} ({end-start} líneas)")

import json

# Estructura canónica del NT (libro: {capítulo: versículos})
NT_STRUCTURE = {
    'MAT': {1:25, 2:23, 3:17, 4:25, 5:48, 6:34, 7:29, 8:34, 9:38, 10:42, 11:30, 12:50, 13:58, 14:36, 15:39, 16:28, 17:27, 18:35, 19:30, 20:34, 21:46, 22:46, 23:39, 24:51, 25:46, 26:75, 27:66, 28:20},
    'MRK': {1:45, 2:28, 3:35, 4:41, 5:43, 6:56, 7:37, 8:38, 9:50, 10:52, 11:33, 12:44, 13:37, 14:72, 15:47, 16:20},
    'LUK': {1:80, 2:52, 3:38, 4:44, 5:39, 6:49, 7:50, 8:56, 9:62, 10:42, 11:54, 12:59, 13:35, 14:35, 15:32, 16:31, 17:37, 18:43, 19:48, 20:47, 21:38, 22:71, 23:56, 24:53},
    'JHN': {1:51, 2:25, 3:36, 4:54, 5:47, 6:71, 7:53, 8:59, 9:41, 10:42, 11:57, 12:50, 13:38, 14:31, 15:27, 16:33, 17:26, 18:40, 19:42, 20:31, 21:25},
    'ACT': {1:26, 2:47, 3:26, 4:37, 5:42, 6:15, 7:60, 8:40, 9:43, 10:48, 11:30, 12:25, 13:52, 14:28, 15:41, 16:40, 17:34, 18:28, 19:41, 20:38, 21:40, 22:30, 23:35, 24:27, 25:27, 26:32, 27:44, 28:31},
    'ROM': {1:32, 2:29, 3:31, 4:25, 5:21, 6:23, 7:25, 8:39, 9:33, 10:21, 11:36, 12:21, 13:14, 14:23, 15:33, 16:27},
    '1CO': {1:31, 2:16, 3:23, 4:21, 5:13, 6:20, 7:40, 8:13, 9:27, 10:33, 11:34, 12:31, 13:13, 14:40, 15:58, 16:24},
    '2CO': {1:24, 2:17, 3:18, 4:18, 5:21, 6:18, 7:16, 8:24, 9:15, 10:18, 11:33, 12:21, 13:14},
    'GAL': {1:24, 2:21, 3:29, 4:31, 5:26, 6:18},
    'EPH': {1:23, 2:22, 3:21, 4:32, 5:33, 6:24},
    'PHP': {1:30, 2:30, 3:21, 4:23},
    'COL': {1:29, 2:23, 3:25, 4:18},
    '1TH': {1:10, 2:20, 3:13, 4:18, 5:28},
    '2TH': {1:12, 2:17, 3:18},
    '1TI': {1:20, 2:15, 3:16, 4:16, 5:25, 6:21},
    '2TI': {1:18, 2:26, 3:17, 4:22},
    'TIT': {1:16, 2:15, 3:15},
    'PHM': {1:25},
    'HEB': {1:14, 2:18, 3:19, 4:16, 5:14, 6:20, 7:28, 8:13, 9:28, 10:39, 11:40, 12:29, 13:25},
    'JAS': {1:27, 2:26, 3:18, 4:17, 5:20},
    '1PE': {1:25, 2:25, 3:22, 4:19, 5:14},
    '2PE': {1:21, 2:22, 3:18},
    '1JN': {1:10, 2:29, 3:24, 4:21, 5:21},
    '2JN': {1:13},
    '3JN': {1:14},
    'JUD': {1:25},
    'REV': {1:20, 2:29, 3:22, 4:11, 5:14, 6:17, 7:17, 8:13, 9:21, 10:11, 11:19, 12:18, 13:18, 14:20, 15:8, 16:21, 17:18, 18:24, 19:21, 20:15, 21:27, 22:21}
}

# Cargar versículos actuales
with open('scripts/navarra_nt_final.json', encoding='utf-8') as f:
    current = json.load(f)

# Organizar por libro/capítulo/versículo
existing = {}
for v in current:
    book = v['book']
    chap = v['chapter']
    verse = v['verse']
    
    if book not in existing:
        existing[book] = {}
    if chap not in existing[book]:
        existing[book][chap] = set()
    
    existing[book][chap].add(verse)

# Encontrar faltantes
missing = []
total_missing = 0

print("📊 VERSÍCULOS FALTANTES POR LIBRO:\n")

for book, chapters in sorted(NT_STRUCTURE.items()):
    book_missing = 0
    
    for chap, max_verse in chapters.items():
        if book not in existing or chap not in existing[book]:
            # Falta el capítulo completo
            for v in range(1, max_verse + 1):
                missing.append({'book': book, 'chapter': chap, 'verse': v})
                book_missing += 1
        else:
            # Verificar versículos individuales
            for v in range(1, max_verse + 1):
                if v not in existing[book][chap]:
                    missing.append({'book': book, 'chapter': chap, 'verse': v})
                    book_missing += 1
    
    if book_missing > 0:
        total_missing += book_missing  
        print(f"  {book}: {book_missing} versículos faltantes")

print(f"\n✅ TOTAL FALTANTES: {total_missing} versículos")

# Guardar lista de faltantes
with open('scripts/nt_missing_verses.json', 'w', encoding='utf-8') as f:
    json.dump(missing, f, indent=2)

print(f"✅ Lista guardada en scripts/nt_missing_verses.json")

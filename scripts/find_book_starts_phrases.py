# Buscar frases clave de inicio de libros
phrases = {
    'MATEO': ["Libro de la genealogía", "Genealogía de Jesucristo", "Abraham engendró a Isaac"],
    'MARCOS': ["Comienzo del Evangelio de Jesucristo", "Principio del Evangelio de Jesucristo"],
    'LUCAS': ["Puesto que muchos han intentado", "Muchos han emprendido", "Teófilo"],
    'JUAN': ["En el principio existía el Verbo", "En el principio era el Verbo", "En el principio existía la Palabra"],
    'HECHOS': ["El primer libro", "En mi primer libro", "Teófilo"],
    'ROMANOS': ["Pablo, siervo de Cristo", "Pablo, llamado a ser apóstol"],
    '1 CORINTIOS': ["Pablo, llamado a ser apóstol de Jesucristo por la voluntad de Dios", "a la iglesia de Dios que está en Corinto"],
    'GALATAS': ["Pablo, apóstol, no de parte de hombres"],
    'EFESIOS': ["Pablo, apóstol de Cristo Jesús por voluntad de Dios"],
    'FILIPENSES': ["Pablo y Timoteo, siervos de Cristo Jesús"],
    'COLOSENSES': ["Pablo, apóstol de Cristo Jesús por voluntad de Dios"],
    '1 TESALONICENSES': ["Pablo, Silvano y Timoteo"],
    '2 TESALONICENSES': ["Pablo, Silvano y Timoteo"],
    '1 TIMOTEO': ["Pablo, apóstol de Cristo Jesús por mandato"],
    '2 TIMOTEO': ["Pablo, apóstol de Cristo Jesús por voluntad de Dios"],
    'TITO': ["Pablo, siervo de Dios y apóstol de Jesucristo"],
    'FILEMON': ["Pablo, prisionero de Cristo Jesús"],
    'HEBREOS': ["Muchas veces y de muchas maneras habló Dios"],
    'SANTIAGO': ["Santiago, siervo de Dios y del Señor Jesucristo"],
    '1 PEDRO': ["Pedro, apóstol de Jesucristo"],
    '2 PEDRO': ["Simeón Pedro, siervo y apóstol"],
    '1 JUAN': ["Lo que existía desde el principio"],
    '2 JUAN': ["El Presbítero a la Señora elegida"],
    '3 JUAN': ["El Presbítero al querido Gayo"],
    'JUDAS': ["Judas, siervo de Jesucristo"],
    'APOCALIPSIS': ["Revelación de Jesucristo"]
}

with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

print("Buscando frases de inicio...\n")

for book, search_phrases in phrases.items():
    found = False
    for phrase in search_phrases:
        for i in range(len(lines)):
            if phrase.upper() in lines[i].upper():
                # Verificar contexto (que no sea un índice o comentario lejano)
                # Para simplificar, aceptamos la primera ocurrencia que parezca texto
                # Evitar líneas muy cortas que podrían ser índices
                if len(lines[i]) > 20:
                    print(f"✓ {book}: '{phrase}' en línea {i}")
                    print(f"   Contexto: {lines[i].strip()[:50]}...")
                    found = True
                    break
        if found: break
    
    if not found:
        print(f"❌ {book}: No encontrado")

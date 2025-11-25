# Buscar inicios de libros del NT
books = [
    "EVANGELIO SEGÚN SAN MATEO", "EVANGELIO SEGÚN SAN MARCOS", "EVANGELIO SEGÚN SAN LUCAS", "EVANGELIO SEGÚN SAN JUAN",
    "HECHOS DE LOS APÓSTOLES", "CARTA A LOS ROMANOS", "PRIMERA CARTA A LOS CORINTIOS", "SEGUNDA CARTA A LOS CORINTIOS",
    "CARTA A LOS GÁLATAS", "CARTA A LOS EFESIOS", "CARTA A LOS FILIPENSES", "CARTA A LOS COLOSENSES",
    "PRIMERA CARTA A LOS TESALONICENSES", "SEGUNDA CARTA A LOS TESALONICENSES",
    "PRIMERA CARTA A TIMOTEO", "SEGUNDA CARTA A TIMOTEO", "CARTA A TITO", "CARTA A FILEMÓN",
    "CARTA A LOS HEBREOS", "CARTA DE SANTIAGO", "PRIMERA CARTA DE SAN PEDRO", "SEGUNDA CARTA DE SAN PEDRO",
    "PRIMERA CARTA DE SAN JUAN", "SEGUNDA CARTA DE SAN JUAN", "TERCERA CARTA DE SAN JUAN",
    "CARTA DE SAN JUDAS", "APOCALIPSIS"
]

with open('scripts/Sagrada_Biblia_Navarra_full.txt', encoding='utf-8') as f:
    lines = f.readlines()

print("Buscando inicios de libros...\n")

found_books = {}

for i in range(len(lines)):
    line = lines[i].strip().upper()
    # Limpieza básica de la línea para matching
    clean_line = line.replace("  ", " ").replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Á", "A").replace("É", "E")
    
    for book in books:
        clean_book = book.replace("Í", "I").replace("Ó", "O").replace("Ú", "U").replace("Á", "A").replace("É", "E")
        
        if clean_book in clean_line and len(line) < 100:
            # Verificar que no sea un título en el índice o referencia
            # Mirar líneas siguientes para confirmar contenido
            is_real_start = False
            for j in range(1, 20):
                if i+j < len(lines) and ("CAPITULO" in lines[i+j].upper() or "INTRODUCCION" in lines[i+j].upper() or "1" in lines[i+j]):
                    is_real_start = True
                    break
            
            if is_real_start:
                if book not in found_books:
                    found_books[book] = i
                    print(f"✓ {book} en línea {i}")

# Imprimir resultados ordenados
print("\n--- RESUMEN ---")
sorted_books = sorted(found_books.items(), key=lambda x: x[1])
for book, line in sorted_books:
    print(f"{book}: {line}")

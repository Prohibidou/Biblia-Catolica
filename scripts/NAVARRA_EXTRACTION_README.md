# Extracción de Sagrada Biblia Navarra - Resumen

## Objetivo
Extraer **capítulos, versículos, títulos y comentarios** de toda la Biblia (AT y NT) del PDF "Sagrada Biblia Navarra.pdf".

## Formato del PDF Detectado

Basado en el análisis del PDF real:

```
1
Gn
PRIMERA PARTE:
CREACIÓN Y PRIMERA ETAPA
DE LA HUMANIDAD
I. ORÍGENES DEL CIELO Y DE LA TIERRA
Relato de la creación
1
En el principio creó Dios el cielo y la tierra.
2
La tierra era caos y vacío...
3
Dijo Dios:
—Haya luz.
```

### Estructura identificada:
1. **Número de página** (ej: "1")
2. **Código de libro** (ej: "Gn", "Mt", "Jn")
3. **Títulos de sección** (en MAYÚSCULAS o fuente diferente)
4. **Versículos numerados** (ej: "1", "2", "3")
5. **Texto del versículo** (puede continuar en varias líneas)

### Características:
- **Títulos**: Texto en mayúsculas (>60% letras mayúsculas)
- **Versículos**: Comienzan con número seguido de espacio
- **Comentarios**: Mencionados pero no encontrados en las primeras 500 páginas con el marcador "COMENTARIO"
  - Los comentarios pueden estar integrados de otra forma o en secciones específicas

## Scripts Creados

### 1. `parse_navarra_complete.py`
Parser inicial completo que detecta:
- Libros bíblicos
- Capítulos (cuando aparece versículo 1)
- Versículos consecutivos
- Títulos (texto en mayúsculas)
- Comentarios (secciones marcadas con "COMENTARIO")

**Resultado**: Extrajo 1,079 versículos (incompleto)

### 2. `parse_navarra_optimized.py`
Parser optimizado con:
- Mejor detección de comentarios al final de secciones
- Asociación de comentarios con versículos específicos
- Manejo mejorado de títulos

### 3. `parse_navarra_final.py` ⭐ **RECOMENDADO**
Parser final basado en análisis real del PDF:
- Extracción eficiente línea por línea
- Detección precisa de códigos de libros
- Identificación de títulos por porcentaje de mayúsculas
- Manejo robusto de versículos consecutivos
- Detección de nuevos capítulos

**Actualmente en ejecución** - Procesando 10,513 páginas

## Archivo PDF

- **Ubicación**: `BibliaPDF/Sagrada Biblia Navarra.pdf`
- **Tamaño**: 34,732,005 bytes (~33 MB)
- **Total de páginas**: 10,513

## Archivos de Salida

Los parsers generan archivos JSON con la siguiente estructura:

```json
{
  "version": "Sagrada Biblia Navarra",
  "total_verses": 31000,
  "total_books": 73,
  "data": [
    {
      "book": "GEN",
      "chapter": 1,
      "verse": 1,
      "text": "En el principio creó Dios el cielo y la tierra.",
      "title": "Relato de la creación"
    }
  ]
}
```

### Campos por versículo:
- `book`: Código del libro (ej: "GEN", "MAT")
- `chapter`: Número de capítulo
- `verse`: Número de versículo
- `text`: Texto del versículo limpio
- `title`: Título de la sección (si existe)
- `comment`: Comentario del versículo (si existe)

## Códigos de Libros Soportados

### Antiguo Testamento (46 libros)
```
GEN, EXO, LEV, NUM, DEU, JOS, JDG, RUT, 1SA, 2SA,
1KI, 2KI, 1CH, 2CH, EZR, NEH, TOB, JDT, EST, 1MA,
2MA, JOB, PSA, PRO, ECC, SNG, WIS, SIR, ISA, JER,
LAM, BAR, EZK, DAN, HOS, JOL, AMO, OBA, JON, MIC,
NAM, HAB, ZEP, HAG, ZEC, MAL
```

### Nuevo Testamento (27 libros)
```
MAT, MRK, LUK, JHN, ACT, ROM, 1CO, 2CO, GAL, EPH,
PHP, COL, 1TH, 2TH, 1TI, 2TI, TIT, PHM, HEB, JAS,
1PE, 2PE, 1JN, 2JN, 3JN, JUD, REV
```

## Próximos Pasos

1. ✅ Completar extracción del PDF (en progreso)
2. ⏳ Verificar que todos los libros estén completos
3. ⏳ Identificar y extraer comentarios (formato específico)
4. ⏳ Validar conteo de versículos por libro
5. ⏳ Convertir a formato SQLite para la aplicación

## Notas sobre Comentarios

Según tu descripción:
- Los comentarios están **al final** de las secciones
- Cada comentario está **precedido por "COMENTARIO"**

Sin embargo, en las primeras 500 páginas no se encontró este marcador. Posibilidades:
1. Los comentarios aparecen después de los primeros libros
2. El marcador puede estar en otro formato (ej: "COMENTARIOS", "Comentario", etc.)
3. Los comentarios pueden estar en secciones separadas del PDF

**Acción**: Una vez completada la extracción completa, buscaremos patrones de comentarios en todo el texto extraído.

## Uso de los Scripts

### Ejecutar parser final:
```bash
python scripts/parse_navarra_final.py
```

### Ejecutar parser optimizado:
```bash
python scripts/parse_navarra_optimized.py
```

## Estado Final
✅ **Completado**: Extracción exitosa de toda la Biblia (AT y NT) con comentarios.

### Resultados:
- **Base de datos**: `navarra_complete.sqlite`
- **Total Versículos**: 35,855 (después de limpieza de apéndices)
- **Comentarios Extraídos**: ~3,600 asignados a versículos
- **Libros**: Todos los 73 libros detectados (incluyendo Epístolas)

### Archivos Generados:
1. `scripts/navarra_v4_complete.json`: Texto completo
2. `scripts/navarra_comments.json`: Comentarios extraídos
3. `scripts/navarra_final_merged.json`: Fusión de texto y comentarios
4. `navarra_complete.sqlite`: Base de datos final lista para usar

### Notas:
- Se utilizó `parse_navarra_v4.py` para el texto, corrigiendo la detección de libros mediante códigos en cabeceras.
- Se utilizó `extract_comments_final.py` para extraer los bloques de comentarios.
- Se fusionaron ambos resultados asignando comentarios a los versículos correspondientes.

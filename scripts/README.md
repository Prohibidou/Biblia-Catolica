# Scripts de extracción de PDF Bíblico

Este directorio contiene scripts para extraer contenido de PDFs bíblicos y convertirlos a bases de datos SQLite optimizadas para la aplicación.

## 📚 Scripts Disponibles

### 1. `parse_navarra_pdf.py` - Parser Especializado para Biblia de Navarra

Extrae versículos de PDFs de la Biblia de Navarra que usan el formato `GEN 1:1 Texto...`.

**Uso:**
```bash
python scripts/parse_navarra_pdf.py "ruta/al/pdf.pdf" nombre_output
```

**Ejemplo:**
```bash
python scripts/parse_navarra_pdf.py "BibliaPDF/AT Navarra.pdf" navarra_at
```

**Resultado:**
- Genera `scripts/navarra_at.json` con todos los versículos estructurados

### 2. `parse_bible_pdf.py` - Parser Genérico (Análisis)

Analiza la estructura de cualquier PDF bíblico para detectar patrones.

**Uso:**
```bash
# Solo análisis (recomendado primero)
python scripts/parse_bible_pdf.py "ruta/al/pdf.pdf"

# Con intento de parseo
python scripts/parse_bible_pdf.py "ruta/al/pdf.pdf" --parse
```

### 3. `convert_to_sqlite.py` - Convertir JSON a SQLite

Convierte un archivo JSON de versículos a una base de datos SQLite comprimida.

**Uso:**
```bash
python scripts/convert_to_sqlite.py scripts/archivo.json nombre_version
```

**Ejemplo:**
```bash
python scripts/convert_to_sqlite.py scripts/navarra_at.json navarra_at
```

**Resultado:**
- Genera `nombre_version.sqlite.gz` - Base de datos comprimida lista para deployment

## 🔄 Flujo de Trabajo Completo

### Para Biblia de Navarra (AT y NT):

1. **Extraer Antiguo Testamento:**
   ```bash
   python scripts/parse_navarra_pdf.py "BibliaPDF/AT Navarra.pdf" navarra_at
   ```

2. **Extraer Nuevo Testamento:**
   ```bash
   python scripts/parse_navarra_pdf.py "BibliaPDF/NT Navarra.pdf" navarra_nt
   ```

3. **Combinar AT y NT (opcional):**
   ```python
   import json
   
   with open('scripts/navarra_at.json', 'r', encoding='utf-8') as f:
       at = json.load(f)
   
   with open('scripts/navarra_nt.json', 'r', encoding='utf-8') as f:
       nt = json.load(f)
   
   combined = at + nt
   
   with open('scripts/navarra_complete.json', 'w', encoding='utf-8') as f:
       json.dump(combined, f, ensure_ascii=False, indent=2)
   ```

4. **Convertir a SQLite:**
   ```bash
   python scripts/convert_to_sqlite.py scripts/navarra_complete.json navarra_complete
   ```

5. **Mover a carpeta pública:**
   ```powershell
   Move-Item -Path "navarra_complete.sqlite.gz" -Destination "public/bibles/navarra_complete.sqlite.gz" -Force
   ```

6. **Actualizar VersionRegistry.ts:**
   - Agregar la nueva versión al array en `src/services/VersionRegistry.ts`
   - Actualizar el tamaño del archivo (fileSize) con el tamaño real

### Para otras Biblias:

1. **Analizar primero el formato:**
   ```bash
   python scripts/parse_bible_pdf.py "ruta/al/pdf.pdf"
   ```

2. **Revisar el archivo `pdf_full_sample.txt` generado**

3. **Adaptar el parser según el formato detectado:**
   - Si usa formato `CODIGO CAP:VER Texto` → usar `parse_navarra_pdf.py`
   - Si usa otro formato → modificar `parse_bible_pdf.py` o crear nuevo parser

4. **Continuar con pasos 3-6 del flujo anterior**

## 📊 Formatos JSON Esperados

### Versículos:
```json
[
  {
    "book": "GEN",
    "chapter": 1,
    "verse": 1,
    "text": "En el principio creó Dios el cielo y la tierra.",
    "comment": "Opcional: comentario o nota"
  }
]
```

### Códigos de Libros (USFM):
- Pentateuco: `GEN`, `EXO`, `LEV`, `NUM`, `DEU`
- Históricos: `JOS`, `JDG`, `RUT`, `1SA`, `2SA`, `1KI`, `2KI`, etc.
- Poéticos: `JOB`, `PSA`, `PRO`, `ECC`, `SNG`
- Profetas: `ISA`, `JER`, `LAM`, `EZK`, `DAN`, etc.
- Evangelios: `MAT`, `MRK`, `LUK`, `JHN`
- Cartas: `ROM`, `1CO`, `2CO`, `GAL`, `EPH`, etc.

## 📦 Tamaños de Archivos

| Archivo | Descripción | Tamaño comprimido |
|---------|-------------|-------------------|
| `navarra_complete.sqlite.gz` | Navarra AT completo (19,514 versículos) | ~1.44 MB |
| `navarra.sqlite.gz` | Demo (3 versículos) | ~0.66 KB |
| `straubinger.sqlite.gz` | Demo (3 versículos) | ~0.65 KB |

## ⚠️ Notas Importantes

1. **Derechos de Autor**: Asegúrate de tener permiso para usar el contenido bíblico
2. **Tamaño de PDFs**: Los PDFs grandes (>1000 páginas) pueden tardar varios minutos en procesarse
3. **Memoria**: El proceso requiere mantener todo el texto en memoria
4. **Formatos Variables**: Diferentes editoriales usan formatos distintos - ajusta el parser según sea necesario

## 🎯 Resultados Actuales

✅ **Completado:**
- ✓ Biblia de Navarra - Antiguo Testamento (19,514 versículos)
- ✓ Sistema de caching IndexedDB
- ✓ Interfaz de lectura con navegación
- ✓ Soporte para comentarios integrados

🔄 **Pendiente:**
- ⏳ Biblia de Navarra - Nuevo Testamento
- ⏳ Biblia Straubinger completa
- ⏳ Otras versiones católicas españolas

## 🛠️ Troubleshooting

### Error: "No se pudieron extraer versículos"
- Verifica el formato del PDF con `parse_bible_pdf.py` primero
- Revisa `pdf_full_sample.txt` para entender la estructura
- Ajusta las expresiones regulares en el parser

### Error: "PermissionError" al convertir a SQLite
- Espera unos segundos y vuelve a intentar
- Cierra cualquier programa que pueda tener abierto el archivo
- En Windows, reinicia el terminal si persiste

### La base de datos es muy grande
- Verifica que el JSON no tenga datos duplicados
- Asegúrate de que la compresión GZIP funcionó correctamente
- Tamaño esperado: ~60-80 bytes por versículo comprimido

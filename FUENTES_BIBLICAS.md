# APIs Bíblicas Disponibles

## 1. API Bible (api.scripture.api.bible)
- Gratuita con registro
- Múltiples versiones en español
- Formato JSON
- URL: https://scripture.api.bible/

## 2. Biblia API
- Española
- https://github.com/thiagobodruk/bible

## 3. Solución Manual Recomendada

Si tienes los textos en PDF o Word:

### Paso 1: Convertir PDF/Word a Texto
Usa herramientas como:
- pdftotext
- Adobe Acrobat
- Calibre (para ebooks)

### Paso 2: Estructurar el texto
Necesitas un JSON con este formato:

```json
[
    {
        "book": "GEN",
        "chapter": 1,
        "verse": 1,
        "text": "En el principio...",
        "comment": "Comentario opcional..."
    }
]
```

### Paso 3: Usar el script convert_to_sqlite.py
```bash
python scripts/convert_to_sqlite.py mi_biblia.json public/bibles/nombre
```

## 4. Contactar con Editoriales

Para uso legal de textos completos:
- **Biblia Navarra**: Universidad de Navarra (www.unav.edu)
- **Biblia Straubinger**: Fundación Gratis Date

Muchas editoriales permiten uso no comercial con atribución.

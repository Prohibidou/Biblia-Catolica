"""
IMPORTANTE: Este proyecto ya tiene funcionalidad para extraer contenido del Nuevo Testamento,
pero el PDF actual ("Sagrada Biblia Navarra.pdf") usa un formato diferente al AT que dificulta
la extracción automática de versículos con sus títulos de sección.

ESTADO ACTUAL:
- ✅ Antiguo Testamento: 26,158 versículos extraídos correctamente
- ⚠️ Nuevo Testamento: PDF sin códigos de libro al inicio de vers (formato diferente)

OPCIONES PARA COMPLETAR EL NT:

1. **MANUAL TYPING** (No recomendado - muy lento)
   - Escribir manualmente los ~7,957 versículos del NT
   - Tiempo: Semanas/meses

2. **BUSCAR FUENTE ALTERNATIVA** (✅ RECOMENDADO)
   - Buscar "Biblia de Navarra NT.pdf" con formato similar al AT
   - O descargar de fuente digital (ej: API, base de datos existente)
   - Tiempo: Minutos con parser existente

3. **OCR + PARSER COMPLEJO** (Posible pero lento)
   - Usar PyMuPDF para extraer con mejor precisión
   - Desarrollar lógica compleja para detectar libros/capítulos
   - Tiempo: 4-8 horas de desarrollo

4. **USAR DATOS EXISTENTES** (✅ MÁS RÁPIDO)
   - Buscar JSON del NT de Navarra ya procesado
   - Buscar API bíblica con Navarra
   - Tiempo: Minutos

RECOMENDACIÓN INMEDIATA:
Por ahora, la aplicación tiene:
- Biblia Navarra AT completa (26,158 vers)
- Sistema de cache funcionando
- UI lista para mostrar comentarios

Para agregar el NT sugiero:
A) Buscar si tienes "NT Navarra.pdf" separado
B) Usar una API bíblica temporal para el NT hasta conseguir Navarra completa
C) Continuar con AT por ahora y agregar NT progresivamente

¿Qué prefieres?
"""

print(__doc__)

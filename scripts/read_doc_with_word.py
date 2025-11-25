import sys
import os

try:
    import win32com.client as win32
    
    # Ruta absoluta
    doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
    
    print(f"Abriendo {doc_path} con Microsoft Word...")
    
    # Crear instancia de Word
    word = win32.Dispatch("Word.Application")
    word.Visible = False  # No mostrar Word
    
    # Abrir documento
    doc = word.Documents.Open(doc_path)
    
    print(f"Documento abierto: {doc.Name}")
    print(f"Número de párrafos: {doc.Paragraphs.Count}")
    
    # Extraer texto
    print("\nExtrayendo texto...")
    full_text = doc.Range().Text
    
    # Guardar muestra
    sample_path = 'scripts/nt_doc_texto_completo.txt'
    with open(sample_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    
    print(f"✓ Texto completo guardado en {sample_path}")
    print(f"  Tamaño: {len(full_text)} caracteres")
    
    # Mostrar primeras líneas
    lines = full_text.split('\r')[:50]
    print("\nPrimeras 50 líneas:")
    print("="*70)
    for i, line in enumerate(lines):
        if line.strip():
            print(f"{i+1}. {line[:100]}")
    
    # Cerrar documento y Word
    doc.Close(False)
    word.Quit()
    
    print("\n✓ Proceso completado")
    
except ImportError:
    print("pywin32 no está instalado. Instalando...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], check=True)
    print("\n¡Instalado! Por favor ejecuta el script nuevamente.")
except Exception as e:
    print(f"Error: {e}")
    print("\nSi Word no está instalado, necesitaremos convertir el archivo manualmente.")

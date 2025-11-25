import win32com.client as win32
import os

# Rutas absolutas
doc_path = os.path.abspath(r"BibliaPDF/NT Eunsa con notas (1).doc")
html_path = os.path.abspath(r"scripts/nt_navarra.html")

print(f"Abriendo {doc_path}...")
word = win32.Dispatch("Word.Application")
word.Visible = False

try:
    word.DisplayAlerts = 0 # wdAlertsNone
    
    doc = word.Documents.Open(doc_path)
    print("Documento abierto.")
    
    # Formato 10 = wdFormatFilteredHTML (HTML más limpio)
    # Formato 8 = wdFormatHTML
    print(f"Guardando como HTML en {html_path}...")
    doc.SaveAs2(html_path, FileFormat=10)
    
    print("✓ Conversión completada.")
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    try:
        doc.Close(False)
        word.Quit()
    except:
        pass

# Verificar tamaño
if os.path.exists(html_path):
    size = os.path.getsize(html_path)
    print(f"Tamaño del HTML: {size/1024/1024:.2f} MB")

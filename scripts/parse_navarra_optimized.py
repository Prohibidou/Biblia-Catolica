#!/usr/bin/env python3
"""
Parser optimizado para Sagrada Biblia Navarra.pdf
Extrae capítulos, versículos, títulos y comentarios

FORMATO DEL PDF:
- Los títulos tienen una fuente distinta a los versículos
- Los comentarios están al final de cada sección
- Cada comentario está precedido por el texto "COMENTARIO"
"""
import PyPDF2
import re
import json
from collections import defaultdict

# Configuración
PDF_FILE = "BibliaPDF/Sagrada Biblia Navarra.pdf"
OUTPUT_FILE = "scripts/navarra_biblia_completa_comentarios.json"

# Mapeo completo de códigos de libros
BOOK_CODES = {
    'Gn': 'GEN', 'Ex': 'EXO', 'Lv': 'LEV', 'Nm': 'NUM', 'Dt': 'DEU',
    'Jos': 'JOS', 'Jue': 'JDG', 'Rt': 'RUT', '1 S': '1SA', '2 S': '2SA',
    '1 R': '1KI', '2 R': '2KI', '1 Cro': '1CH', '2 Cro': '2CH',
    'Esd': 'EZR', 'Neh': 'NEH', 'Tob': 'TOB', 'Jdt': 'JDT', 'Est': 'EST',
    '1 Mac': '1MA', '2 Mac': '2MA', 'Job': 'JOB', 'Sal': 'PSA', 'Pr': 'PRO',
    'Ecl': 'ECC', 'Cant': 'SNG', 'Sab': 'WIS', 'Eclo': 'SIR', 'Is': 'ISA',
    'Jer': 'JER', 'Lam': 'LAM', 'Bar': 'BAR', 'Ez': 'EZK', 'Dan': 'DAN',
    'Os': 'HOS', 'Jl': 'JOL', 'Am': 'AMO', 'Abd': 'OBA', 'Jon': 'JON',
    'Miq': 'MIC', 'Nah': 'NAM', 'Hab': 'HAB', 'Sof': 'ZEP', 'Ag': 'HAG',
    'Zac': 'ZEC', 'Mal': 'MAL',
    'Mt': 'MAT', 'Mc': 'MRK', 'Lc': 'LUK', 'Jn': 'JHN', 'Hch': 'ACT',
    'Rom': 'ROM', '1 Cor': '1CO', '2 Cor': '2CO', 'Gal': 'GAL', 'Ef': 'EPH',
    'Flp': 'PHP', 'Col': 'COL', '1 Tes': '1TH', '2 Tes': '2TH',
    '1 Tim': '1TI', '2 Tim': '2TI', 'Tit': 'TIT', 'Flm': 'PHM', 'Heb': 'HEB',
    'Sant': 'JAS', '1 Pe': '1PE', '2 Pe': '2PE', '1 Jn': '1JN', '2 Jn': '2JN',
    '3 Jn': '3JN', 'Jud': 'JUD', 'Ap': 'REV'
}


class NavarraParser:
    def __init__(self):
        self.current_book = None
        self.current_chapter = 0
        self.current_verse = 0
        self.verse_buffer = ""
        self.title_buffer = []
        self.verses = []
        self.comments_section = defaultdict(list)  # Almacena comentarios por (book, chapter)
        self.is_in_comments = False
        self.current_comment_verse = None
        self.verse_count = 0
        self.comment_count = 0
        
    def extract_pdf_text(self, pdf_path):
        """Extrae texto del PDF página por página"""
        print(f"📖 Abriendo: {pdf_path}")
        text_lines = []
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            total_pages = len(pdf_reader.pages)
            print(f"   Total páginas: {total_pages:,}")
            
            for page_num in range(total_pages):
                if page_num % 200 == 0:
                    print(f"   Extrayendo página {page_num + 1}/{total_pages}...")
                
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                
                if text:
                    lines = text.split('\n')
                    text_lines.extend(lines)
        
        print(f"✅ Extraídas {len(text_lines):,} líneas\n")
        return text_lines
    
    def is_verse_number(self, line):
        """Detecta si una línea empieza con número de versículo"""
        return bool(re.match(r'^\d+\s+', line))
    
    def is_title(self, line):
        """Detecta si es un título (mayúsculas o fuente diferente)"""
        if not line or len(line) < 3:
            return False
        
        # No es título si empieza con número
        if re.match(r'^\d+', line):
            return False
        
        # Si es mayormente mayúsculas
        text_only = re.sub(r'[^A-ZÁÉÍÓÚÑa-záéíóúñ]', '', line)
        if text_only and len([c for c in text_only if c.isupper()]) / len(text_only) > 0.7:
            return True
        
        return False
    
    def is_comment_marker(self, line):
        """Detecta el marcador COMENTARIO"""
        return 'COMENTARIO' in line.upper()
    
    def detect_book_change(self, line):
        """Detecta cambio de libro bíblico"""
        for code_short, code_long in BOOK_CODES.items():
            # Buscar patrón: código al inicio de línea
            if line.startswith(code_short + ' ') or line.startswith(code_short + '\n'):
                return code_long
        return None
    
    def save_verse(self):
        """Guarda el versículo actual"""
        if not self.verse_buffer or not self.current_book:
            return
        
        # Limpiar texto del versículo
        text = re.sub(r'^\d+\s+', '', self.verse_buffer).strip()
        text = re.sub(r'\s+', ' ', text)
        
        verse_data = {
            'book': self.current_book,
            'chapter': self.current_chapter,
            'verse': self.current_verse,
            'text': text
        }
        
        # Agregar título si existe
        if self.title_buffer:
            verse_data['title'] = ' | '.join(self.title_buffer)
            self.title_buffer = []
        
        self.verses.append(verse_data)
        self.verse_count += 1
    
    def parse(self, text_lines):
        """Parser principal"""
        print("🔍 Iniciando parsing...")
        processing = False
        
        for i, line in enumerate(text_lines):
            line = line.strip()
            
            if not line:
                continue
            
            # Progreso
            if i % 20000 == 0 and i > 0:
                print(f"   Línea {i:,}/{len(text_lines):,} - Versículos: {self.verse_count}")
            
            # Buscar inicio (Génesis)
            if not processing:
                if 'Gn' in line or (re.match(r'^1\s+', line) and 'principio' in line.lower() and 'creó' in line.lower()):
                    processing = True
                    self.current_book = 'GEN'
                    self.current_chapter = 1
                    self.current_verse = 1
                    self.verse_buffer = line
                    print(f"✓ Inicio en Génesis: {line[:50]}...\n")
                    continue
                else:
                    continue
            
            # Detectar sección de comentarios
            if self.is_comment_marker(line):
                self.is_in_comments = True
                self.current_comment_verse = None
                continue
            
            # Si estamos en sección de comentarios
            if self.is_in_comments:
                # Detectar versículo al que pertenece el comentario
                # Formato común: "1. Texto del comentario" o "1-3. Texto"
                comment_verse_match = re.match(r'^(\d+)[\.\-,]', line)
                if comment_verse_match:
                    self.current_comment_verse = int(comment_verse_match.group(1))
                    comment_text = re.sub(r'^\d+[\.\-,]\s*', '', line)
                    self.comments_section[(self.current_book, self.current_chapter, self.current_comment_verse)].append(comment_text)
                elif self.current_comment_verse:
                    # Continuación del comentario
                    self.comments_section[(self.current_book, self.current_chapter, self.current_comment_verse)].append(line)
                
                # Salir de comentarios si encontramos inicio de nuevo capítulo/libro
                if self.is_verse_number(line) and re.match(r'^1\s+', line):
                    self.is_in_comments = False
                    self.current_comment_verse = None
                
                continue
            
            # Detectar cambio de libro
            new_book = self.detect_book_change(line)
            if new_book and new_book != self.current_book:
                self.save_verse()
                self.current_book = new_book
                self.current_chapter = 0
                self.verse_buffer = ""
                print(f"📕 Nuevo libro: {new_book}")
                continue
            
            # Detectar versículo
            if self.is_verse_number(line):
                verse_match = re.match(r'^(\d+)\s+(.*)$', line)
                if verse_match:
                    new_verse_num = int(verse_match.group(1))
                    verse_text = verse_match.group(2)
                    
                    # Nuevo capítulo (versículo 1)
                    if new_verse_num == 1 and self.current_verse > 1:
                        self.save_verse()
                        self.current_chapter += 1
                        self.current_verse = 1
                        self.verse_buffer = verse_text
                    
                    # Versículo consecutivo
                    elif new_verse_num == self.current_verse + 1 or (self.current_verse == 0 and new_verse_num == 1):
                        self.save_verse()
                        if self.current_chapter == 0:
                            self.current_chapter = 1
                        self.current_verse = new_verse_num
                        self.verse_buffer = verse_text
                    
                    # Continuación
                    else:
                        self.verse_buffer += " " + line
                continue
            
            # Detectar título
            if self.is_title(line):
                self.title_buffer.append(line)
                continue
            
            # Continuación del versículo
            if self.verse_buffer:
                self.verse_buffer += " " + line
        
        # Guardar último versículo
        self.save_verse()
        
        # Asociar comentarios con versículos
        print(f"\n📝 Asociando {len(self.comments_section)} comentarios con versículos...")
        for verse in self.verses:
            key = (verse['book'], verse['chapter'], verse['verse'])
            if key in self.comments_section:
                comments = self.comments_section[key]
                verse['comment'] = ' '.join(comments).strip()
                self.comment_count += 1
        
        print(f"\n✅ Parsing completado:")
        print(f"   Versículos: {self.verse_count:,}")
        print(f"   Con comentarios: {self.comment_count:,}")
        
        return self.verses
    
    def save_to_json(self, output_file):
        """Guarda resultado en JSON"""
        # Organizar por estructura
        structure = defaultdict(lambda: defaultdict(list))
        for verse in self.verses:
            structure[verse['book']][verse['chapter']].append(verse)
        
        output = {
            'version': 'Sagrada Biblia Navarra',
            'total_verses': len(self.verses),
            'total_books': len(structure),
            'verses_with_comments': self.comment_count,
            'data': self.verses
        }
        
        print(f"\n💾 Guardando en {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        # Estadísticas por libro
        print(f"\n📚 Libros procesados:")
        for book in sorted(structure.keys()):
            chapters = len(structure[book])
            total_verses = sum(len(structure[book][ch]) for ch in structure[book])
            total_comments = sum(1 for v in self.verses if v['book'] == book and 'comment' in v)
            print(f"   {book}: {chapters} cap, {total_verses} vers, {total_comments} com")


def main():
    print("="*70)
    print("PARSER OPTIMIZADO - SAGRADA BIBLIA NAVARRA")
    print("="*70)
    print()
    
    parser = NavarraParser()
    
    # 1. Extraer texto
    text_lines = parser.extract_pdf_text(PDF_FILE)
    
    # 2. Parsear
    verses = parser.parse(text_lines)
    
    # 3. Guardar
    parser.save_to_json(OUTPUT_FILE)
    
    print(f"\n✅ ¡Proceso completado exitosamente!")
    print(f"📄 Archivo: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

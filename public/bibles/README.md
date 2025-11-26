# Sagrada Biblia de Navarra - Data Source

## Source PDF
The complete extraction was performed from the following PDF:

**Sagrada Biblia Navarra.pdf**
- Google Drive: https://drive.google.com/file/d/1r0HUELJztDNZIPypfOUKKF87nkCIM0tU/view?usp=sharing
- Total Pages: 10,513
- Size: ~33 MB

## Extraction Results
- **Total Verses:** 35,855
- **Comments:** 3,250 (assigned to verses)
- **Section Titles:** 739
- **Books:** 73 complete (Catholic Canon)

### Old Testament
- 27,949 verses
- 2,571 comments
- 46 books (all complete)

### New Testament  
- 7,906 verses
- 679 comments
- 27 books (all complete, including Epistles)

## Database Files
- `navarra.sqlite` - Uncompressed database (19 MB)
- `navarra.sqlite.gz` - Compressed database (2.3 MB) - **Use this for deployment**

## Extraction Process
See `scripts/NAVARRA_EXTRACTION_README.md` for detailed extraction process and parser documentation.

## Scripts Used
- `parse_navarra_v4.py` - Main text parser
- `extract_comments_final.py` - Comment extractor
- `merge_navarra.py` - Text and comments merger
- `convert_navarra_to_sqlite.py` - SQLite database generator
- `validate_navarra_db.py` - Database validator

## Validation
All 73 books have been verified with correct chapter counts (±1 chapter due to edition variations).
Comments coverage is excellent with 3,250 comments distributed across key books.

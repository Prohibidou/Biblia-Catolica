// Mapeo de abreviaturas a códigos de libro
const bookAbbreviations: Record<string, string> = {
    // Nuevo Testamento
    'Mt': 'MAT', 'Mc': 'MRK', 'Lc': 'LUK', 'Jn': 'JHN',
    'Hch': 'ACT', 'Hec': 'ACT',
    'Rm': 'ROM', 'Rom': 'ROM',
    '1Co': '1CO', '2Co': '2CO',
    'Gal': 'GAL', 'Gá': 'GAL',
    'Ef': 'EPH', 'Efe': 'EPH',
    'Flp': 'PHP', 'Fil': 'PHP',
    'Col': 'COL',
    '1Ts': '1TH', '1Te': '1TH', '2Ts': '2TH', '2Te': '2TH',
    '1Tim': '1TI', '1Ti': '1TI', '2Tim': '2TI', '2Ti': '2TI',
    'Tit': 'TIT', 'Flm': 'PHM',
    'Heb': 'HEB',
    'Sant': 'JAS', 'Stg': 'JAS',
    '1Pe': '1PE', '1P': '1PE', '2Pe': '2PE', '2P': '2PE',
    '1Jn': '1JN', '1J': '1JN', '2Jn': '2JN', '2J': '2JN', '3Jn': '3JN', '3J': '3JN',
    'Jud': 'JUD',
    'Ap': 'REV', 'Apo': 'REV',

    // Antiguo Testamento  
    'Gn': 'GEN', 'Gén': 'GEN', 'Gen': 'GEN',
    'Ex': 'EXO', 'Éx': 'EXO',
    'Lv': 'LEV', 'Lev': 'LEV',
    'Nm': 'NUM', 'Núm': 'NUM',
    'Dt': 'DEU',
    'Jos': 'JOS',
    'Jue': 'JDG',
    'Rt': 'RUT', 'Rut': 'RUT',
    '1S': '1SA', '1Sa': '1SA', '1Sam': '1SA', '2S': '2SA', '2Sa': '2SA', '2Sam': '2SA',
    '1R': '1KI', '1Re': '1KI', '2R': '2KI', '2Re': '2KI',
    '1Cr': '1CH', '1Cro': '1CH', '2Cr': '2CH', '2Cro': '2CH',
    'Esd': 'EZR',
    'Neh': 'NEH',
    'Est': 'EST',
    'Job': 'JOB',
    'Sal': 'PSA',
    'Pr': 'PRO', 'Prov': 'PRO',
    'Ecl': 'ECC', 'Qo': 'ECC',
    'Cant': 'SNG', 'Ct': 'SNG',
    'Is': 'ISA',
    'Jr': 'JER', 'Jer': 'JER',
    'Lm': 'LAM', 'Lam': 'LAM',
    'Ez': 'EZK', 'Ezq': 'EZK',
    'Dn': 'DAN', 'Dan': 'DAN',
    'Os': 'HOS',
    'Jl': 'JOL', 'Joel': 'JOL',
    'Am': 'AMO', 'Amós': 'AMO',
    'Abd': 'OBA',
    'Jon': 'JON',
    'Miq': 'MIC',
    'Nah': 'NAH',
    'Hab': 'HAB',
    'Sof': 'ZEP',
    'Ag': 'HAG',
    'Zac': 'ZEC',
    'Mal': 'MAL'
};

export interface BibleReference {
    book: string;
    chapter: number;
    verseStart?: number;
    verseEnd?: number;
}

export function parseBibleReference(ref: string): BibleReference | null {
    ref = ref.trim();
    const match = ref.match(/^([A-Za-zÁÉÍÓÚáéíóúñÑ0-9]+)\s+(\d+)(?:,\s*(\d+)(?:-(\d+))?)?$/);

    if (!match) return null;

    const bookAbbr = match[1];
    const chapter = parseInt(match[2]);
    const verseStart = match[3] ? parseInt(match[3]) : undefined;
    const verseEnd = match[4] ? parseInt(match[4]) : verseStart;

    const bookCode = bookAbbreviations[bookAbbr];
    if (!bookCode) return null;

    return { book: bookCode, chapter, verseStart, verseEnd };
}

export function makeReferencesClickable(html: string): string {
    return html.replace(
        /<em>([^<]+)<\/em>/g,
        (_match, content) => {
            const parts = content.split(/\s+/);
            const firstRef = parseBibleReference(parts[0] + (parts[1] ? ' ' + parts[1] : ''));

            if (firstRef) {
                const refData = JSON.stringify(firstRef).replace(/"/g, '&quot;');
                return `<em><span class="bible-ref-link" data-ref='${refData}'>${content}</span></em>`;
            }

            return `<em>${content}</em>`;
        }
    );
}

export function attachReferenceHandlers(
    container: HTMLElement,
    onReferenceClick: (ref: BibleReference) => void
) {
    const links = container.querySelectorAll('.bible-ref-link');

    links.forEach(link => {
        const refData = link.getAttribute('data-ref');

        if (refData) {
            try {
                const ref = JSON.parse(refData) as BibleReference;

                (link as HTMLElement).style.cursor = 'pointer';
                (link as HTMLElement).style.textDecoration = 'underline';
                (link as HTMLElement).style.color = '#2563eb';

                link.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    onReferenceClick(ref);
                });
            } catch (e) {
                console.error('Failed to parse reference data:', refData, e);
            }
        }
    });
}

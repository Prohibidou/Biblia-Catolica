import initSqlJs, { type Database, type SqlJsStatic } from 'sql.js';
import type { IBibleAdapter } from './IBibleAdapter';
import type { Verse, SearchResult } from '../models/Verse';

export class SQLiteAdapter implements IBibleAdapter {
    private db: Database | null = null;
    private SQL: SqlJsStatic | null = null;

    async init(data: ArrayBuffer): Promise<void> {
        if (!this.SQL) {
            this.SQL = await initSqlJs({
                // Locate the wasm file. We'll ensure it's copied to public/assets
                locateFile: file => `/assets/${file}`
            });
        }

        if (this.db) {
            this.db.close();
        }

        this.db = new this.SQL.Database(new Uint8Array(data));
    }
    async getChapterContent(bookId: string, chapter: number): Promise<Verse[]> {
        if (!this.db) throw new Error("Database not initialized");

        // 1. Get verses
        const stmtVerses = this.db.prepare("SELECT book, chapter, verse, text FROM verses WHERE book = $book AND chapter = $chapter ORDER BY verse");
        stmtVerses.bind({ $book: bookId, $chapter: chapter });

        const verses: Verse[] = [];
        while (stmtVerses.step()) {
            const row = stmtVerses.getAsObject();
            verses.push({
                bookId: row.book as string,
                chapter: row.chapter as number,
                verse: row.verse as number,
                text: row.text as string,
                comment: undefined // Will be populated below
            });
        }
        stmtVerses.free();

        // 2. Get comments for this chapter
        // We select all comments that overlap with this chapter
        // Actually comments table has book/chapter columns, so it's easy
        try {
            const stmtComments = this.db.prepare("SELECT verse_start, verse_end, text FROM comments WHERE book = $book AND chapter = $chapter ORDER BY verse_start, id");
            stmtComments.bind({ $book: bookId, $chapter: chapter });

            const comments: Array<{ start: number, end: number, text: string }> = [];
            while (stmtComments.step()) {
                const row = stmtComments.getAsObject();
                comments.push({
                    start: row.verse_start as number,
                    end: row.verse_end as number,
                    text: row.text as string
                });
            }
            stmtComments.free();

            // 3. Attach comments to verses
            // Since we need to maintain compatibility with the frontend which expects a single 'comment' string,
            // we will concatenate multiple comments with <br><br> if a verse has multiple.
            // The frontend is already equipped to split them.

            for (const verse of verses) {
                const vNum = verse.verse;
                // Find all comments that include this verse
                const applicableComments = comments.filter(c => vNum >= c.start && vNum <= c.end);

                if (applicableComments.length > 0) {
                    // Join with separator
                    verse.comment = applicableComments.map(c => c.text).join('<br><br>');
                }
            }
        } catch (e) {
            // Table might not exist yet (if using old DB), fallback or ignore
            console.warn("Could not load comments from new table:", e);
            // Fallback: try loading from verses table if comments table failed?
            // But we just cleared the verses table comments column.
        }

        return verses;
    }

    async search(query: string, limit: number = 20): Promise<SearchResult[]> {
        if (!this.db) throw new Error("Database not initialized");

        const stmt = this.db.prepare("SELECT book, chapter, verse, text FROM verses WHERE text LIKE $query LIMIT $limit");
        const result: SearchResult[] = [];

        stmt.bind({ $query: `%${query}%`, $limit: limit });

        while (stmt.step()) {
            const row = stmt.getAsObject();
            result.push({
                bookId: row.book as string,
                chapter: row.chapter as number,
                verse: row.verse as number,
                text: row.text as string
            });
        }
        stmt.free();
        return result;
    }

    close(): void {
        if (this.db) {
            this.db.close();
            this.db = null;
        }
    }
}

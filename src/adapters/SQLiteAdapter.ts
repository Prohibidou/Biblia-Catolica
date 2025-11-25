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

        // Assuming a standard schema: verses table with book, chapter, verse, text columns
        // Adjust table/column names based on your actual SQLite schema
        const stmt = this.db.prepare("SELECT book, chapter, verse, text, comment FROM verses WHERE book = $book AND chapter = $chapter");
        const result: Verse[] = [];

        stmt.bind({ $book: bookId, $chapter: chapter });

        while (stmt.step()) {
            const row = stmt.getAsObject();
            result.push({
                bookId: row.book as string,
                chapter: row.chapter as number,
                verse: row.verse as number,
                text: row.text as string,
                comment: row.comment as string || undefined
            });
        }
        stmt.free();
        return result;
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

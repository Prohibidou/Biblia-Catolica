import type { Verse, SearchResult } from '../models/Verse';

export interface IBibleAdapter {
    /**
     * Initialize the adapter with the raw data (ArrayBuffer for SQLite, Object for JSON)
     */
    init(data: ArrayBuffer | object): Promise<void>;

    /**
     * Get all verses for a specific chapter
     */
    getChapterContent(bookId: string, chapter: number): Promise<Verse[]>;

    /**
     * Search for text within the bible version
     */
    search(query: string, limit?: number): Promise<SearchResult[]>;

    /**
     * Close connection/free resources
     */
    close(): void;
}

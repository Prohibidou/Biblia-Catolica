export interface Verse {
    bookId: string;
    chapter: number;
    verse: number;
    text: string;
    comment?: string;
}

export interface SearchResult {
    bookId: string;
    chapter: number;
    verse: number;
    text: string;
    matchScore?: number;
}

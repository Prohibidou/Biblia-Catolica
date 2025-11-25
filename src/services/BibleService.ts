import type { IBibleAdapter } from '../adapters/IBibleAdapter';
import { SQLiteAdapter } from '../adapters/SQLiteAdapter';
import { CacheManager } from './CacheManager';
import { NetworkLoader } from './NetworkLoader';
import { VersionRegistry } from './VersionRegistry';
import type { Verse, SearchResult } from '../models/Verse';

export class BibleService {
    private activeAdapter: IBibleAdapter | null = null;
    private cache: CacheManager;
    private network: NetworkLoader;
    private registry: VersionRegistry;
    private currentVersionId: string | null = null;

    constructor() {
        this.cache = new CacheManager();
        this.network = new NetworkLoader();
        this.registry = new VersionRegistry();
    }

    async initialize(): Promise<void> {
        // Any startup logic, e.g. checking cache health
    }

    getAvailableVersions() {
        return this.registry.getAvailableVersions();
    }

    async loadVersion(versionId: string): Promise<void> {
        if (this.currentVersionId === versionId && this.activeAdapter) {
            return; // Already loaded
        }

        const metadata = this.registry.getVersionMetadata(versionId);
        if (!metadata) {
            throw new Error(`Version ${versionId} not found`);
        }

        // 1. Check Cache
        let data = await this.cache.getVersion(versionId);

        // 2. If not in cache, download
        if (!data) {
            console.log(`Downloading version ${versionId}...`);
            const rawData = await this.network.fetchResource(metadata.url);
            data = this.network.decompressGzip(rawData);

            // 3. Save to Cache
            await this.cache.saveVersion(versionId, data);
        } else {
            console.log(`Loaded version ${versionId} from cache.`);
        }

        // 4. Initialize Adapter
        if (this.activeAdapter) {
            this.activeAdapter.close();
        }

        if (metadata.format === 'sqlite') {
            this.activeAdapter = new SQLiteAdapter();
            await this.activeAdapter.init(data);
        } else {
            throw new Error(`Format ${metadata.format} not supported yet`);
        }

        this.currentVersionId = versionId;
    }

    async getChapter(bookId: string, chapter: number): Promise<Verse[]> {
        if (!this.activeAdapter) {
            throw new Error("No bible version loaded");
        }
        return await this.activeAdapter.getChapterContent(bookId, chapter);
    }

    async search(query: string): Promise<SearchResult[]> {
        if (!this.activeAdapter) {
            throw new Error("No bible version loaded");
        }
        return await this.activeAdapter.search(query);
    }
}

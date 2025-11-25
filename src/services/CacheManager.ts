import localforage from 'localforage';

export class CacheManager {
    private store: LocalForage;

    constructor() {
        this.store = localforage.createInstance({
            name: 'BibliaCatolicaApp',
            storeName: 'bible_versions'
        });
    }

    async saveVersion(versionId: string, data: ArrayBuffer): Promise<void> {
        try {
            await this.store.setItem(versionId, data);
            console.log(`Version ${versionId} cached successfully.`);
        } catch (error) {
            console.error(`Failed to cache version ${versionId}:`, error);
            throw error;
        }
    }

    async getVersion(versionId: string): Promise<ArrayBuffer | null> {
        try {
            const data = await this.store.getItem<ArrayBuffer>(versionId);
            return data;
        } catch (error) {
            console.error(`Failed to retrieve version ${versionId} from cache:`, error);
            return null;
        }
    }

    async hasVersion(versionId: string): Promise<boolean> {
        try {
            const keys = await this.store.keys();
            return keys.includes(versionId);
        } catch (error) {
            return false;
        }
    }

    async clearCache(): Promise<void> {
        await this.store.clear();
    }
}

import pako from 'pako';

export class NetworkLoader {

    async fetchResource(url: string): Promise<ArrayBuffer> {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Failed to fetch resource: ${response.statusText}`);
        }
        return await response.arrayBuffer();
    }

    decompressGzip(data: ArrayBuffer): ArrayBuffer {
        try {
            // Check if it's actually gzipped (magic number 1f 8b)
            const view = new Uint8Array(data);
            if (view[0] === 0x1f && view[1] === 0x8b) {
                const decompressed = pako.ungzip(view);
                return decompressed.buffer;
            }
            // If not gzipped, return original
            return data;
        } catch (error) {
            console.error("Decompression failed", error);
            throw error;
        }
    }
}

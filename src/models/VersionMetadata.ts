export interface VersionMetadata {
    id: string;
    name: string;
    shortName: string;
    type?: 'catholic' | 'protestant' | 'ecumenical';
    description?: string;
    fileSize: number;
    isExternal: boolean;
    url: string;
    format: 'sqlite' | 'json';
    available?: boolean;
    copyright?: string;
}

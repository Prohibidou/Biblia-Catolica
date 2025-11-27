import type { VersionMetadata } from '../models/VersionMetadata';

export class VersionRegistry {
    private versions: VersionMetadata[] = [
        {
            id: 'navarra_v7',
            name: 'Biblia de Navarra',
            shortName: 'Navarra',
            type: 'catholic',
            description: 'Sagrada Biblia Universidad de Navarra (Completa - AT + NT con comentarios)',
            fileSize: 2275328, // 2.17 MB
            isExternal: false,
            url: '/bibles/navarra.sqlite.gz',
            format: 'sqlite',
            available: true,
            copyright: 'EUNSA'
        },
        {
            id: 'straubinger',
            name: 'Biblia Straubinger',
            shortName: 'Straubinger',
            type: 'catholic',
            description: 'Sagrada Biblia Platense (Mons. Juan Straubinger)',
            fileSize: 2260325,
            isExternal: false,
            url: '/bibles/straubinger.sqlite.gz',
            format: 'sqlite',
            available: true,
            copyright: 'Fundación Gratis Date'
        }
    ];

    getAvailableVersions(): VersionMetadata[] {
        return this.versions;
    }

    getVersionMetadata(versionId: string): VersionMetadata | undefined {
        return this.versions.find(v => v.id === versionId);
    }
}

import type { UTI } from '@/src/models';
import type { DocumentType, InfoPlist } from '@/src/types';
import type { JXAApplication } from '@/src/types';
import '@jxa/global-type';

export class App {
    readonly name: string;
    readonly id: string;
    readonly version: string;
    readonly path: string;

    readonly documentTypes: {
        [key: string]: DocumentType['CFBundleTypeRole'];
    } = {};
    readonly urlSchemes: string[] = [];

    constructor(bundleId: string) {
        const app: JXAApplication = Application(bundleId);
        app.includeStandardAdditions = true;

        // Basic app properties
        this.name = app.name();
        this.id = app.id() as unknown as string;
        this.version = app.properties()['version'];
        this.path = app
            .pathTo(null, {
                from: null,
            })
            .toString()
            .replace('/System/Volumes/Preboot/Cryptexes/App/System', '');

        // Complex app properties
        const contents: InfoPlist = ObjC.deepUnwrap(
            $.NSDictionary.dictionaryWithContentsOfFile(this.infoPlist),
        );

        for (const documentType of contents.CFBundleDocumentTypes!) {
            for (const mimeType of documentType.CFBundleTypeMIMETypes || []) {
                this.documentTypes[mimeType] = documentType.CFBundleTypeRole;
            }

            for (const extension of documentType.CFBundleTypeExtensions || []) {
                this.documentTypes[extension] = documentType.CFBundleTypeRole;
            }
        }

        this.urlSchemes = contents.CFBundleURLTypes!.flatMap(
            (urlType) => urlType.CFBundleURLSchemes,
        );
    }

    get infoPlist(): string {
        return this.path + '/Contents/Info.plist';
    }

    supportsUTI(uti: UTI, role: DocumentType['CFBundleTypeRole']) {
        const commonTags = uti.tags.filter((tag) =>
            Object.keys(this.documentTypes).includes(tag)
                ? this.documentTypes[tag] === role
                : false,
        );
        return commonTags.length > 0;
    }

    supportsURLScheme(urlScheme: string) {
        return this.urlSchemes.includes(urlScheme);
    }
}

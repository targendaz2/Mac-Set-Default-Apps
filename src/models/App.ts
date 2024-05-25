import type { AppAssociation, UTI } from '@/models';
import type { DocumentType, InfoPlist } from '@/types';
import type { JXAApplication } from '@/types';
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
        const app: JXAApplication = Application.currentApplication();
        app.includeStandardAdditions = true;

        // App path so we can get Info.plist
        this.path = app.doShellScript(
            `mdfind kMDItemCFBundleIdentifier = '${bundleId}'`,
        );

        // Info.plist contents
        const contents: InfoPlist = ObjC.deepUnwrap(
            $.NSDictionary.dictionaryWithContentsOfFile(this.infoPlist),
        );

        // Basic app properties
        this.name = contents.CFBundleDisplayName;
        this.id = contents.CFBundleIdentifier;
        this.version = contents.CFBundleShortVersionString;

        // Complex app properties
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

    supportsUTI(uti: UTI): boolean {
        const commonTags = uti.tags.filter((tag) =>
            Object.keys(this.documentTypes).includes(tag)
                ? this.documentTypes[tag] === uti.role
                : false,
        );
        return commonTags.length > 0;
    }

    supportsURLScheme(urlScheme: string): boolean {
        return this.urlSchemes.includes(urlScheme);
    }

    supportsAssociation(assoc: AppAssociation): boolean {
        for (const uti of assoc.utis) {
            if (!this.supportsUTI(uti)) return false;
        }

        for (const urlScheme of assoc.urlSchemes) {
            if (!this.supportsURLScheme(urlScheme)) return false;
        }

        return true;
    }
}

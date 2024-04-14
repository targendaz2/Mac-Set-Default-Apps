import '@jxa/global-type';
import type { InfoPlist } from '../types';

export class App {
    readonly name: string;
    readonly id: string;
    readonly version: string;
    readonly path: string;

    readonly documentTypes: string[] = [];
    readonly urlSchemes: string[] = [];

    constructor(bundleId: string) {
        const app = Application(bundleId);
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

        let documentTypes = [];

        documentTypes = contents.CFBundleDocumentTypes!.flatMap(
            (documentType) => documentType.CFBundleTypeMIMETypes!,
        );

        documentTypes = documentTypes.concat(
            contents.CFBundleDocumentTypes!.flatMap(
                (documentType) => documentType.CFBundleTypeExtensions!,
            ),
        );

        this.documentTypes = Array.from(new Set(documentTypes));

        this.urlSchemes = contents.CFBundleURLTypes!.flatMap(
            (urlType) => urlType.CFBundleURLSchemes,
        );
    }

    get infoPlist(): string {
        return this.path + '/Contents/Info.plist';
    }
}

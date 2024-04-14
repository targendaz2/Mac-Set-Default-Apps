import '@jxa/global-type';
import type { InfoPlist } from '../types';

export class App {
    readonly name: string;
    readonly id: string;
    readonly version: string;
    readonly path: string;

    readonly urlSchemes?: string[] = [];

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

        for (const urlType of contents.CFBundleURLTypes!) {
            this.urlSchemes = this.urlSchemes!.concat(
                urlType.CFBundleURLSchemes,
            );
        }
    }

    get infoPlist(): string {
        return this.path + '/Contents/Info.plist';
    }
}

import '@jxa/global-type';

export class App {
    readonly name: string;
    readonly id: string;
    readonly version: string;
    readonly path: string;

    constructor(bundleId: string) {
        const app = Application(bundleId);
        app.includeStandardAdditions = true;

        this.name = app.name();
        this.id = app.id() as unknown as string;
        this.version = app.properties()['version'];
        this.path = app
            .pathTo(null, {
                from: null,
            })
            .toString()
            .replace('/System/Volumes/Preboot/Cryptexes/App/System', '');
    }

    get infoPlist(): string {
        return this.path + '/Contents/Info.plist';
    }
}

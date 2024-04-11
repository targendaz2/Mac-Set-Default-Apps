export default class App {
    name: string;
    id: string;
    version: string;
    path: string;
    documentTypes?: string[];

    constructor(public bundleId: string) {
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
}

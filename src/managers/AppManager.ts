import '@jxa/global-type';
import type AppModel from '../models/App';

const App: typeof AppModel = require('../models/App');

export default class AppManager {
    readonly app: typeof Application &
        Application._StandardAdditions &
        Application.AnyValue;

    constructor(bundleId: string) {
        this.app = Application(bundleId);
        this.app.includeStandardAdditions = true;
    }

    get name(): string {
        return this.app.name();
    }

    get id(): string {
        return this.app.id() as unknown as string;
    }

    get version(): string {
        return this.app.properties()['version'];
    }

    get path(): string {
        return this.app
            .pathTo(null, {
                from: null,
            })
            .toString()
            .replace('/System/Volumes/Preboot/Cryptexes/App/System', '');
    }

    create(): AppModel {
        return new App(this.name, this.id, this.version, this.path);
    }
}

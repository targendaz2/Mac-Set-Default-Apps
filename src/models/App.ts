import '@jxa/global-type';

export class App {
    constructor(
        readonly name: string,
        readonly id: string,
        readonly version: string,
        readonly path: string,
    ) {}

    get infoPlist(): string {
        return this.path + '/Contents/Info.plist';
    }
}

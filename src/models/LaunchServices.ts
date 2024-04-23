import type { LSHandler, LaunchServicesPlist } from '@/src/types';
import type { JXAApplication } from '@/src/types';
import '@jxa/global-type';

export class LaunchServices {
    readonly lsHandlers: LSHandler[] = [];

    constructor(readonly plist: string) {
        const app: JXAApplication = Application.currentApplication();
        app.includeStandardAdditions = true;

        const path = Path(this.plist);

        if (app.exists(path)) {
            const contents: LaunchServicesPlist = ObjC.deepUnwrap(
                $.NSDictionary.dictionaryWithContentsOfFile(this.plist),
            );

            this.lsHandlers = contents.LSHandlers;
        }
    }
}

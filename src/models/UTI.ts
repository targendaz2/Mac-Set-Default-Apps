import type Config from '@/src/config.json';
import '@jxa/global-type';

const config: typeof Config = require('@/src/config.json');

export class UTI {
    readonly id: string;
    readonly tags: string[];

    constructor(id: string) {
        const app = Application.currentApplication();
        app.includeStandardAdditions = true;

        this.id = id;

        // This long awk command essentially parses the lsregister dump for
        // ID's and tags matching the given UTI. The lsregister dump is huge
        // and the command doesn't natively allow searching or filtering.
        // TODO: Handle the lsregister dump parsing in JavaScript
        const cmd = `${config.systemPaths.lsregister} -gc -dump Type | awk -F ':' "{ if (\\$1 == \\"type id\\" && \\$2 ~ \\"public.html\\") { check=\\"yes\\" } else if (\\$1 == \\"type id\\") { check=\\"no\\" } else if (\\$1 == \\"tags\\" && check == \\"yes\\") { print \\$2 } }"`;

        const result: string = app.doShellScript(cmd);

        this.tags = Array.from(
            new Set(
                result
                    .replace(/(, )?["'][\w ]+["'],?/g, '')
                    .replace(/\s|\.|,/g, ' ')
                    .replace(/ +/g, ' ')
                    .trim()
                    .split(' '),
            ),
        );
    }
}

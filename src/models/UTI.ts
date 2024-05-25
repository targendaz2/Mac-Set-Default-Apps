import type Config from '@/config.json';
import type { UTIRole } from '@/types';
import '@jxa/global-type';

const config: typeof Config = require('@/config.json');

export class UTI {
    readonly id: string;
    readonly role: UTIRole;
    readonly tags: string[];

    constructor(id: string, role: UTIRole) {
        const app = Application.currentApplication();
        app.includeStandardAdditions = true;

        this.id = id;
        this.role = role;

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

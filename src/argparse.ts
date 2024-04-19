import type { JXAApplication } from '@/src/types';
import '@jxa/global-type';

export function getArgs(): string[] {
    const args = $.NSProcessInfo.processInfo.arguments;
    // Build the normal argv/argc
    const argv = [];
    const argc = args.count; // -[NSArray count]
    for (let i = 0; i < argc; i++) {
        argv.push(ObjC.unwrap(args.objectAtIndex(i))); // -[NSArray objectAtIndex:]
    }
    return argv;
}

export function parseArgs(args: string[]) {
    const app: JXAApplication = Application.currentApplication();
    app.includeStandardAdditions = true;

    const code = `
        function parse_args() {
            local bundle_id="\${1:-}"
            echo "$bundle_id"
        }
        parse_args ${args.join(' ')}
    `;

    const parsedArgs = app.doShellScript(code);

    return parsedArgs;
}

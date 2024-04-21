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

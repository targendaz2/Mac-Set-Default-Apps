export function getArgs(): string[] {
  const args = $.NSProcessInfo.processInfo.arguments;
  const argv = [];
  const argc = args.count;
  for (let i = 0; i < argc; i++) {
    argv.push(ObjC.unwrap(args.objectAtIndex(i)));
  }
  return argv;
}

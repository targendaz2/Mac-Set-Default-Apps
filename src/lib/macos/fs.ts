export function exists(path: string): boolean {
  ObjC.import('Foundation');
  return $.NSFileManager.alloc.init.fileExistsAtPathIsDirectory(path, false);
}

export function mkDir(path: string): void {
  ObjC.import('Foundation');
  $.NSFileManager.alloc.init.createDirectoryAtPathWithIntermediateDirectoriesAttributesError(
    path,
    true,
    $(),
    $(),
  );
}

export function readPlist<T = { [key: string]: unknown }>(path: string): T {
  return ObjC.deepUnwrap($.NSDictionary.dictionaryWithContentsOfFile(path));
}

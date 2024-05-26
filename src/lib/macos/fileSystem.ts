export const fs = {
    pathExists: (path: string): boolean => {
        ObjC.import('Foundation');
        return $.NSFileManager.alloc.init.fileExistsAtPathIsDirectory(
            path,
            false,
        );
    },
    readPlist: <T = { [key: string]: unknown }>(path: string): T => {
        return ObjC.deepUnwrap(
            $.NSDictionary.dictionaryWithContentsOfFile(path),
        );
    },
};

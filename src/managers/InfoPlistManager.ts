import type { CFBundleURLType, InfoPlist } from '../types';

export class InfoPlistManager {
    readonly contents: InfoPlist;

    constructor(plistPath: string) {
        this.contents = ObjC.deepUnwrap(
            $.NSDictionary.dictionaryWithContentsOfFile(plistPath),
        );
    }

    get urlTypes(): CFBundleURLType[] | undefined {
        return this.contents.CFBundleURLTypes;
    }
}

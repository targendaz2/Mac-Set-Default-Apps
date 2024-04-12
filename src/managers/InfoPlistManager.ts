import type { DocumentType, InfoPlist, UrlType } from '../types';

export class InfoPlistManager {
    readonly contents: InfoPlist;

    constructor(plistPath: string) {
        this.contents = ObjC.deepUnwrap(
            $.NSDictionary.dictionaryWithContentsOfFile(plistPath),
        );
    }

    get documentTypes(): DocumentType[] | undefined {
        return this.contents.CFBundleDocumentTypes;
    }

    get urlTypes(): UrlType[] | undefined {
        return this.contents.CFBundleURLTypes;
    }
}

import type { DocumentType, InfoPlist, URLType } from '../types';

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

    get urlTypes(): URLType[] | undefined {
        return this.contents.CFBundleURLTypes;
    }
}

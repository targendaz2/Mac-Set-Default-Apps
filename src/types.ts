import '@jxa/global-type';

export type DocumentType = {
    CFBundleTypeExtensions?: string[];
    CFBundleTypeMIMETypes?: string[];
    CFBundleTypeRole: 'Editor' | 'Viewer' | 'Shell' | 'QLGenerator' | 'None';
};

export type UrlType = {
    CFBundleURLSchemes: string[];
};

export type InfoPlist = {
    CFBundleDisplayName: string;
    CFBundleDocumentTypes?: DocumentType[];
    CFBundleIdentifier: string;
    CFBundleName: string;
    CFBundleShortVersionString: string;
    CFBundleURLTypes?: UrlType[];
};

export type JxaApplication = typeof Application &
    Application._StandardAdditions &
    Application.AnyValue;

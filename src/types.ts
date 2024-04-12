import '@jxa/global-type';

export type DocumentType = {
    CFBundleTypeExtensions?: string[];
    CFBundleTypeMIMETypes?: string[];
    CFBundleTypeRole: 'Editor' | 'Viewer' | 'Shell' | 'QLGenerator' | 'None';
};

export type URLType = {
    CFBundleURLSchemes: string[];
};

export type InfoPlist = {
    CFBundleDisplayName: string;
    CFBundleDocumentTypes?: DocumentType[];
    CFBundleIdentifier: string;
    CFBundleName: string;
    CFBundleShortVersionString: string;
    CFBundleURLTypes?: URLType[];
};

export type JXAApplication = typeof Application &
    Application._StandardAdditions &
    Application.AnyValue;

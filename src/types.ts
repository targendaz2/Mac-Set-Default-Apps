import '@jxa/global-type';

export type CFBundleDocumentType = {
    CFBundleTypeExtensions?: string[];
    CFBundleTypeMIMETypes?: string[];
    CFBundleTypeRole: string;
};

export type CFBundleURLType = {
    CFBundleURLSchemes: string[];
};

export type InfoPlist = {
    CFBundleDisplayName: string;
    CFBundleDocumentTypes?: CFBundleDocumentType[];
    CFBundleIdentifier: string;
    CFBundleName: string;
    CFBundleShortVersionString: string;
    CFBundleURLTypes?: CFBundleURLType[];
};

export type JxaApplication = typeof Application &
    Application._StandardAdditions &
    Application.AnyValue;

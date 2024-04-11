interface CFBundleDocumentType {
    CFBundleTypeExtensions?: string[];
    CFBundleTypeMIMETypes?: string[];
    CFBundleTypeRole: string;
}

interface CFBundleURLType {
    CFBundleURLSchemes: string[];
}

export interface InfoPlist {
    CFBundleDisplayName: string;
    CFBundleDocumentTypes: CFBundleDocumentType[];
    CFBundleIdentifier: string;
    CFBundleName: string;
    CFBundleShortVersionString: string;
    CFBundleURLTypes: CFBundleURLType[];
}

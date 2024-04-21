import '@jxa/global-type';

export type DocumentType = {
    CFBundleTypeExtensions?: string[];
    CFBundleTypeMIMETypes?: string[];
    CFBundleTypeRole:
        | 'Editor'
        | 'Viewer'
        | 'Shell'
        | 'QLGenerator'
        | 'None'
        | 'All';
};

export type UTLType = {
    CFBundleURLSchemes: string[];
};

export type InfoPlist = {
    CFBundleDisplayName: string;
    CFBundleDocumentTypes?: DocumentType[];
    CFBundleIdentifier: string;
    CFBundleName: string;
    CFBundleShortVersionString: string;
    CFBundleURLTypes?: UTLType[];
};

export type JXAApplication = typeof Application &
    Application._StandardAdditions &
    Application.AnyValue;

export type UTIRole = 'Viewer' | 'Shell' | 'QLGenerator' | 'None' | 'All';

type DefaultApp = {
    /**
     * UTI's required by this default app definition.
     *
     * @minProperties 1
     * */
    utis: {
        [key: string]: UTIRole;
    };

    /**
     * URL schemes by this default app definition.
     *
     * @minItems 1
     * */
    urlSchemes: string[];
};

export interface Config {
    $schema: string;

    /**
     * Requirements an app must meet to be set as a default.
     *
     * @minProperties 1
     * */
    defaultAppRequirements: {
        [key: string]:
            | Pick<DefaultApp, 'utis'>
            | Pick<DefaultApp, 'urlSchemes'>
            | DefaultApp;
    };

    /**
     * Paths to system files and directories.
     *
     * @minProperties 1
     * */
    systemPaths: {
        [key: string]: string;
    };
}

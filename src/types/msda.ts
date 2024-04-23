export type UTIRole = 'Viewer' | 'Shell' | 'QLGenerator' | 'None' | 'All';

export type DefaultApp = {
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
     * Configures how MSDA handles logging.
     *
     * */
    logging: {
        logPath: string;
        verbose: boolean;
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

type LSHandlerBaseViewer = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleViewer: string;
    };
    LSHandlerRoleViewer: string;
};

type LSHandlerBaseShell = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleShell: string;
    };
    LSHandlerRoleShell: string;
};

type LSHandlerBaseQLGenerator = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleQLGenerator: string;
    };
    LSHandlerRoleQLGenerator: string;
};

type LSHandlerBaseNone = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleNone: string;
    };
    LSHandlerRoleNone: string;
};

type LSHandlerBaseAll = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleAll: string;
    };
    LSHandlerRoleAll: string;
};

type LSHandlerBase =
    | LSHandlerBaseViewer
    | LSHandlerBaseShell
    | LSHandlerBaseQLGenerator
    | LSHandlerBaseNone
    | LSHandlerBaseAll;

export type LSHandlerDocumentType = LSHandlerBase & {
    LSHandlerContentType: string;
};

export type LSHandlerURLScheme = {
    LSHandlerPreferredVersions: {
        LSHandlerRoleAll: '-';
    };
    LSHandlerRoleAll: string;
    LSHandlerURLScheme: string;
};

export type LSHandler = LSHandlerDocumentType | LSHandlerURLScheme;

export type LaunchServicesPlist = {
    LSHandlers: LSHandler[];
};

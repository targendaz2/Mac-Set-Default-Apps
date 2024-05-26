import type { DocumentType, LSHandler, URLScheme } from './interfaces';
import type {
    DocumentTypeSchema,
    LSHandlerSchema,
    LaunchServicesSchema,
    URLSchemeSchema,
} from './schemas';

export function serializeDocumentType(data: DocumentTypeSchema): DocumentType {
    const uti = data.LSHandlerContentType;

    let role: DocumentType['role'];
    let appID: string;
    let appVersion: string;

    if ('LSHandlerRoleViewer' in data) {
        role = 'Viewer';
        appID = data['LSHandlerRoleViewer'];
        appVersion = data['LSHandlerPreferredVersions']['LSHandlerRoleViewer'];
    } else if ('LSHandlerRoleShell' in data) {
        role = 'Shell';
        appID = data['LSHandlerRoleShell'];
        appVersion = data['LSHandlerPreferredVersions']['LSHandlerRoleShell'];
    } else if ('LSHandlerRoleQLGenerator' in data) {
        role = 'QLGenerator';
        appID = data['LSHandlerRoleQLGenerator'];
        appVersion =
            data['LSHandlerPreferredVersions']['LSHandlerRoleQLGenerator'];
    } else if ('LSHandlerRoleNone' in data) {
        role = 'None';
        appID = data['LSHandlerRoleNone'];
        appVersion = data['LSHandlerPreferredVersions']['LSHandlerRoleNone'];
    } else if ('LSHandlerRoleAll' in data) {
        role = 'All';
        appID = data['LSHandlerRoleAll'];
        appVersion = data['LSHandlerPreferredVersions']['LSHandlerRoleAll'];
    } else {
        throw new Error();
    }

    return {
        uti,
        role,
        appID,
        appVersion,
        type: 'DocumentType',
    };
}

export function deserializeDocumentType(
    data: DocumentType,
): DocumentTypeSchema {
    const LSHandlerContentType = data.uti;

    switch (data.role) {
        case 'Viewer':
            return {
                LSHandlerContentType,
                LSHandlerRoleViewer: data.appID,
                LSHandlerPreferredVersions: {
                    LSHandlerRoleViewer: data.appVersion,
                },
            };
        case 'Shell':
            return {
                LSHandlerContentType,
                LSHandlerRoleShell: data.appID,
                LSHandlerPreferredVersions: {
                    LSHandlerRoleShell: data.appVersion,
                },
            };
        case 'QLGenerator':
            return {
                LSHandlerContentType,
                LSHandlerRoleQLGenerator: data.appID,
                LSHandlerPreferredVersions: {
                    LSHandlerRoleQLGenerator: data.appVersion,
                },
            };
        case 'None':
            return {
                LSHandlerContentType,
                LSHandlerRoleNone: data.appID,
                LSHandlerPreferredVersions: {
                    LSHandlerRoleNone: data.appVersion,
                },
            };
        case 'All':
            return {
                LSHandlerContentType,
                LSHandlerRoleAll: data.appID,
                LSHandlerPreferredVersions: {
                    LSHandlerRoleAll: data.appVersion,
                },
            };
        default:
            throw new Error();
    }
}

export function serializeURLScheme(data: URLSchemeSchema): URLScheme {
    const scheme = data['LSHandlerURLScheme'];
    return {
        scheme,
        role: 'All',
        appID: data['LSHandlerRoleAll'],
        appVersion: data['LSHandlerPreferredVersions']['LSHandlerRoleAll'],
        type: 'URLScheme',
    };
}

export function deserializeURLScheme(data: URLScheme): URLSchemeSchema {
    return {
        LSHandlerURLScheme: data.scheme,
        LSHandlerRoleAll: data.appID,
        LSHandlerPreferredVersions: {
            LSHandlerRoleAll: data.appVersion,
        },
    };
}

export function serializeLSHandler(data: LSHandlerSchema): LSHandler {
    if ('LSHandlerContentType' in data) {
        return serializeDocumentType(data);
    } else if ('LSHandlerURLScheme' in data) {
        return serializeURLScheme(data);
    }
    throw new Error();
}

export function deserializeLSHandler(data: LSHandler): LSHandlerSchema {
    switch (data.type) {
        case 'DocumentType':
            return deserializeDocumentType(data);
        case 'URLScheme':
            return deserializeURLScheme(data);
        default:
            throw new Error();
    }
}

export function serializeLaunchServices(
    data: LaunchServicesSchema,
): LSHandler[] {
    return data.LSHandlers.map((lsHandler) => serializeLSHandler(lsHandler));
}

export function deserializeLaunchServices(
    data: LSHandler[],
): LaunchServicesSchema {
    return {
        LSHandlers: data.map((lsHandler) => deserializeLSHandler(lsHandler)),
    };
}

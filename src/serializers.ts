import {
    LSHandlerDocumentTypeSchema,
    LSHandlerSchema,
    LSHandlerURLSchemeSchema,
    LaunchServicesSchema,
} from '@/lib/macos/types';

export function serializeDocumentType(data: LSHandlerDocumentTypeSchema) {
    const uti = data.LSHandlerContentType;

    let role: string;
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

export function serializeURLScheme(data: LSHandlerURLSchemeSchema) {
    const urlScheme = data['LSHandlerURLScheme'];
    return {
        urlScheme,
        type: 'URLScheme',
    };
}

export function serializeLSHandler(data: LSHandlerSchema) {
    if ('LSHandlerContentType' in data) {
        return serializeDocumentType(data);
    } else if ('LSHandlerURLScheme' in data) {
        return serializeURLScheme(data);
    }
    throw new Error();
}

export function serializeLaunchServices(data: LaunchServicesSchema) {
    return data.LSHandlers.map((lsHandler) => serializeLSHandler(lsHandler));
}

export interface DocumentType {
    uti: string;
    role: 'Viewer' | 'Shell' | 'QLGenerator' | 'None' | 'All';
    appID: string;
    appVersion: string;
    type: 'DocumentType';
}

export interface URLScheme {
    scheme: string;
    role: 'All';
    appID: string;
    appVersion: '-';
    type: 'URLScheme';
}

export type LSHandler = DocumentType | URLScheme;

import type { DocumentType } from '@/src/types';

interface DefaultAssociationParams {
    utis?: { [key: string]: DocumentType['CFBundleTypeRole'] };
    urlSchemes?: string[];
}

export class DefaultAssociation {
    readonly utis: { [key: string]: DocumentType['CFBundleTypeRole'] };
    readonly urlSchemes: string[];

    constructor(params: DefaultAssociationParams) {
        this.utis = params.utis || {};
        this.urlSchemes = params.urlSchemes || [];
    }
}

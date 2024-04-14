interface DefaultAssociationParams {
    utis?: string[];
    urlSchemes?: string[];
}

export class DefaultAssociation {
    readonly utis: string[];
    readonly urlSchemes: string[];

    constructor(params: DefaultAssociationParams) {
        this.utis = params.utis || [];
        this.urlSchemes = params.urlSchemes || [];
    }
}

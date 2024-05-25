import { UTI as UTIClass } from '@/models/UTI';
import type { DefaultApp } from '@/types';

const UTI: typeof UTIClass = require('@/models/UTI').UTI;

export class AppAssociation {
    readonly utis: UTIClass[] = [];
    readonly urlSchemes: string[] = [];

    constructor(spec: Partial<DefaultApp>) {
        if (spec.utis) {
            this.utis =
                Object.entries(spec.utis).map(
                    ([id, role]) => new UTI(id, role),
                ) || [];
        }

        if (spec.urlSchemes) {
            this.urlSchemes = spec.urlSchemes || [];
        }
    }
}

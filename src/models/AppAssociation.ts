import { UTI as UTIClass } from '@/src/models/UTI';
import type { DefaultApp } from '@/src/types';

const UTI: typeof UTIClass = require('@/src/models/UTI').UTI;

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

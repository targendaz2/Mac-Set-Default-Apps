import { LSHandler } from '@/lib/macos/launchServices/interfaces';
import { LSHandlerSchema } from '@/lib/macos/launchServices/schemas';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';
import { documentTypeFactory, documentTypeSchemaFactory } from './documentType';
import { urlSchemeFactory, urlSchemeSchemaFactory } from './urlScheme';

class LSHandlerFactory extends Factory<LSHandler> {}

export const lsHandlerFactory = LSHandlerFactory.define(() => {
    const lsHandlerType = faker.helpers.arrayElement([
        'DocumentType',
        'URLScheme',
    ]);

    switch (lsHandlerType) {
        case 'DocumentType':
            return documentTypeFactory.build();
        case 'URLScheme':
            return urlSchemeFactory.build();
        default:
            throw new Error();
    }
});

class LSHandlerSchemaFactory extends Factory<LSHandlerSchema> {}

export const lsHandlerSchemaFactory = LSHandlerSchemaFactory.define(() => {
    const lsHandlerType = faker.helpers.arrayElement([
        'DocumentType',
        'URLScheme',
    ]);

    switch (lsHandlerType) {
        case 'DocumentType':
            return documentTypeSchemaFactory.build();
        case 'URLScheme':
            return urlSchemeSchemaFactory.build();
        default:
            throw new Error();
    }
});

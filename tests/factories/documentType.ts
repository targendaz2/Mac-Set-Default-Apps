import type { DocumentType } from '@/src/types';
import extensionsAndMIMETypes from '@/tests/factories/data/extensionsAndMIMETypes.json';
import roles from '@/tests/factories/data/roles.json';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class DocumentTypeFactory extends Factory<DocumentType> {}

export const documentTypeFactory = DocumentTypeFactory.define(() => {
    const [extension, mimeType] = faker.helpers.objectEntry(
        extensionsAndMIMETypes,
    );

    const role = faker.helpers.arrayElement(roles);

    return {
        CFBundleTypeExtensions: [extension],
        CFBundleTypeMIMETypes: [mimeType],
        CFBundleTypeRole: role as DocumentType['CFBundleTypeRole'],
    };
});

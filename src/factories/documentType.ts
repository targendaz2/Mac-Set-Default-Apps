import extensionsAndMIMETypes from '@/data/extensionsAndMIMETypes.json';
import roles from '@/data/roles.json';
import type { DocumentType } from '@/types';
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

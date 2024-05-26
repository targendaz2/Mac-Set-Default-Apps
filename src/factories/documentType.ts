import roles from '@/data/roles.json';
import utis from '@/data/utis.json';
import { DocumentType } from '@/lib/macos/launchServices/interfaces';
import { DocumentTypeSchema } from '@/lib/macos/launchServices/schemas';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class DocumentTypeFactory extends Factory<DocumentType> {}

export const documentTypeFactory = DocumentTypeFactory.define(() => {
    const appID =
        faker.internet.domainSuffix() +
        '.' +
        faker.internet.domainWord() +
        '.' +
        faker.word.noun();

    return {
        uti: faker.helpers.arrayElement(utis),
        role: faker.helpers.arrayElement(roles) as DocumentType['role'],
        appID,
        appVersion: faker.system.semver(),
        type: 'DocumentType' as DocumentType['type'],
    };
});

class DocumentTypeSchemaFactory extends Factory<DocumentTypeSchema> {}

export const documentTypeSchemaFactory = DocumentTypeSchemaFactory.define(
    () => {
        const documentType = documentTypeFactory.build();
        const LSHandlerContentType = documentType.uti;
        const { appID, appVersion } = documentType;

        switch (documentType.role) {
            case 'Viewer':
                return {
                    LSHandlerContentType,
                    LSHandlerRoleViewer: appID,
                    LSHandlerPreferredVersions: {
                        LSHandlerRoleViewer: appVersion,
                    },
                };
            case 'Shell':
                return {
                    LSHandlerContentType,
                    LSHandlerRoleShell: appID,
                    LSHandlerPreferredVersions: {
                        LSHandlerRoleShell: appVersion,
                    },
                };
            case 'QLGenerator':
                return {
                    LSHandlerContentType,
                    LSHandlerRoleQLGenerator: appID,
                    LSHandlerPreferredVersions: {
                        LSHandlerRoleQLGenerator: appVersion,
                    },
                };
            case 'None':
                return {
                    LSHandlerContentType,
                    LSHandlerRoleNone: appID,
                    LSHandlerPreferredVersions: {
                        LSHandlerRoleNone: appVersion,
                    },
                };
            case 'All':
                return {
                    LSHandlerContentType,
                    LSHandlerRoleAll: appID,
                    LSHandlerPreferredVersions: {
                        LSHandlerRoleAll: appVersion,
                    },
                };
            default:
                throw new Error();
        }
    },
);

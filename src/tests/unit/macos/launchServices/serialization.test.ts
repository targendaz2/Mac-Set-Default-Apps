import { documentTypeFactory, documentTypeSchemaFactory } from '@/factories';
import { run } from '@/lib/jxaRun';
import { DocumentType } from '@/lib/macos/launchServices/interfaces';
import { DocumentTypeSchema } from '@/lib/macos/launchServices/schemas';
import {
    deserializeDocumentType,
    serializeDocumentType,
} from '@/lib/macos/launchServices/serializers';
import { describe, expect, test } from '@jest/globals';

describe('Document Type serialization', () => {
    test('can serialize a valid Document Type schema', async () => {
        const documentTypeSchema = documentTypeSchemaFactory.build();

        const result = await run<DocumentType>(
            (
                documentTypeSchema: DocumentTypeSchema,
                serialize: typeof serializeDocumentType,
            ) => {
                return serialize(documentTypeSchema);
            },
            documentTypeSchema,
            serializeDocumentType,
        );

        ['uti', 'role', 'appID', 'appVersion'].forEach((prop) => {
            expect(result).toHaveProperty(prop);
        });
        expect(result.type).toBe('DocumentType');
    });

    test("can't serialize an invalid Document Type schema", async () => {
        const documentTypeSchema = {
            LSHandlerContentType: 'public.html',
            LSHandlerRoleFake: 'com.apple.Safari',
            LSHandlerPreferredVersions: {
                LSHandlerRoleFake: '14.0.0.23',
            },
        };

        expect(async () => {
            await run<DocumentType>(
                (
                    documentTypeSchema: DocumentTypeSchema,
                    serialize: typeof serializeDocumentType,
                ) => {
                    return serialize(documentTypeSchema);
                },
                documentTypeSchema,
                serializeDocumentType,
            );
        }).rejects.toThrowError();
    });

    test('can deserialize a valid Document Type', async () => {
        const documentType = documentTypeFactory.build();

        const result = await run<DocumentTypeSchema>(
            (
                documentType: DocumentType,
                deserialize: typeof deserializeDocumentType,
            ) => {
                return deserialize(documentType);
            },
            documentType,
            deserializeDocumentType,
        );

        [
            'LSHandlerContentType',
            'LSHandlerPreferredVersions',
            `LSHandlerRole${documentType.role}`,
        ].forEach((prop) => {
            expect(result).toHaveProperty(prop);
        });

        expect(
            // @ts-expect-error "DocumentTypeSchema doesn't support variable keys"
            result['LSHandlerPreferredVersions'][
                `LSHandlerRole${documentType.role}`
            ],
        ).toBe(documentType.appVersion);
    });

    test("can't deserialize an invalid Document Type", async () => {
        const documentType = {
            uti: 'public.html',
            role: 'FakeRole',
            appID: 'com.apple.Safari',
            appVersion: '14.0.0.23',
            type: 'FakeType',
        };

        expect(async () => {
            await run<DocumentType>(
                (
                    documentType: DocumentType,
                    deserialize: typeof deserializeDocumentType,
                ) => {
                    return deserialize(documentType);
                },
                documentType,
                deserializeDocumentType,
            );
        }).rejects.toThrowError();
    });
});

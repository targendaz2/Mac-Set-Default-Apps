import { documentTypeSchemaFactory } from '@/factories';
import { run } from '@/lib/jxaRun';
import { DocumentType } from '@/lib/macos/launchServices/interfaces';
import { DocumentTypeSchema } from '@/lib/macos/launchServices/schemas';
import { serializeDocumentType } from '@/lib/macos/launchServices/serializers';
import { describe, expect, test } from '@jest/globals';

describe('Document Type serialization', () => {
    test('can serialize a valid Document Type schema', async () => {
        const documentTypeSchema = documentTypeSchemaFactory.build();

        const result = await run<DocumentType>(
            (
                schema: DocumentTypeSchema,
                serialize: typeof serializeDocumentType,
            ) => {
                return serialize(schema);
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
                    schema: DocumentTypeSchema,
                    serialize: typeof serializeDocumentType,
                ) => {
                    return serialize(schema);
                },
                documentTypeSchema,
                serializeDocumentType,
            );
        }).rejects.toThrowError();
    });
});

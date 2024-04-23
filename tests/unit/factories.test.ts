// import cp from 'node:child_process';
import {
    documentTypeFactory,
    infoPlistFactory,
    urlTypeFactory,
} from '@/tests/factories';
import extensionsAndMIMETypes from '@/tests/factories/data/extensionsAndMIMETypes.json';
import { describe, expect, test } from '@jest/globals';

describe('Document Type factory tests', () => {
    test('can generate an object', () => {
        documentTypeFactory.build();
    });

    test('generated document type has a corresponding extension and MIME type', () => {
        const documentType = documentTypeFactory.build();
        const extension = documentType.CFBundleTypeExtensions![0];

        expect(documentType.CFBundleTypeMIMETypes![0]).toBe(
            // @ts-expect-error 'eslint thinks this is an any type for some reason'
            extensionsAndMIMETypes[extension],
        );
    });

    test('generated document type has a role', () => {
        const documentType = documentTypeFactory.build();
        expect(documentType.CFBundleTypeRole).toBeDefined;
    });
});

describe('URL Type factory tests', () => {
    test('can generate an object', () => {
        urlTypeFactory.build();
    });

    test('generated URL Type has a URL scheme', () => {
        const urlType = urlTypeFactory.build();
        expect(urlType.CFBundleURLSchemes).toBeDefined();
    });
});

describe('Info.plist factory tests', () => {
    test('can generate an object', () => {
        infoPlistFactory.build();
    });

    test('generated plist has uniform app name', () => {
        const infoPlist = infoPlistFactory.build();
        const name = infoPlist.CFBundleName;

        expect(infoPlist.CFBundleDisplayName).toBe(name);
        expect(infoPlist.CFBundleIdentifier).toContain(name);
    });

    test('can generate Info.plist with single Document Type', () => {
        const infoPlist = infoPlistFactory.documentTypes().build();
        expect(infoPlist.CFBundleDocumentTypes!.length).toBe(1);
    });

    test('can generate Info.plist with multiple Document Types', () => {
        const infoPlist = infoPlistFactory.documentTypes(3).build();
        expect(infoPlist.CFBundleDocumentTypes!.length).toBe(3);
    });

    test('can generate Info.plist with single URL Type', () => {
        const infoPlist = infoPlistFactory.urlTypes().build();
        expect(infoPlist.CFBundleURLTypes!.length).toBe(1);
    });

    test('can generate Info.plist with multiple URL Types', () => {
        const infoPlist = infoPlistFactory.urlTypes(3).build();
        expect(infoPlist.CFBundleURLTypes!.length).toBe(3);
    });

    test('can generate Info.plist with Document Types and URL Types', () => {
        const infoPlist = infoPlistFactory.documentTypes(3).urlTypes(2).build();

        expect(infoPlist.CFBundleDocumentTypes!.length).toBe(3);
        expect(infoPlist.CFBundleURLTypes!.length).toBe(2);
    });
});

// import cp from 'node:child_process';
import { infoPlistFactory, urlTypeFactory } from '@/tests/factories';
import { describe, expect, test } from '@jest/globals';

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

    test('can generate Info.plist with single URL Type', () => {
        const infoPlist = infoPlistFactory.urlTypes().build();
        expect(infoPlist.CFBundleURLTypes!.length).toBe(1);
    });

    test('can generate Info.plist with multiple URL Types', () => {
        const infoPlist = infoPlistFactory.urlTypes(3).build();
        expect(infoPlist.CFBundleURLTypes!.length).toBe(3);
    });
});

// import cp from 'node:child_process';
import { infoPlistFactory } from '@/tests/factories';
import { describe, expect, test } from '@jest/globals';

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
});

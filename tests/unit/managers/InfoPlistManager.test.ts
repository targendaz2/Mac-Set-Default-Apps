import { InfoPlistManager } from '@/src/managers';
import type { DocumentType, InfoPlist, URLType } from '@/src/types';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can get plist contents as JSON', async () => {
    const result = await run<InfoPlist>(
        (ManagerClass: typeof InfoPlistManager) => {
            const manager = new ManagerClass(
                '/Applications/Safari.app/Contents/Info.plist',
            );
            return manager.contents;
        },
        InfoPlistManager,
    );

    expect(result.CFBundleDisplayName).toBe('Safari');
    expect(result.CFBundleIdentifier).toBe('com.apple.Safari');
    expect(result.CFBundleShortVersionString).toMatch(/\d{1,2}\.\d{1,2}/);
});

test('can get document types from plist', async () => {
    const result = await run<DocumentType[]>(
        (ManagerClass: typeof InfoPlistManager) => {
            const manager = new ManagerClass(
                '/Applications/Safari.app/Contents/Info.plist',
            );
            return manager.documentTypes;
        },
        InfoPlistManager,
    );

    expect(result[0].CFBundleTypeMIMETypes).toContain('text/css');
    expect(result[0].CFBundleTypeExtensions).toContain('css');
    expect(result[0].CFBundleTypeRole).toBe('Viewer');
});

test('can get URL types from plist', async () => {
    const result = await run<URLType[]>(
        (ManagerClass: typeof InfoPlistManager) => {
            const manager = new ManagerClass(
                '/Applications/Safari.app/Contents/Info.plist',
            );
            return manager.urlTypes;
        },
        InfoPlistManager,
    );

    expect(result[0].CFBundleURLSchemes).toContain('http');
    expect(result[0].CFBundleURLSchemes).toContain('https');
});

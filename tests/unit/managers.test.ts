import { PathLike } from 'node:fs';
import { describe, expect, test } from '@jest/globals';
import { AppManager, InfoPlistManager, UtiManager } from '../../src/managers';
import { App, Uti } from '../../src/models';
import type { DocumentType, InfoPlist, UrlType } from '../../src/types';
import { run } from '../helpers/jxaRun';

describe('app manager tests', () => {
    test('can get app name', async () => {
        const result = await run<string>((ManagerClass: typeof AppManager) => {
            const manager = new ManagerClass('com.apple.Safari');
            return manager.name;
        }, AppManager);

        expect(result).toBe('Safari');
    });

    test('can get app bundle ID', async () => {
        const result = await run<string>((ManagerClass: typeof AppManager) => {
            const manager = new ManagerClass('com.apple.Safari');
            return manager.id;
        }, AppManager);

        expect(result).toBe('com.apple.Safari');
    });

    test('can get app version', async () => {
        const result = await run<string>((ManagerClass: typeof AppManager) => {
            const manager = new ManagerClass('com.apple.Safari');
            return manager.version;
        }, AppManager);

        expect(result).toMatch(/\d{1,2}\.\d{1,2}/);
    });

    test('can get app path', async () => {
        const result = await run<PathLike>(
            (ManagerClass: typeof AppManager) => {
                const manager = new ManagerClass('com.apple.Safari');
                return manager.path;
            },
            AppManager,
            App,
        );

        expect(result).toBe('/Applications/Safari.app');
    });

    test('can create App instance', async () => {
        const result = await run<App>(
            (ManagerClass: typeof AppManager, _) => {
                const manager = new ManagerClass('com.apple.Safari');
                return manager.create();
            },
            AppManager,
            App,
        );

        const newApp = new App(
            result.name,
            result.id,
            result.version,
            result.path,
        );

        expect(result).toMatchObject({ ...newApp });
    });
});

describe('Info.plist manager tests', () => {
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
        const result = await run<UrlType[]>(
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
});

describe('UTI manager tests', () => {
    test('can return UTI ID', async () => {
        const result = await run<string>((ManagerClass: typeof UtiManager) => {
            const manager = new ManagerClass('public.html');
            return manager.id;
        }, UtiManager);

        expect(result).toBe('public.html');
    });

    test('can get UTI tags', async () => {
        const result = await run<string>((ManagerClass: typeof UtiManager) => {
            const manager = new ManagerClass('public.html');
            return manager.tags;
        }, UtiManager);

        expect(result).toContain('htm');
        expect(result).toContain('html');
        expect(result).toContain('text/html');
    });

    test('can create Uti instance', async () => {
        const result = await run<Uti>(
            (ManagerClass: typeof UtiManager, _) => {
                const manager = new ManagerClass('public.html');
                return manager.create();
            },
            UtiManager,
            Uti,
        );

        const newUti = new Uti(result.id, result.tags);

        expect(result).toMatchObject({ ...newUti });
    });
});

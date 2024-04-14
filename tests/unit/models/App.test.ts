import { PathLike } from 'node:fs';
import { App, UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { describe, expect, test } from '@jest/globals';

describe('app model instantiation tests', () => {
    test('can get app name', async () => {
        const result = await run<string>((ModelClass: typeof App) => {
            const app = new ModelClass('com.apple.Safari');
            return app.name;
        }, App);

        expect(result).toBe('Safari');
    });

    test('can get app bundle ID', async () => {
        const result = await run<string>((ModelClass: typeof App) => {
            const app = new ModelClass('com.apple.Safari');
            return app.id;
        }, App);

        expect(result).toBe('com.apple.Safari');
    });

    test('can get app version', async () => {
        const result = await run<string>((ModelClass: typeof App) => {
            const app = new ModelClass('com.apple.Safari');
            return app.version;
        }, App);

        expect(result).toMatch(/\d{1,2}\.\d{1,2}/);
    });

    test('can get app path', async () => {
        const result = await run<PathLike>((ModelClass: typeof App) => {
            const manager = new ModelClass('com.apple.Safari');
            return manager.path;
        }, App);

        expect(result).toBe('/Applications/Safari.app');
    });

    test("can get path to app's Info.plist", async () => {
        const result = await run<PathLike>((ModelClass: typeof App) => {
            const app = new ModelClass('com.apple.Safari');
            return app.infoPlist;
        }, App);

        expect(result).toBe('/Applications/Safari.app/Contents/Info.plist');
    });

    test("can get app's supported document types", async () => {
        const result = await run<{ [key: string]: string }>(
            (ModelClass: typeof App) => {
                const app = new ModelClass('com.apple.Safari');
                return app.documentTypes;
            },
            App,
        );

        expect(result['text/css']).toBe('Viewer');
        expect(result['css']).toBe('Viewer');
        expect(result['text/html']).toBe('Viewer');
        expect(result['html']).toBe('Viewer');
        expect(result['application/pdf']).toBe('Viewer');
    });

    test("can get app's supported URL schemes", async () => {
        const result = await run<string[]>((ModelClass: typeof App) => {
            const app = new ModelClass('com.apple.Safari');
            return app.urlSchemes;
        }, App);

        expect(result).toContain('http');
        expect(result).toContain('https');
    });
});

describe('support checking tests', () => {
    test('can confirm an app supports a UTI', async () => {
        const result = await run<string[]>(
            (AppClass: typeof App, UTIClass: typeof UTI) => {
                const uti = new UTIClass('public.html');

                const app = new AppClass('com.apple.Safari');
                return app.supportsUTI(uti, 'Viewer');
            },
            App,
            UTI,
        );

        expect(result).toBeTruthy();
    });

    test('can confirm an app supports a URL scheme', async () => {
        const result = await run<string[]>((AppClass: typeof App) => {
            const app = new AppClass('com.apple.Safari');
            return app.supportsURLScheme('http');
        }, App);

        expect(result).toBeTruthy();
    });
});

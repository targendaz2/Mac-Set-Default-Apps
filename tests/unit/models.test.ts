import { PathLike } from 'node:fs';
import { App, UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { describe, expect, test } from '@jest/globals';

describe('App model tests', () => {
    test('can create App instance', async () => {
        const result = await run<App>((AppClass: typeof App) => {
            const app = new AppClass(
                'Safari',
                'com.apple.Safari',
                '17.4',
                '/Applications/Safari.app',
            );
            return app;
        }, App);

        expect(result).toMatchObject({
            name: 'Safari',
            id: 'com.apple.Safari',
            version: '17.4',
            path: '/Applications/Safari.app',
        });
    });

    test("can get path to app's Info.plist", async () => {
        const result = await run<PathLike>((AppClass: typeof App) => {
            const app = new AppClass(
                'Safari',
                'com.apple.Safari',
                '17.4',
                '/Applications/Safari.app',
            );
            return app.infoPlist;
        }, App);

        expect(result).toBe('/Applications/Safari.app/Contents/Info.plist');
    });
});

describe('UTI model tests', () => {
    test('can create UTI instance', async () => {
        const result = await run<UTI>((UTIClass: typeof UTI) => {
            const UTI = new UTIClass('public.html', [
                'html',
                'htm',
                'text/html',
            ]);
            return UTI;
        }, UTI);

        expect(result).toMatchObject({
            id: 'public.html',
            tags: ['html', 'htm', 'text/html'],
        });
    });
});

import { PathLike } from 'node:fs';
import { describe, expect, test } from '@jest/globals';
import App from '../src/models/App';
import { run } from './helpers/jxaRun';

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

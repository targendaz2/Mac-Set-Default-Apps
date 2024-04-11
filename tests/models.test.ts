import { PathLike } from 'node:fs';
import { describe, expect, test } from '@jest/globals';
import App from '../src/models/App';
import { run } from './helpers/jxaRun';

describe('App model tests', () => {
    test('gets app name on instantiation', async () => {
        const result = await run<string>((AppClass: typeof App) => {
            const app = new AppClass('com.apple.Safari');
            return app.name;
        }, App);

        expect(result).toBe('Safari');
    });

    test('stores app ID on instantiation', async () => {
        const result = await run<string>((AppClass: typeof App) => {
            const app = new AppClass('com.apple.Safari');
            return app.id;
        }, App);

        expect(result).toBe('com.apple.Safari');
    });

    test('gets app version on instantiation', async () => {
        const result = await run<string>((AppClass: typeof App) => {
            const app = new AppClass('com.apple.Safari');
            return app.version;
        }, App);

        expect(result).toMatch(/\d{1,2}\.\d{1,2}/);
    });

    test('gets path to app on instantiation', async () => {
        const result = await run<PathLike>((AppClass: typeof App) => {
            const app = new AppClass('com.apple.Safari');
            return app.path;
        }, App);

        expect(result).toBe('/Applications/Safari.app');
    });
});

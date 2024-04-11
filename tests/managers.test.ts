import { PathLike } from 'node:fs';
import { describe, expect, test } from '@jest/globals';
import AppManager from '../src/managers/AppManager';
import App from '../src/models/App';
import { run } from './helpers/jxaRun';

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
                return manager.build();
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

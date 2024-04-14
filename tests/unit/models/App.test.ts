import { PathLike } from 'node:fs';
import { App } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

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

test("can get app's supported URL schemes", async () => {
    const result = await run<string[]>((ModelClass: typeof App) => {
        const app = new ModelClass('com.apple.Safari');
        return app.urlSchemes;
    }, App);

    expect(result).toContain('http');
    expect(result).toContain('https');
});

import { UtiManager } from '@/src/managers';
import { Uti } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

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

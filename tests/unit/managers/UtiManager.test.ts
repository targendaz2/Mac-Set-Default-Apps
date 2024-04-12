import { UTIManager } from '@/src/managers';
import { UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can return UTI ID', async () => {
    const result = await run<string>((ManagerClass: typeof UTIManager) => {
        const manager = new ManagerClass('public.html');
        return manager.id;
    }, UTIManager);

    expect(result).toBe('public.html');
});

test('can get UTI tags', async () => {
    const result = await run<string>((ManagerClass: typeof UTIManager) => {
        const manager = new ManagerClass('public.html');
        return manager.tags;
    }, UTIManager);

    expect(result).toContain('htm');
    expect(result).toContain('html');
    expect(result).toContain('text/html');
});

test('can create UTI instance', async () => {
    const result = await run<UTI>(
        (ManagerClass: typeof UTIManager, _) => {
            const manager = new ManagerClass('public.html');
            return manager.create();
        },
        UTIManager,
        UTI,
    );

    const newUTI = new UTI(result.id, result.tags);

    expect(result).toMatchObject({ ...newUTI });
});

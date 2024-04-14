import { UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can return UTI ID', async () => {
    const result = await run<string>((UTIClass: typeof UTI) => {
        const uti = new UTIClass('public.html');
        return uti.id;
    }, UTI);

    expect(result).toBe('public.html');
});

test('can get UTI tags', async () => {
    const result = await run<string>((UTIClass: typeof UTI) => {
        const uti = new UTIClass('public.html');
        return uti.tags;
    }, UTI);

    expect(result).toContain('htm');
    expect(result).toContain('html');
    expect(result).toContain('text/html');
});

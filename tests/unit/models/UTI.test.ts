import { UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can return UTI ID', async () => {
    const result = await run<string>((UTIClass: typeof UTI) => {
        const uti = new UTIClass('public.html', 'All');
        return uti.id;
    }, UTI);

    expect(result).toBe('public.html');
});

test('can return UTI role', async () => {
    const result = await run<string>((UTIClass: typeof UTI) => {
        const uti = new UTIClass('public.html', 'Viewer');
        return uti.role;
    }, UTI);

    expect(result).toBe('Viewer');
});

test('can get UTI tags', async () => {
    const result = await run<string>((UTIClass: typeof UTI) => {
        const uti = new UTIClass('public.html', 'All');
        return uti.tags;
    }, UTI);

    expect(result).toContain('htm');
    expect(result).toContain('html');
    expect(result).toContain('text/html');
});

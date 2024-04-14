import { UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can create UTI instance', async () => {
    const result = await run<UTI>((UTIClass: typeof UTI) => {
        const UTI = new UTIClass('public.html', ['html', 'htm', 'text/html']);
        return UTI;
    }, UTI);

    expect(result).toMatchObject({
        id: 'public.html',
        tags: ['html', 'htm', 'text/html'],
    });
});

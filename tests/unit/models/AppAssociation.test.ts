import { AppAssociation, UTI } from '@/src/models';
import { run } from '@/tests/helpers/jxaRun';
import { expect, test } from '@jest/globals';

test('can instantiate with single UTI', async () => {
    const result = await run<UTI[]>(
        (ModelClass: typeof AppAssociation, _) => {
            const defaultPDF = new ModelClass({
                utis: { 'com.adobe.pdf': 'All' },
            });
            return defaultPDF.utis;
        },
        AppAssociation,
        UTI,
    );

    const uti = await run<UTI>((ModelClass: typeof UTI) => {
        return new ModelClass('com.adobe.pdf', 'All');
    }, UTI);

    expect(result).toContainEqual(uti);
});

test("can instantiate with multiple UTI's", async () => {
    const result = await run<UTI[]>(
        (ModelClass: typeof AppAssociation, _) => {
            const defaultApp = new ModelClass({
                utis: {
                    'com.apple.ical.ics': 'All',
                    'com.apple.ical.vcs': 'All',
                },
            });
            return defaultApp.utis;
        },
        AppAssociation,
        UTI,
    );

    const utis = await run<UTI[]>((ModelClass: typeof UTI) => {
        return [
            new ModelClass('com.apple.ical.ics', 'All'),
            new ModelClass('com.apple.ical.vcs', 'All'),
        ];
    }, UTI);

    expect(result).toContainEqual(utis[0]);
    expect(result).toContainEqual(utis[1]);
});

test('can instantiate with URL schemes', async () => {
    const result = await run<string[]>((ModelClass: typeof AppAssociation) => {
        const defaultMail = new ModelClass({
            urlSchemes: ['mailto'],
        });
        return defaultMail.urlSchemes;
    }, AppAssociation);

    expect(result).toContain('mailto');
});

test('can instantiate', async () => {
    const result = await run<AppAssociation>(
        (ModelClass: typeof AppAssociation, _) => {
            const defaultApp = new ModelClass({
                utis: {
                    'public.html': 'Viewer',
                    'public.url': 'Viewer',
                    'public.xhtml': 'Viewer',
                },
                urlSchemes: ['http', 'https'],
            });
            return defaultApp;
        },
        AppAssociation,
        UTI,
    );

    const utis = await run<UTI[]>((ModelClass: typeof UTI) => {
        return [
            new ModelClass('public.html', 'Viewer'),
            new ModelClass('public.url', 'Viewer'),
            new ModelClass('public.xhtml', 'Viewer'),
        ];
    }, UTI);

    expect(result.utis).toContainEqual(utis[0]);
    expect(result.utis).toContainEqual(utis[1]);
    expect(result.utis).toContainEqual(utis[2]);
    expect(result.urlSchemes).toContainEqual('http');
    expect(result.urlSchemes).toContainEqual('https');
});

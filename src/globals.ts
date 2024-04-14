import type { DefaultAssociation as DefaultAssociationClass } from './models/DefaultAssociation';

const DefaultAssociation: typeof DefaultAssociationClass =
    require('@/src/models/DefaultAssociation').DefaultAssociation;

export const browserAssoc = new DefaultAssociation({
    utis: {
        'public.html': 'Viewer',
        'public.url': 'Viewer',
        'public.xhtml': 'Viewer',
    },
    urlSchemes: ['http', 'https'],
});

export const calendarAssoc = new DefaultAssociation({
    utis: {
        'com.apple.ical.ics': 'All',
        'com.apple.ical.vcs': 'All',
    },
    urlSchemes: ['webcal'],
});

export const mailAssoc = new DefaultAssociation({
    urlSchemes: ['mailto'],
});

export const pdfAssoc = new DefaultAssociation({
    utis: {
        'com.adobe.pdf': 'All',
    },
});

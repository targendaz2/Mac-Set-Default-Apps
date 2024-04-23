import type { DocumentType } from '@/src/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class DocumentTypeFactory extends Factory<DocumentType> {}

export const documentTypeFactory = DocumentTypeFactory.define(() => {
    const [extension, mimeType] = faker.helpers.objectEntry({
        aac: 'audio/aac',
        css: 'text/css',
        csv: 'text/csv',
        gif: 'image/gif',
        gz: 'application/gzip',
        heic: 'image/heic',
        heif: 'image/heic',
        htm: 'text/html',
        html: 'text/html',
        jpeg: 'image/jpeg',
        jpg: 'image/jpeg',
        js: 'text/javascript',
        json: 'application/json',
        m4a: 'audio/aac',
        md: 'text/markdown',
        mp4: 'video/mp4',
        pdf: 'application/pdf',
        png: 'image/png',
        rtf: 'application/rtf',
        tgz: 'application/gzip',
        tif: 'image/tiff',
        tiff: 'image/tiff',
        txt: 'text/plain',
        xhtml: 'application/xhtml+xml',
        xml: 'application/xml',
        yaml: 'application/yaml',
        yml: 'application/yaml',
        zip: 'application/zip',
    });

    const role = faker.helpers.arrayElement([
        'Editor',
        'Viewer',
        'Shell',
        'QLGenerator',
        'None',
        'All',
    ]);

    return {
        CFBundleTypeExtensions: [extension],
        CFBundleTypeMIMETypes: [mimeType],
        CFBundleTypeRole: role as DocumentType['CFBundleTypeRole'],
    };
});

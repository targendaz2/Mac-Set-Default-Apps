import roles from '@/data/roles.json';
import urlSchemes from '@/data/urlSchemes.json';
import utis from '@/data/utis.json';
import type {
    LSHandler,
    LSHandlerDocumentType,
    LSHandlerURLScheme,
} from '@/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class LSHandlerFactory extends Factory<
    LSHandler,
    { documentType?: boolean; urlScheme?: boolean }
> {
    buildDocumentType() {
        return this.transient({
            documentType: true,
        }).build() as LSHandlerDocumentType;
    }

    buildURLScheme() {
        return this.transient({
            urlScheme: true,
        }).build() as LSHandlerURLScheme;
    }
}

export const lsHandlerFactory = LSHandlerFactory.define(
    ({ transientParams }) => {
        const appName = faker.word.noun();
        const domain = faker.internet.domainName();
        const bundleId = domain.split(',').reverse().join('.') + '.' + appName;

        let role = '';
        const lsHandler = {
            LSHandlerPreferredVersions: {},
        };

        if (transientParams.documentType) {
            role = faker.helpers.arrayElement(roles);
            const uti = faker.helpers.arrayElement(utis);

            // @ts-expect-error 'ignoring implicit any error'
            lsHandler['LSHandlerContentType'] = uti;
        } else if (transientParams.urlScheme) {
            role = 'All';
            const urlScheme = faker.helpers.arrayElement(urlSchemes);

            // @ts-expect-error 'ignoring implicit any error'
            lsHandler['LSHandlerURLScheme'] = urlScheme;
        } else {
            throw new Error();
        }

        // @ts-expect-error 'ignoring implicit any error'
        lsHandler[`LSHandlerRole${role}`] = bundleId;

        // @ts-expect-error 'ignoring implicit any error'
        lsHandler.LSHandlerPreferredVersions[`LSHandlerRole${role}`] = '-';

        return lsHandler as LSHandler;
    },
);

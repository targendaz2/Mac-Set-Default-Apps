import urlSchemes from '@/data/urlSchemes.json';
import { URLScheme } from '@/lib/macos/launchServices/interfaces';
import { URLSchemeSchema } from '@/lib/macos/launchServices/schemas';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class URLSchemeFactory extends Factory<URLScheme> {}

export const urlSchemeFactory = URLSchemeFactory.define(() => {
    const appID =
        faker.internet.domainSuffix() +
        '.' +
        faker.internet.domainWord() +
        '.' +
        faker.word.noun();

    return {
        scheme: faker.helpers.arrayElement(urlSchemes),
        role: 'All' as URLScheme['role'],
        appID,
        appVersion: '-' as URLScheme['appVersion'],
        type: 'URLScheme' as URLScheme['type'],
    };
});

class URLSchemeSchemaFactory extends Factory<URLSchemeSchema> {}

export const urlSchemeSchemaFactory = URLSchemeSchemaFactory.define(() => {
    const urlScheme = urlSchemeFactory.build();
    const { scheme, appID, appVersion } = urlScheme;

    return {
        LSHandlerURLScheme: scheme,
        LSHandlerRoleAll: appID,
        LSHandlerPreferredVersions: {
            LSHandlerRoleAll: appVersion,
        },
    };
});

import type { URLType } from '@/src/types';
import urlSchemes from '@/tests/factories/data/urlSchemes.json';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class URLTypeFactory extends Factory<URLType> {}

export const urlTypeFactory = URLTypeFactory.define(() => {
    const urlScheme = faker.helpers.arrayElement(urlSchemes);

    return {
        CFBundleURLSchemes: [urlScheme],
    };
});

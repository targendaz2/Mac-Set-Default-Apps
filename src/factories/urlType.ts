import urlSchemes from '@/data/urlSchemes.json';
import type { URLType } from '@/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class URLTypeFactory extends Factory<URLType> {}

export const urlTypeFactory = URLTypeFactory.define(() => {
    const urlScheme = faker.helpers.arrayElement(urlSchemes);

    return {
        CFBundleURLSchemes: [urlScheme],
    };
});

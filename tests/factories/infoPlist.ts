import type { InfoPlist } from '@/src/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class InfoPlistFactory extends Factory<InfoPlist, { urlSchemes?: boolean }> {}

export const infoPlistFactory = InfoPlistFactory.define(() => {
    const appName = faker.word.noun();
    const domain = faker.internet.domainName();
    const bundleId = domain.split(',').reverse().join('.') + '.' + appName;

    const infoPlist = {
        CFBundleDisplayName: appName,
        CFBundleIdentifier: bundleId,
        CFBundleName: appName,
        CFBundleShortVersionString: faker.system.semver(),
    };

    return infoPlist;
});

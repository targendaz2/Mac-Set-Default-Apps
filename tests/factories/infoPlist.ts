import type { InfoPlist } from '@/src/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

export const infoPlistFactory = Factory.define<InfoPlist>(() => {
    const appName = faker.word.noun();
    const domain = faker.internet.domainName();
    const bundleId = domain.split(',').reverse().join('.') + '.' + appName;

    return {
        CFBundleDisplayName: appName,
        CFBundleIdentifier: bundleId,
        CFBundleName: appName,
        CFBundleShortVersionString: faker.system.semver(),
    };
});

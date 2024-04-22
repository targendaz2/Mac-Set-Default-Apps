import type { InfoPlist } from '@/src/types';
import { urlTypeFactory } from '@/tests/factories/urlType';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class InfoPlistFactory extends Factory<InfoPlist, { urlTypes?: number }> {
    urlTypes(count: number = 1) {
        return this.transient({ urlTypes: count });
    }
}

export const infoPlistFactory = InfoPlistFactory.define(
    ({ transientParams }) => {
        const appName = faker.word.noun();
        const domain = faker.internet.domainName();
        const bundleId = domain.split(',').reverse().join('.') + '.' + appName;

        const infoPlist: InfoPlist = {
            CFBundleDisplayName: appName,
            CFBundleIdentifier: bundleId,
            CFBundleName: appName,
            CFBundleShortVersionString: faker.system.semver(),
        };

        if (transientParams.urlTypes) {
            infoPlist.CFBundleURLTypes = urlTypeFactory.buildList(
                transientParams.urlTypes,
            );
        }

        return infoPlist;
    },
);

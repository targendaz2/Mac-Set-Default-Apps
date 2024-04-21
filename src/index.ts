import { arg } from '@/src/args';
import { AppAssociation } from '@/src/models';
import type { Config } from '@/src/types';

const config: Config = require('@/src/config.json');

function main() {
    const args = arg({
        '--browser': Boolean,
        '--calendar': Boolean,
        '--mail': Boolean,
        '--pdf': Boolean,
        '--feu': Boolean,
        '--fut': Boolean,
        '--force': Boolean,
        '-f': '--force',
        '-l': String,
    });

    const appAssocs = [];

    if (args['--browser'])
        appAssocs.push(
            new AppAssociation(config.defaultAppRequirements.browser),
        );

    if (args['--calendar'])
        appAssocs.push(
            new AppAssociation(config.defaultAppRequirements.calendar),
        );

    if (args['--mail'])
        appAssocs.push(new AppAssociation(config.defaultAppRequirements.mail));

    if (args['--pdf'])
        appAssocs.push(new AppAssociation(config.defaultAppRequirements.pdf));
}

main();

import type { URLType } from '@/src/types';
import { faker } from '@faker-js/faker';
import { Factory } from 'fishery';

class URLTypeFactory extends Factory<URLType> {}

export const urlTypeFactory = URLTypeFactory.define(() => {
    const urlScheme = faker.helpers.arrayElement([
        'chrome',
        'facetime',
        'fax',
        'file',
        'ftp',
        'git',
        'http',
        'https',
        'imap',
        'jabber',
        'ldap',
        'ldaps',
        'mailto',
        'maps',
        'ms-excel',
        'ms-powerpoint',
        'ms-remotedesktop',
        'ms-word',
        'msteams',
        'news',
        'nfs',
        'notes',
        'sftp',
        'skype',
        'slack',
        'smb',
        'smtp',
        'spotify',
        'ssh',
        'steam',
        'things',
        'vnc',
        'vscode',
        'webcal',
        'zoommtg',
    ]);

    return {
        CFBundleURLSchemes: [urlScheme],
    };
});

import { fs } from '@/lib/macos';
import { LaunchServicesSchema } from './schemas';

export const launchServices = {
    read: (forUser: string): LaunchServicesSchema | undefined => {
        const username = forUser;
        const path =
            '/Users/' +
            username +
            '/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist';

        if (fs.pathExists(path)) {
            return fs.readPlist(path);
        }
    },
};

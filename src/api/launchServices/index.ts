import { LaunchServicesSchema } from '@/api/launchServices/schema';
import { os } from '@/lib/os';
import '@jxa/global-type';

class LaunchServicesAPI {
    readHandlers(forUser: string) {
        const username = forUser;
        const lsPath =
            '/Users/' +
            username +
            '/Library/Preferences/com.apple.LaunchServices/com.apple.launchservices.secure.plist';

        if (os.pathExists(lsPath)) {
            const contents = os.readPlist(lsPath);
            return LaunchServicesSchema.parse(contents);
        }
    }
}

export const lsClient = new LaunchServicesAPI();

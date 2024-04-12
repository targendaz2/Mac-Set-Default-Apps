import '@/tests/extensions/fs.ext';
import { describe, expect, test } from '@jest/globals';

describe('lsregister tests', () => {
    test('command exists', async () => {
        const path =
            '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister';

        expect(path).toExist();
    });
});

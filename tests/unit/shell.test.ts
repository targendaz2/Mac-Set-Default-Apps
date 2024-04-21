import '@/tests/extensions/fs.ext';
import { expect, test } from '@jest/globals';

test('lsregister command exists', () => {
    const path =
        '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister';

    expect(path).toExist();
});

test('zsh command exists', () => {
    const path = '/bin/zsh';
    expect(path).toExist();
});

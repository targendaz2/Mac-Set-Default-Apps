import { describe, expect, test } from '@jest/globals';
import './extensions/fs.ext';

// import { lsregister } from '../src/utils';
// import { run } from './helpers/jxaRun';

describe('lsregister tests', () => {
    test('command exists', async () => {
        const path =
            '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister';

        expect(path).toExist();
    });

    // test('can dump database', async () => {
    //     const result = await run<string>((utilFn: typeof lsregister) => {
    //         return utilFn({ dump: 'Type' });
    //     }, lsregister);

    //     const actual = result;
    //     const expected = cp
    //         .execSync(
    //             '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -dump Type',
    //         )
    //         .toString();

    //     expect(actual).toBe(expected);
    // });
});

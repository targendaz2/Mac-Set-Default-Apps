import type { Config } from '@/src/types';
import '@/tests/extensions/fs.ext';
import { expect, test } from '@jest/globals';

const config: Config = require('@/src/config.json');

test('lsregister binary should exist', () => {
    expect(config.systemPaths['lsregister']).toExist();
});

test('mdfind binary should exist', () => {
    const path = '/usr/bin/mdfind';
    expect(path).toExist();
});

test('osascript binary should exist', () => {
    const path = '/usr/bin/osascript';
    expect(path).toExist();
});

test('zsh binary should exist', () => {
    const path = '/bin/zsh';
    expect(path).toExist();
});

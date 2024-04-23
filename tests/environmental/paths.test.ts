import type { Config } from '@/src/types';
import '@/tests/extensions/fs.ext';
import { expect, test } from '@jest/globals';

const config: Config = require('@/src/config.json');

test('User template should exist', () => {
    expect(config.systemPaths['userTemplate']).toExist();
});

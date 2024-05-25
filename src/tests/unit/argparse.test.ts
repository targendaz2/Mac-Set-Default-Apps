// import cp from 'node:child_process';
import cp from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { getArgs } from '@/lib/args/getter';
// import { run } from '@/tests/helpers/jxaRun';
import { describe, expect, test } from '@jest/globals';

describe('argument fetching tests', () => {
    test('can get command line arguments', async () => {
        const scriptFile = path.join(fs.mkdtempSync(os.tmpdir()), 'script.js');
        fs.writeFileSync(scriptFile, `${getArgs.toString()}\ngetArgs();`);

        const result = cp
            .execFileSync(
                'osascript',
                [
                    '-l',
                    'JavaScript',
                    scriptFile,
                    'com.apple.Safari',
                    '--browser',
                    '--feu',
                ],
                {
                    encoding: 'utf8',
                },
            )
            .trim()
            .split(', ');

        expect(result).toContain('com.apple.Safari');
        expect(result).toContain('--browser');
        expect(result).toContain('--feu');
    });
});

import fs, { PathLike } from 'node:fs';
import { expect } from '@jest/globals';
import { MatcherFunction } from 'expect';

const toExist: MatcherFunction = function (actual) {
    const typedActual = actual as PathLike;
    const pass = fs.existsSync(typedActual);

    return {
        pass,
        message: pass
            ? () => `"${typedActual}" exists`
            : () => `"${typedActual}" does not exist`,
    };
};

expect.extend({
    toExist,
});

declare module 'expect' {
    interface AsymmetricMatchers {
        /** Checks that a file path exists. */
        toExist(): void;
    }
    interface Matchers<R> {
        /** Checks that a file path exists. */
        toExist(): R;
    }
}

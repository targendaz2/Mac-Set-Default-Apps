// Based heavily on @jxa/run
// https://github.com/JXA-userland/JXA/tree/master/packages/%40jxa/run
import { execFile } from 'node:child_process';

export function runJXACode(jxaCode: string) {
    return executeInOsa(jxaCode);
}

export function run<R>(
    jxaCodeFunction: (...args: any[]) => void,
    ...args: any[]
): Promise<R>;
export function run<R, A1>(
    jxaCodeFunction: (a1: A1) => void,
    a1: A1,
): Promise<R>;
export function run<R, A1, A2>(
    jxaCodeFunction: (a1: A1, a2: A2) => void,
    a1: A1,
    a2: A2,
): Promise<R>;
export function run<R, A1, A2, A3>(
    jxaCodeFunction: (a1: A1, a2: A2, a3: A3) => void,
    a1: A1,
    a2: A2,
    a3: A3,
): Promise<R>;
export function run<R, A1, A2, A3, A4>(
    jxaCodeFunction: (a1: A1, a2: A2, a3: A3, a4: A4) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
): Promise<R>;
export function run<R, A1, A2, A3, A4, A5>(
    jxaCodeFunction: (a1: A1, a2: A2, a3: A3, a4: A4, a5: A5) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
    a5: A5,
): Promise<R>;
export function run<R, A1, A2, A3, A4, A5, A6>(
    jxaCodeFunction: (a1: A1, a2: A2, a3: A3, a4: A4, a5: A5, a6: A6) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
    a5: A5,
    a6: A6,
): Promise<R>;
export function run<R, A1, A2, A3, A4, A5, A6, A7>(
    jxaCodeFunction: (
        a1: A1,
        a2: A2,
        a3: A3,
        a4: A4,
        a5: A5,
        a6: A6,
        a7: A7,
    ) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
    a5: A5,
    a6: A6,
    a7: A7,
): Promise<R>;
export function run<R, A1, A2, A3, A4, A5, A6, A7, A8>(
    jxaCodeFunction: (
        a1: A1,
        a2: A2,
        a3: A3,
        a4: A4,
        a5: A5,
        a6: A6,
        a7: A7,
        a8: A8,
    ) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
    a5: A5,
    a6: A6,
    a7: A7,
    a8: A8,
): Promise<R>;
export function run<R, A1, A2, A3, A4, A5, A6, A7, A8, A9>(
    jxaCodeFunction: (
        a1: A1,
        a2: A2,
        a3: A3,
        a4: A4,
        a5: A5,
        a6: A6,
        a7: A7,
        a8: A8,
        a9: A9,
    ) => void,
    a1: A1,
    a2: A2,
    a3: A3,
    a4: A4,
    a5: A5,
    a6: A6,
    a7: A7,
    a8: A8,
    a9: A9,
): Promise<R>;
export function run(jxaCodeFunction: (...args: any[]) => void, ...args: any[]) {
    const parsedArgs = args
        .map((value) => (value.name ? value.name : `"${value}"`))
        .toString();
    const code = `
        ${args.filter((value) => value.name).join('\n')}
        var fn   = (${jxaCodeFunction.toString()});
        var out  = fn(${parsedArgs});
        JSON.stringify({ result: out });
        `;
    return executeInOsa(code);
}

// https://github.com/sindresorhus/execa
const DEFAULT_MAX_BUFFER = 1000 * 1000 * 100;
/**
 * execute the `code` in `osascript`
 */
function executeInOsa(code: string) {
    return new Promise((resolve, reject) => {
        const child = execFile(
            '/usr/bin/osascript',
            ['-l', 'JavaScript'],
            {
                maxBuffer: DEFAULT_MAX_BUFFER,
            },
            (err, stdout, stderr) => {
                if (err) {
                    return reject(err);
                }

                if (stderr) {
                    console.error(stderr);
                }

                if (!stdout) {
                    resolve(undefined);
                }

                try {
                    const result = JSON.parse(stdout.toString().trim()).result;
                    resolve(result);
                } catch (errorOutput) {
                    resolve(stdout.toString().trim());
                }
            },
        );
        child.stdin?.write(code);
        child.stdin?.end();
    });
}

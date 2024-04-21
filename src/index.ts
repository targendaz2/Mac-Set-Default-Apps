import { arg } from '@/src/args';

function main() {
    const args = arg({
        '--browser': Boolean,
        '--calendar': Boolean,
        '--mail': Boolean,
        '--pdf': Boolean,
        '--feu': Boolean,
        '--fut': Boolean,
        '-l': String
    });
    console.log(args['_'][-1]);
    console.log(args['--browser']);
}

main();

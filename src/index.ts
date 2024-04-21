import { arg } from '@/src/args';

function main() {
    const args = arg({
        '--help': Boolean,
        '--browser': Boolean,
    });
    console.log(args['_']);
    console.log(args['--browser']);
}

main();

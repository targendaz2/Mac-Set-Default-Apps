import { parseArgs } from '@/src/argparse';

// import type Config from '@/src/config.json';
// import type { App as AppClass, UTI as UTIClass } from '@/src/models';

// const config: typeof Config = require('@/src/config.json');
// const App: typeof AppClass = require('@/src/models').App;
// const UTI: typeof UTIClass = require('@/src/models').UTI;

// const app = new App('com.apple.Safari');
// console.log(app.name + ' as default browser');

// for (const [utiID, role] of Object.entries(
//     config.defaultAppRequirements.browser.utis,
// )) {
//     const uti = new UTI(utiID);
//     // @ts-expect-error 'role will return one of the expected values'
//     console.log(`Supports ${utiID}: ` + app.supportsUTI(uti, role));
// }

// for (const urlScheme of config.defaultAppRequirements.browser.urlSchemes) {
//     console.log(`Supports ${urlScheme}: ` + app.supportsURLScheme(urlScheme));
// }

function main() {
    console.log(parseArgs(['com.apple.Safari', '--browser']));
}

main();

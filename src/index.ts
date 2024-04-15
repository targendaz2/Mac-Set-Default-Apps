import config from '@/src/config.json';
import { App, UTI } from '@/src/models';

const app = new App('com.apple.Safari');
console.log(app.name);

const uti = new UTI('public.html');
console.log(uti.tags);

console.log(app.supportsUTI(uti, 'Viewer'));

console.log(config);

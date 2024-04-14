import { App, UTI } from './models';

const app = new App('com.apple.Safari');
console.log(app.name);

const uti = new UTI('public.html');
console.log(uti.tags);

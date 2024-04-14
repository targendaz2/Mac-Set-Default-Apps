import { UTIManager } from './managers';
import { App } from './models';

const app = new App('com.apple.Safari');
console.log(app.name);

const uti = new UTIManager('public.html').create();
console.log(uti.tags);

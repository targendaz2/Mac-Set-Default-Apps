import { AppManager, UTIManager } from './managers';

const app = new AppManager('com.apple.Safari').create();
console.log(app.name);

const uti = new UTIManager('public.html').create();
console.log(uti.tags);

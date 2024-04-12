import { AppManager, UtiManager } from './managers';

const app = new AppManager('com.apple.Safari').create();
console.log(app.name);

const uti = new UtiManager('public.html').create();
console.log(uti.tags);

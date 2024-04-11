import { AppManager } from './managers/AppManager';

const app = new AppManager('com.apple.Safari').create();

console.log(app.name);

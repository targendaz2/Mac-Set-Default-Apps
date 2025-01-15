// @ts-check
import typescript from '@rollup/plugin-typescript';
import { chmodSync, statSync } from 'node:fs';

/** @type {import('rollup').RollupOptions} */
const config = {
  input: './src/index.ts',
  output: {
    file: './build/msda.js',
    format: 'commonjs',
    strict: false,
    banner: '#!/usr/bin/env osascript -l JavaScript\n',
  },
  plugins: [
    typescript({ module: 'ESNext' }),
    {
      name: 'rollup-make-executable',
      writeBundle: (options) => {
        const file = options.file;
        if (!file) return;
        const { mode } = statSync(file);
        const newMode = mode | 0o111;
        chmodSync(file, newMode);
      },
    },
  ],
};

export default config;

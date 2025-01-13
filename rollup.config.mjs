// @ts-check

/** @type {import('rollup').RollupOptions} */
const config = {
  input: './src/index.ts',
  output: {
    file: './build/bundle.js',
    format: 'commonjs',
  },
};

export default config;

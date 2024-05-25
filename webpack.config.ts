import path from 'node:path';
import { BannerPlugin, Configuration } from 'webpack';
import WebpackShellPluginNext from 'webpack-shell-plugin-next';

const config: Configuration = {
  devtool: 'source-map',
  entry: './src/index.ts',
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.ts$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  optimization: {
    concatenateModules: true,
    minimize: true,
  },
  output: {
    filename: 'msda.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new BannerPlugin({
      banner: '#!/usr/bin/osascript -l JavaScript',
      raw: true,
    }),
    new WebpackShellPluginNext({
      onAfterDone: {
        scripts: ['chmod +x ./dist/msda.js'],
        blocking: true,
        parallel: false,
      },
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    extensions: ['.ts', '.js'],
  },
};

export default config;

import path from 'node:path';
import webpack, { BannerPlugin } from 'webpack';
import WebpackShellPluginNext from 'webpack-shell-plugin-next'

export default {
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
    minimize: true,
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
  },
  plugins: [
    new BannerPlugin({
      banner: '#!/usr/bin/osascript -l JavaScript',
      raw: true,
    }),
    new WebpackShellPluginNext({
      onAfterDone: {
        scripts: ['chmod +x ./dist/bundle.js'],
        blocking: true,
        parallel: false,
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname),
    },
    extensions: ['.ts', '.js'],
  },
} satisfies webpack.Configuration;

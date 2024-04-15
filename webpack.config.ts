import path from 'node:path';
import webpack from 'webpack';

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
  plugins: [],
  resolve: {
    alias: {
      '@': path.resolve(__dirname),
    },
    extensions: ['.ts', '.js'],
  },
} satisfies webpack.Configuration;

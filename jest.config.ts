import { JestConfigWithTsJest, pathsToModuleNameMapper } from 'ts-jest';
import { compilerOptions } from './tsconfig.json';

const config: JestConfigWithTsJest = {
  moduleFileExtensions: ['js', 'ts'],
  moduleNameMapper: pathsToModuleNameMapper(compilerOptions.paths, {
    prefix: '<rootDir>',
    useESM: true,
  }),
  preset: 'ts-jest',
  setupFilesAfterEnv: ['./tests/extensions/fs.ext.ts'],
  testEnvironment: 'node',
  testRegex: '.+\\.test\\.ts$',
  testTimeout: 30000,
};

export default config;

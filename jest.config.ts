import type { JestConfigWithTsJest } from 'ts-jest';

const config: JestConfigWithTsJest = {
  moduleFileExtensions: ['js', 'ts'],
  preset: 'ts-jest',
  setupFilesAfterEnv: ['./tests/extensions/fs.ext.ts'],
  testEnvironment: 'node',
  testRegex: 'tests/.*\\.test\\.ts$',
};

export default config;

import type { JestConfigWithTsJest } from "ts-jest";

const config: JestConfigWithTsJest = {
  moduleFileExtensions: ["js", "ts"],
  preset: "ts-jest",
  setupFilesAfterEnv: [],
  testEnvironment: "node",
  testRegex: "tests/.*\\.test\\.ts$",
};

export default config;

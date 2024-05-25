// @ts-check
import eslint from '@eslint/js';
import eslintConfigPrettier from 'eslint-config-prettier';
import tseslint from 'typescript-eslint';

const config = tseslint.config(
  {
    ignores: ['dist/*'],
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  eslintConfigPrettier,
  {
    files: ['./src/*.ts'],
    ignores: ['./src/tests/**/*.ts'],
    rules: {
      'no-restricted-imports': [
        'error',
        {
          patterns: ['node:*'],
        },
      ],
      'no-restricted-syntax': [
        'error',
        {
          selector: 'AwaitExpression',
          message: 'JXA does not support async JavaScript.',
        },
        {
          selector: 'ExportDefaultDeclaration',
          message: 'Webpack breaks default exports in JXA code.',
        },
        {
          selector: 'SpreadElement',
          message: 'JXA does not support the spread operator.',
        },
      ],
    },
  },
  {
    rules: {
      '@typescript-eslint/no-unused-vars': [
        'error',
        {
          args: 'all',
          argsIgnorePattern: '^_',
          caughtErrors: 'all',
          caughtErrorsIgnorePattern: '^_',
          destructuredArrayIgnorePattern: '^_',
          varsIgnorePattern: '^_',
          ignoreRestSiblings: true,
        },
      ],
      '@typescript-eslint/no-var-requires': 'off',
      eqeqeq: 'error',
      'no-var': 'error',
    },
  },
);

export default config;

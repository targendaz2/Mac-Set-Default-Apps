// @ts-check
import eslint from '@eslint/js';
import eslintConfigPrettier from 'eslint-config-prettier';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {
    ignores: ['dist/*'],
  },
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  eslintConfigPrettier,
  {
    files: ['src/**/*.ts'],
    rules: {
      '@typescript-eslint/no-var-requires': 'off',
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
      eqeqeq: 'error',
      'no-unused-vars': [
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
      'no-var': 'error',
    },
  },
);

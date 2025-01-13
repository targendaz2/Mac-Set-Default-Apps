// Heavily based on Vercel's "arg" package
// https://github.com/vercel/arg
import { getArgs } from './getter';

type Handler<T = any> = (value: T, name: string, previousValue?: T) => T;

interface Args {
  [key: string]: string | Handler<any> | [Handler<any>];
}

interface ParseArgsOptions {
  argv?: string[];
  permissive?: boolean;
  stopAtPositional?: boolean;
}

interface ParsedArgs {
  _: string[];
  [key: string]: any;
}

class ArgumentError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'ArgumentError';
  }
}

export function parseArgs(
  args: Args,
  {
    argv = getArgs(),
    permissive = false,
    stopAtPositional = false,
  }: ParseArgsOptions = {},
) {
  const result: ParsedArgs = { _: [] };
  const aliases: { [key: string]: string } = {};
  const handlers: { [key: string]: [Handler, boolean] } = {};

  // Sort arguments into aliases and handlers
  for (const key of Object.keys(args)) {
    // Argument validity checks
    if (!key) {
      throw new ArgumentError('argument key cannot be an empty string');
    }

    if (key[0] !== '-') {
      throw new ArgumentError(
        `argument key must start with '-' but found: '${key}'`,
      );
    }

    if (key.length === 1) {
      throw new ArgumentError(
        `argument key must have a name; singular '-' keys are not allowed: ${key}`,
      );
    }

    // If the argument is a string, it's an alias for another argument
    if (typeof args[key] === 'string') {
      aliases[key] = args[key] as string;
      continue;
    }

    // Otherwise, it's a type
    let type = args[key];
    let isFlag = false;

    if (
      Array.isArray(type) &&
      type.length === 1 &&
      typeof type[0] === 'function'
    ) {
      const [fn] = type;
      type = (value, name, prev: any[] = []) => {
        prev.push(fn(value, name, prev[prev.length - 1]));
        return prev;
      };
      isFlag = fn === Boolean;
    } else if (typeof type === 'function') {
      isFlag = type === Boolean;
    } else {
      throw new ArgumentError(
        `type missing or not a function or valid array type: ${key}`,
      );
    }

    if (key[1] !== '-' && key.length > 2) {
      throw new ArgumentError(
        `short argument keys (with a single hyphen) must have only one character: ${key}`,
      );
    }

    handlers[key] = [type, isFlag];
  }

  for (let i = 0, len = argv.length; i < len; i++) {
    const wholeArg = argv[i];

    if (stopAtPositional && result._.length > 0) {
      result._ = result._.concat(argv.slice(i));
      break;
    }

    if (wholeArg === '--') {
      result._ = result._.concat(argv.slice(i + 1));
      break;
    }

    if (wholeArg.length > 1 && wholeArg[0] === '-') {
      const separatedArguments =
        wholeArg[1] === '-' || wholeArg.length === 2 ?
          [wholeArg]
        : wholeArg
            .slice(1)
            .split('')
            .map((a) => `-${a}`);

      for (let j = 0; j < separatedArguments.length; j++) {
        const arg = separatedArguments[j];
        const [originalArgName, argStr] =
          arg[1] === '-' ? arg.split(/=(.*)/, 2) : [arg, undefined];

        let argName = originalArgName;
        while (argName in aliases) {
          argName = aliases[argName];
        }

        if (!(argName in handlers)) {
          if (permissive) {
            result._.push(arg);
            continue;
          } else {
            throw new ArgumentError(
              `unknown or unexpected option: ${originalArgName}`,
            );
          }
        }

        const [type, isFlag] = handlers[argName];

        if (!isFlag && j + 1 < separatedArguments.length) {
          throw new ArgumentError(
            `option requires argument (but was followed by another short argument): ${originalArgName}`,
          );
        }

        if (isFlag) {
          result[argName] = type(true, argName, result[argName]);
        } else if (argStr === undefined) {
          if (
            argv.length < i + 2 ||
            (argv[i + 1].length > 1 &&
              argv[i + 1][0] === '-' &&
              !(
                argv[i + 1].match(/^-?\d*(\.(?=\d))?\d*$/) &&
                (type === Number ||
                  (typeof BigInt !== 'undefined' && type === BigInt))
              ))
          ) {
            const extended =
              originalArgName === argName ? '' : ` (alias for ${argName})`;
            throw new ArgumentError(
              `option requires argument: ${originalArgName}${extended}`,
            );
          }

          result[argName] = type(argv[i + 1], argName, result[argName]);
          ++i;
        } else {
          result[argName] = type(argStr, argName, result[argName]);
        }
      }
    } else {
      result._.push(wholeArg);
    }
  }
  return result;
}

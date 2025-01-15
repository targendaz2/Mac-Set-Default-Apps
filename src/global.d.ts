declare global {
  type Nil = any;

  interface Application {
    closeAccess: (path: string) => void;
    doShellScript: (script: string) => string;
    exists: (path: string) => boolean;
    id: () => string;
    includeStandardAdditions: boolean;
    name: () => string;
    openForAccess: (path: string) => any;
    read: (handle: any) => any;
  }

  interface NSArray<T = any> {
    count: number;
    objectAtIndex: (index: number) => T;
  }

  interface Error {
    localizedDescription: string;
  }

  function $(): Nil;

  $.NSDictionary = {
    dictionaryWithContentsOfFile: (path: string) => any,
  };

  $.NSFileManager = {
    alloc: {
      init: {
        createDirectoryAtPathWithIntermediateDirectoriesAttributesError:
          function (
            path: string,
            createIntermediates: boolean,
            attributes: any | Nil,
            error: Error | Nil,
          ): undefined {},

        fileExistsAtPathIsDirectory: function (
          path: string,
          isDirectory: boolean,
        ): boolean {},
      },
    },
  };

  $.NSLog = function (message: string): void {};

  $.NSProcessInfo = {
    processInfo: {
      arguments: NSArray,
    },
  };

  function Application(path: string): Application;
  Application.currentApplication = function (): Application {};

  const ObjC: {
    deepUnwrap: (dict: object) => any;
    import: (lib: string) => void;
    unwrap: (dict: object) => any;
  };

  const Path: (path: string) => string;
}

export {};

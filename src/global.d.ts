interface Application {
  closeAccess: (path: string) => void;
  doShellScript: (script: string) => string;
  exists: (path: string) => boolean;
  includeStandardAdditions: boolean;
  openForAccess: (path: string) => any;
  read: (handle: any) => any;
}

interface NSArray<T = any> {
  count: number;
  objectAtIndex: (index: number) => T;
}

declare global {
  const $: {
    NSDictionary: {
      dictionaryWithContentsOfFile: (path: string) => any;
    };

    NSProcessInfo: {
      processInfo: {
        arguments: NSArray;
      };
    };
  };

  const Application: {
    currentApplication: () => Application;
  };

  const ObjC: {
    deepUnwrap: (dict: object) => any;
    unwrap: (dict: object) => any;
  };

  const Path: (path: string) => string;
}

export {};

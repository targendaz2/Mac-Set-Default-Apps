import '@jxa/global-type';

export class UtiManager {
    // readonly tags: string[];

    constructor(readonly id: string) {
        // const app = Application.currentApplication();
        // app.includeStandardAdditions = true;
        // const result = app.doShellScript(
        //     '/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister' +
        //         `-gc -dump Type \
        //         | awk -F ':' "{ \
        //             if (\\$1 == \\"type id\\" && \\$2 ~ \\"$${this.id}\\") { \
        //                 check=\\"yes\\" \
        //             } else if (\\$1 == \\"type id\\") { \
        //                 check=\\"no\\" \
        //             } else if (\\$1 == \\"tags\\" && check == \\"yes\\") { \
        //                 print \\$2 \
        //             } \
        //         }`,
        // );
        // console.log(result);
    }
}

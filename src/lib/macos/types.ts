export type LSHandlerDocumentTypeSchema = {
    LSHandlerContentType: string;
} & (
    | {
          LSHandlerPreferredVersions: {
              LSHandlerRoleViewer: string;
          };
          LSHandlerRoleViewer: string;
      }
    | {
          LSHandlerPreferredVersions: {
              LSHandlerRoleShell: string;
          };
          LSHandlerRoleShell: string;
      }
    | {
          LSHandlerPreferredVersions: {
              LSHandlerRoleQLGenerator: string;
          };
          LSHandlerRoleQLGenerator: string;
      }
    | {
          LSHandlerPreferredVersions: {
              LSHandlerRoleNone: string;
          };
          LSHandlerRoleNone: string;
      }
    | {
          LSHandlerPreferredVersions: {
              LSHandlerRoleAll: string;
          };
          LSHandlerRoleAll: string;
      }
);

export type LSHandlerURLSchemeSchema = {
    LSHandlerURLScheme: string;
    LSHandlerPreferredVersions: {
        LSHandlerRoleAll: string;
    };
    LSHandlerRoleAll: string;
};

export type LSHandlerSchema =
    | LSHandlerDocumentTypeSchema
    | LSHandlerURLSchemeSchema;

export type LaunchServicesSchema = {
    LSHandlers: LSHandlerSchema[];
};

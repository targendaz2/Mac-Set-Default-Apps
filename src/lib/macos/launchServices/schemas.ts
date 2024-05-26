export type DocumentTypeSchema = {
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

export type URLSchemeSchema = {
    LSHandlerURLScheme: string;
    LSHandlerPreferredVersions: {
        LSHandlerRoleAll: '-';
    };
    LSHandlerRoleAll: string;
};

export type LSHandlerSchema = DocumentTypeSchema | URLSchemeSchema;

export type LaunchServicesSchema = {
    LSHandlers: LSHandlerSchema[];
};

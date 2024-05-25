import z from 'zod';

const LSHandlerDocumentTypeSchema = z.intersection(
    z.object({ LSHandlerContentType: z.string() }),
    z.union([
        z.object({
            LSHandlerPreferredVersions: z.object({
                LSHandlerRoleViewer: z.string(),
            }),
            LSHandlerRoleViewer: z.string(),
        }),
        z.object({
            LSHandlerPreferredVersions: z.object({
                LSHandlerRoleShell: z.string(),
            }),
            LSHandlerRoleShell: z.string(),
        }),
        z.object({
            LSHandlerPreferredVersions: z.object({
                LSHandlerRoleQLGenerator: z.string(),
            }),
            LSHandlerRoleQLGenerator: z.string(),
        }),
        z.object({
            LSHandlerPreferredVersions: z.object({
                LSHandlerRoleNone: z.string(),
            }),
            LSHandlerRoleNone: z.string(),
        }),
        z.object({
            LSHandlerPreferredVersions: z.object({
                LSHandlerRoleAll: z.string(),
            }),
            LSHandlerRoleAll: z.string(),
        }),
    ]),
);

const LSHandlerURLSchemeSchema = z.object({
    LSHandlerURLScheme: z.string(),
    LSHandlerPreferredVersions: z.object({
        LSHandlerRoleAll: z.string(),
    }),
    LSHandlerRoleAll: z.string(),
});

export const LaunchServicesSchema = z.object({
    LSHandlers: z
        .union([LSHandlerDocumentTypeSchema, LSHandlerURLSchemeSchema])
        .array(),
});

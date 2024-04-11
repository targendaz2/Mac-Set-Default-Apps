import z from 'zod';

const CFBundleDocumentType = z.object({
    CFBundleTypeExtensions: z.string().array().optional(),
    CFBundleTypeMIMETypes: z.string().array().optional(),
    CFBundleTypeRole: z.string(),
});

const CFBundleURLType = z.object({
    CFBundleURLSchemes: z.string().array(),
});

const InfoPlist = z.object({
    CFBundleDisplayName: z.string(),
    CFBundleDocumentTypes: CFBundleDocumentType.array().optional(),
    CFBundleIdentifier: z.string(),
    CFBundleName: z.string(),
    CFBundleShortVersionString: z.string(),
    CFBundleURLTypes: CFBundleURLType.array().optional(),
});

type InfoPlist = z.infer<typeof InfoPlist>;

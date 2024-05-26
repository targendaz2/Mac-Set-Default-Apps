import { LaunchServicesSchema } from '@/lib/macos/launchServices/schemas';
import { Factory } from 'fishery';
import { lsHandlerSchemaFactory } from './lsHandler';

class LaunchServicesSchemaFactory extends Factory<LaunchServicesSchema> {}

export const launchServicesSchemaFactory = LaunchServicesSchemaFactory.define(
    () => {
        const launchServices = lsHandlerSchemaFactory.buildList(25);
        return {
            LSHandlers: launchServices,
        };
    },
);

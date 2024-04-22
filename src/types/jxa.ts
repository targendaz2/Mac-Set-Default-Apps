import '@jxa/global-type';

export type JXAApplication = typeof Application &
    Application._StandardAdditions &
    Application.AnyValue;

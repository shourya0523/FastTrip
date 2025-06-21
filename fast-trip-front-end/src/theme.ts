/* eslint-disable @typescript-eslint/no-empty-object-type */
"use client";

import { Inter } from "next/font/google";
import { Palette, createTheme } from "@mui/material/styles";
interface ICustomPalette {
  light: Palette["primary"];
  lightest: Palette["primary"];
  black: Palette["primary"];
  darkGrey: Palette["primary"];
  lightGrey: Palette["primary"];
  defaultGrey: Palette["primary"];
  purple: Palette["primary"];
}

interface ICustomPaletteOverride {
  light: true;
  lightest: true;
  black: true;
  darkGrey: true;
  lightGrey: true;
  defaultGrey: true;
  purple: true;
}

interface ICustomTypography {
  title: React.CSSProperties;
  hero: React.CSSProperties;
  titleSmall: React.CSSProperties;
}
interface ITypographyVariantOverrides {
  title: true;
  hero: true;
  titleSmall: true;
}

declare module "@mui/material/styles" {
  // Palette
  interface Palette extends ICustomPalette {}
  interface PaletteOptions extends Partial<ICustomPalette> {}

  // Typography
  interface TypographyVariants extends ICustomTypography {}
  interface TypographyVariantsOptions extends Partial<ICustomTypography> {}
}

declare module "@mui/material/Button" {
  interface ButtonPropsColorOverrides extends ICustomPaletteOverride {}
}

declare module "@mui/material/Typography" {
  interface TypographyPropsColorOverrides extends ICustomPaletteOverride {}
  interface TypographyPropsVariantOverrides
    extends ITypographyVariantOverrides {}
}

const inter = Inter({
  weight: ["300", "400", "500", "700"],
  subsets: ["latin"],
  display: "swap",
});

let theme = createTheme({});

theme = createTheme({
  typography: {
    fontFamily: inter.style.fontFamily,
    hero: {
      fontSize: "44px",
      fontWeight: "normal",
      lineHeight: "80px",
      fontFamily: inter.style.fontFamily,
      color: "#1E3C31",
    },
    title: {
      fontSize: "32px",
      fontWeight: "normal",
      lineHeight: "40px",
      fontFamily: inter.style.fontFamily,
      color: "#1E3C31",
    },
    titleSmall: {
      fontSize: "20px",
      fontWeight: "normal",
      lineHeight: "40px",
      fontFamily: inter.style.fontFamily,
      color: "#1E3C31",
    },
    body1: {
      fontSize: "14px",
      fontWeight: "normal",
      lineHeight: "22px",
      color: "#1E3C31",
    },
    body2: {
      fontSize: "14px",
      fontWeight: "bold",
      lineHeight: "22px",
      color: "#1E3C31",
    },
    overline: {
      fontSize: "11px",
      fontWeight: "normal",
      lineHeight: "22px",
      color: "#1E3C31",
      textTransform: "none",
    },
  },
  components: {
    MuiTypography: {
      defaultProps: {
        variantMapping: {
          hero: "h1",
          title: "h2",
          titleSmall: "h3",
        },
      },
    },
  },

  palette: {
    primary: {
      main: "#0AA86F",
    },
    secondary: {
      main: "#19D28F",
    },
    text: {
      primary: "#1E3C31",
    },
    light: theme.palette.augmentColor({
      color: {
        main: "#C5DFD6",
      },
      name: "light",
    }),
    lightest: theme.palette.augmentColor({
      color: {
        main: "#EBF6F2",
      },
      name: "lightest",
    }),
    black: theme.palette.augmentColor({
      color: {
        main: "#1E3C31",
      },
      name: "black",
    }),
    defaultGrey: theme.palette.augmentColor({
      color: {
        main: "#AAAAAA",
      },
      name: "defaultGrey",
    }),
    lightGrey: theme.palette.augmentColor({
      color: {
        main: "#DDDDDD",
      },
      name: "lightGrey",
    }),
    darkGrey: theme.palette.augmentColor({
      color: {
        main: "#666666",
      },
      name: "darkGrey",
    }),
    purple: theme.palette.augmentColor({
      color: {
        main: "#7723FF",
      },
      name: "purple",
    }),
  },
});

export default theme;

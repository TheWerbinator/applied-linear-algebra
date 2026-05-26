// `plotly.js-dist-min` ships only a minified bundle (no .d.ts). Its public
// API matches `plotly.js`, which has full @types/plotly.js declarations,
// so re-export those for type imports.
declare module "plotly.js-dist-min" {
  export * from "plotly.js";
}

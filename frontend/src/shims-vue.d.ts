/* eslint-disable */
declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

declare module "@kangc/*" {
  import type { DefineComponent } from "@kangc";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

declare module "codemirror" {
  import type { DefineComponent } from "codemirror";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}

// declare module "@fortawesome/*" {
//   import type { DefineComponent } from "@fortawesome/*";
//   const component: DefineComponent<{}, {}, any>;
//   export default component;
// }
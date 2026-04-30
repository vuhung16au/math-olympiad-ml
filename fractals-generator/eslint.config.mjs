import js from "@eslint/js";
import tseslint from "typescript-eslint";

const nodeScriptGlobals = {
  __dirname: "readonly",
  __filename: "readonly",
  Buffer: "readonly",
  clearImmediate: "readonly",
  console: "readonly",
  exports: "writable",
  module: "readonly",
  process: "readonly",
  require: "readonly",
  setImmediate: "readonly",
};

export default tseslint.config(
  {
    ignores: ["lib/**", "esm/**", "node_modules/**"],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["scripts/**/*.js"],
    languageOptions: {
      ecmaVersion: 2022,
      globals: nodeScriptGlobals,
      sourceType: "commonjs",
    },
    rules: {
      "@typescript-eslint/no-require-imports": "off",
      "no-await-in-loop": "off",
    },
  },
  {
    files: ["src/**/*.ts"],
    languageOptions: {
      ecmaVersion: 2018,
      sourceType: "module",
    },
    rules: {
      "no-plusplus": "off",
      "no-restricted-syntax": "off",
      "no-continue": "off",
      "object-curly-newline": "off",
    },
  },
);

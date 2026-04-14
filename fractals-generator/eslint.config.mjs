import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(
  {
    ignores: ["lib/**", "esm/**", "node_modules/**"],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
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

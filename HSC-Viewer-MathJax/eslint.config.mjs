import nextVitals from "eslint-config-next/core-web-vitals";

const config = [
  ...nextVitals,
  {
    ignores: [".generated/**", ".next/**", "coverage/**"],
  },
];

export default config;

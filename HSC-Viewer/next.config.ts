import type { NextConfig } from "next";

const isCloudflareBuild = process.env.CLOUDFLARE_BUILD === "1";

const nextConfig: NextConfig = {
  serverExternalPackages: isCloudflareBuild
    ? []
    : ["@napi-rs/canvas", "pdfjs-dist", "sharp"],
  async rewrites() {
    return [
      {
        source: "/og/preview-:version/booklets/:slug/:page.png",
        destination: "/og/booklets/:slug/:page.png",
      },
    ];
  },
  ...(isCloudflareBuild ? {
    webpack(config, { isServer }) {
      if (isServer) {
        config.resolve.alias = {
          ...config.resolve.alias,
          "sharp": false,
          "@napi-rs/canvas": false,
          "pdfjs-dist/legacy/build/pdf.mjs": false,
          "pdfjs-dist/legacy/build/pdf.worker.mjs": false,
        };
      }
      return config;
    }
  } : {})
};

export default nextConfig;

if (process.env.NODE_ENV === "development") {
  import("@opennextjs/cloudflare").then((m) => m.initOpenNextCloudflareForDev());
}


import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["@napi-rs/canvas", "pdfjs-dist"],
  async rewrites() {
    return [
      {
        source: "/og/preview-:version/booklets/:slug/:page.png",
        destination: "/og/booklets/:slug/:page.png",
      },
    ];
  },
};

export default nextConfig;

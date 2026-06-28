// default open-next.config.ts file created by @opennextjs/cloudflare
import { defineCloudflareConfig } from "@opennextjs/cloudflare";
// import r2IncrementalCache from "@opennextjs/cloudflare/overrides/incremental-cache/r2-incremental-cache";

const config = defineCloudflareConfig({
	// For best results consider enabling R2 caching
	// See https://opennext.js.org/cloudflare/caching for more details
	// incrementalCache: r2IncrementalCache
});

(config as any).edgeExternals = [
	...(config.edgeExternals || []),
	"sharp",
	"sharp-*",
	"@napi-rs/canvas",
	"@napi-rs/canvas-*"
];

(config as any).buildCommand = "bun run next build --webpack";

export default config;

import path from "node:path";

export const projectRoot = process.cwd();
export const repoRoot = path.resolve(projectRoot, "..");
export const generatedRoot = path.join(projectRoot, ".generated");
export const generatedBookletsRoot = path.join(generatedRoot, "booklets");
export const generatedAssetsRoot = path.join(generatedRoot, "assets");
export const generatedLogsRoot = path.join(generatedRoot, "logs");

import path from "node:path";
import chokidar from "chokidar";
import { BOOKLETS } from "@/lib/booklets";
import { generateBooklets } from "@/scripts/lib/conversion";
import { logStep } from "@/scripts/lib/logger";
import { repoRoot } from "@/scripts/lib/paths";

function detectAffectedBooklets(changedPath: string) {
  const relative = path.relative(repoRoot, changedPath);

  if (relative.startsWith("HSC-Common/")) {
    return BOOKLETS;
  }

  const topLevelDir = relative.split(path.sep)[0];
  return BOOKLETS.filter((booklet) => booklet.sourceDir === topLevelDir);
}

export async function watchBooklets() {
  const watcher = chokidar.watch(
    [
      path.join(repoRoot, "HSC-*", "**", "*.tex"),
      path.join(repoRoot, "HSC-Common", "styles", "**", "*"),
      path.join(repoRoot, "HSC-Common", "assets", "**", "*"),
    ],
    { ignoreInitial: true },
  );

  watcher.on("all", async (_event, changedPath) => {
    const affected = detectAffectedBooklets(changedPath);
    if (affected.length === 0) {
      return;
    }

    logStep(`Detected change in ${path.relative(repoRoot, changedPath)}.`);
    await generateBooklets(affected);
  });

  logStep("Watching HSC booklet sources for changes...");
}

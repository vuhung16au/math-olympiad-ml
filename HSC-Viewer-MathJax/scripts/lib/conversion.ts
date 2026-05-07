import { promises as fs } from "node:fs";
import path from "node:path";
import { spawn } from "node:child_process";
import type { BookletManifestEntry, BookletSourceConfig, ConversionResult } from "@/lib/booklets";
import { BOOKLETS } from "@/lib/booklets";
import { buildFallbackHtml } from "@/scripts/lib/html-fallback";
import { ensureDir, removeDir, writeTextFile } from "@/scripts/lib/fs-utils";
import { logStep, logWarn } from "@/scripts/lib/logger";
import {
  generatedAssetsRoot,
  generatedBookletsRoot,
  generatedLogsRoot,
  generatedRoot,
  repoRoot,
} from "@/scripts/lib/paths";
import { postprocessHtml } from "@/scripts/lib/postprocess";

const FALLBACK_MARKER = "Generated fallback";
const generatedTmpRoot = path.join(generatedRoot, "tmp");
const generatedBuildRoot = path.join(generatedRoot, "build");

async function runMake4ht(
  booklet: BookletSourceConfig,
  buildDir: string,
  outputDir: string,
): Promise<{
  success: boolean;
  stdout: string;
  stderr: string;
  timedOut: boolean;
  exitCode: number | null;
}> {
  const bookletDir = path.join(repoRoot, booklet.sourceDir);
  const timeoutMs = Number.parseInt(process.env.MAKE4HT_TIMEOUT_MS ?? "3000", 10);
  const pathEntries = new Set([
    "/opt/homebrew/bin",
    "/usr/local/bin",
    ...(process.env.PATH ?? "").split(":").filter((entry) => entry.length > 0),
  ]);
  const env = {
    ...process.env,
    GS: process.env.GS ?? "/opt/homebrew/bin/gs",
    LIBGS: process.env.LIBGS ?? "/opt/homebrew/lib/libgs.dylib",
    PATH: Array.from(pathEntries).join(":"),
  };

  return new Promise((resolve) => {
    const child = spawn(
      "make4ht",
      [
        "-f",
        "html5",
        "-B",
        buildDir,
        "-d",
        outputDir,
        booklet.entryTex,
        "mathjax",
      ],
      { cwd: bookletDir, env, stdio: ["ignore", "pipe", "pipe"] },
    );

    let stdout = "";
    let stderr = "";
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGTERM");
    }, timeoutMs);

    child.stdout.on("data", (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on("data", (chunk) => {
      stderr += chunk.toString();
    });

    child.on("close", (code) => {
      clearTimeout(timer);
      if (timedOut) {
        stderr += `\nmake4ht timed out after ${timeoutMs}ms.`;
      }

      resolve({
        success: code === 0 && !timedOut,
        stdout,
        stderr,
        timedOut,
        exitCode: code,
      });
    });
  });
}

async function cleanupSourceIntermediates(booklet: BookletSourceConfig) {
  const bookletDir = path.join(repoRoot, booklet.sourceDir);
  const baseName = path.basename(booklet.entryTex, ".tex");
  const removableNames = new Set([
    `${baseName}.4ct`,
    `${baseName}.4tc`,
    `${baseName}.aux`,
    `${baseName}.css`,
    `${baseName}.dvi`,
    `${baseName}.html`,
    `${baseName}.idv`,
    `${baseName}.lg`,
    `${baseName}.log`,
    `${baseName}.tmp`,
    `${baseName}.xref`,
  ]);

  const names = await fs.readdir(bookletDir).catch(() => []);
  await Promise.all(
    names.map(async (name) => {
      const isGeneratedSvg = new RegExp(`^${baseName}\\d+x\\.svg$`).test(name);
      if (!removableNames.has(name) && !isGeneratedSvg) {
        return;
      }

      await fs.rm(path.join(bookletDir, name), {
        force: true,
        recursive: true,
      });
    }),
  );
}

function getWarnings(stdout: string, stderr: string) {
  return [...stdout.split("\n"), ...stderr.split("\n")]
    .map((line) => line.trim())
    .filter((line) => line.length > 0)
    .filter((line) => /warning|error/i.test(line))
    .slice(0, 20);
}

async function writeConversionLog(
  booklet: BookletSourceConfig,
  stdout: string,
  stderr: string,
) {
  const logPath = path.join(generatedLogsRoot, `${booklet.slug}.log`);
  const content = [
    `booklet=${booklet.slug}`,
    `sourceDir=${booklet.sourceDir}`,
    "",
    "[stdout]",
    stdout,
    "",
    "[stderr]",
    stderr,
    "",
  ].join("\n");

  await writeTextFile(logPath, content);
}

async function copyGeneratedAssets(
  booklet: BookletSourceConfig,
  tempOutputDir: string,
  tempBuildDir: string,
) {
  const assetTargetDir = path.join(generatedAssetsRoot, booklet.slug);
  await removeDir(assetTargetDir);
  await ensureDir(assetTargetDir);

  const copyDirContents = async (sourceDir: string, skipIntermediates: boolean) => {
    const names = await fs.readdir(sourceDir).catch(() => []);
    for (const name of names) {
      if (name.endsWith(".html")) {
        continue;
      }

      if (
        skipIntermediates &&
        /\.(4ct|4tc|aux|css|dvi|idv|lg|log|tmp|xref)$/i.test(name)
      ) {
        continue;
      }

      await fs.cp(path.join(sourceDir, name), path.join(assetTargetDir, name), {
        recursive: true,
        force: true,
      });
    }
  };

  await copyDirContents(tempOutputDir, false);
  await copyDirContents(tempBuildDir, true);
}

function isFallbackHtml(html: string) {
  return html.includes(FALLBACK_MARKER);
}

async function readPreservableExistingHtml(booklet: BookletSourceConfig) {
  const htmlPath = path.join(generatedBookletsRoot, `${booklet.slug}.html`);

  try {
    const existingHtml = await fs.readFile(htmlPath, "utf8");
    if (isFallbackHtml(existingHtml)) {
      return null;
    }

    return existingHtml;
  } catch {
    return null;
  }
}

async function createFallbackResult(
  booklet: BookletSourceConfig,
  reason: string,
): Promise<ConversionResult> {
  const existingHtml = await readPreservableExistingHtml(booklet);
  const relativeHtmlPath = `.generated/booklets/${booklet.slug}.html`;

  if (existingHtml) {
    logWarn(`Preserving existing converted HTML for ${booklet.slug}; fallback output was skipped.`);

    return {
      booklet: {
        ...booklet,
        htmlPath: relativeHtmlPath,
        assetBasePath: `/_generated/assets/${booklet.slug}`,
        conversionWarnings: [
          `${reason} Existing converted HTML was preserved.`,
        ],
        lastGeneratedAt: new Date().toISOString(),
      },
      html: existingHtml,
    };
  }

  const entryPath = path.join(repoRoot, booklet.sourceDir, booklet.entryTex);
  const preview = await fs.readFile(entryPath, "utf8").catch(() => "");
  const html = buildFallbackHtml(booklet, reason, preview.slice(0, 4000));

  await writeTextFile(path.join(generatedRoot, "booklets", `${booklet.slug}.html`), html);

  return {
    booklet: {
      ...booklet,
      htmlPath: relativeHtmlPath,
      assetBasePath: `/_generated/assets/${booklet.slug}`,
      conversionWarnings: [reason],
      lastGeneratedAt: new Date().toISOString(),
    },
    html,
  };
}

async function readGeneratedHtml(htmlPath: string) {
  try {
    const html = await fs.readFile(htmlPath, "utf8");
    return html.trim().length > 0 ? html : null;
  } catch {
    return null;
  }
}

export async function convertBooklet(booklet: BookletSourceConfig): Promise<ConversionResult> {
  const bookletDir = path.join(repoRoot, booklet.sourceDir);
  const entryPath = path.join(bookletDir, booklet.entryTex);

  try {
    await fs.access(entryPath);
  } catch {
    return createFallbackResult(
      booklet,
      `Entry file not found: ${booklet.entryTex} in ${booklet.sourceDir}.`,
    );
  }

  if (!booklet.entryTex.endsWith(".tex")) {
    return createFallbackResult(
      booklet,
      `This source folder is not a renderable booklet entry: ${booklet.entryTex}.`,
    );
  }

  const tempOutputDir = path.join(generatedRoot, "tmp", booklet.slug);
  const tempBuildDir = path.join(generatedRoot, "build", booklet.slug);
  await removeDir(tempOutputDir);
  await removeDir(tempBuildDir);
  await ensureDir(tempOutputDir);
  await ensureDir(tempBuildDir);

  logStep(`Generating ${booklet.slug}...`);
  const result = await runMake4ht(booklet, tempBuildDir, tempOutputDir);
  await cleanupSourceIntermediates(booklet);
  await writeConversionLog(booklet, result.stdout, result.stderr);
  const htmlPath = path.join(
    tempBuildDir,
    `${path.basename(booklet.entryTex, ".tex")}.html`,
  );

  if (!result.success) {
    const salvagedHtml = !result.timedOut ? await readGeneratedHtml(htmlPath) : null;

    if (salvagedHtml) {
      logWarn(`make4ht reported errors for ${booklet.slug}; salvaging generated HTML.`);
      const processedHtml = postprocessHtml(salvagedHtml, booklet.slug);
      await copyGeneratedAssets(booklet, tempOutputDir, tempBuildDir);

      const relativeHtmlPath = `.generated/booklets/${booklet.slug}.html`;
      await writeTextFile(path.join(generatedBookletsRoot, `${booklet.slug}.html`), processedHtml);

      return {
        booklet: {
          ...booklet,
          htmlPath: relativeHtmlPath,
          assetBasePath: `/_generated/assets/${booklet.slug}`,
          conversionWarnings: [
            `make4ht exited with code ${result.exitCode ?? "unknown"}, but generated HTML was salvaged.`,
            ...getWarnings(result.stdout, result.stderr),
          ].slice(0, 20),
          lastGeneratedAt: new Date().toISOString(),
        },
        html: processedHtml,
      };
    }

    logWarn(`make4ht failed for ${booklet.slug}; writing fallback HTML.`);
    return createFallbackResult(
      booklet,
      `${result.stderr || result.stdout || "make4ht returned a non-zero status."}`.slice(0, 2000),
    );
  }

  const html = await readGeneratedHtml(htmlPath);
  if (!html) {
    return createFallbackResult(
      booklet,
      `make4ht completed without producing ${path.basename(htmlPath)}.`,
    );
  }

  const processedHtml = postprocessHtml(html, booklet.slug);
  await copyGeneratedAssets(booklet, tempOutputDir, tempBuildDir);

  const relativeHtmlPath = `.generated/booklets/${booklet.slug}.html`;
  await writeTextFile(path.join(generatedBookletsRoot, `${booklet.slug}.html`), processedHtml);

  const warnings = getWarnings(result.stdout, result.stderr);

  return {
    booklet: {
      ...booklet,
      htmlPath: relativeHtmlPath,
      assetBasePath: `/_generated/assets/${booklet.slug}`,
      conversionWarnings: warnings,
      lastGeneratedAt: new Date().toISOString(),
    },
    html: processedHtml,
  };
}

export async function generateBooklets(booklets: BookletSourceConfig[]) {
  await ensureDir(generatedRoot);
  await ensureDir(generatedBookletsRoot);
  await ensureDir(generatedAssetsRoot);
  await ensureDir(generatedLogsRoot);

  const conversions: ConversionResult[] = [];
  for (const booklet of booklets.sort((a, b) => a.order - b.order)) {
    conversions.push(await convertBooklet(booklet));
  }

  const manifest = conversions.map((conversion) => conversion.booklet);
  await writeTextFile(
    path.join(generatedRoot, "manifest.json"),
    `${JSON.stringify(manifest, null, 2)}\n`,
  );

  return manifest;
}

export function resolveBooklets(selection?: string) {
  if (!selection) {
    return BOOKLETS;
  }

  const needle = selection.toLowerCase();
  return BOOKLETS.filter((booklet) => {
    return (
      booklet.slug === needle ||
      booklet.sourceDir.toLowerCase() === needle ||
      booklet.sourceDir.toLowerCase() === selection.toLowerCase()
    );
  });
}

export async function cleanGeneratedArtifacts() {
  await ensureDir(generatedRoot);
  await removeDir(generatedTmpRoot);
  await removeDir(generatedBuildRoot);
  await removeDir(generatedLogsRoot);
  await ensureDir(generatedBookletsRoot);
  await ensureDir(generatedAssetsRoot);
  await ensureDir(generatedLogsRoot);
  await writeTextFile(path.join(generatedRoot, ".gitkeep"), "");
}

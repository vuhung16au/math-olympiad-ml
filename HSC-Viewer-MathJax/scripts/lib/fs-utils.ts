import { promises as fs } from "node:fs";
import path from "node:path";

export async function ensureDir(dirPath: string) {
  await fs.mkdir(dirPath, { recursive: true });
}

export async function removeDir(dirPath: string) {
  await fs.rm(dirPath, { recursive: true, force: true });
}

export async function writeTextFile(filePath: string, content: string) {
  await ensureDir(path.dirname(filePath));
  await fs.writeFile(filePath, content, "utf8");
}

export async function copyDir(sourceDir: string, targetDir: string) {
  await ensureDir(targetDir);
  await fs.cp(sourceDir, targetDir, { recursive: true, force: true });
}

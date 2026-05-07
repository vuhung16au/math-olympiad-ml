import { cleanGeneratedArtifacts, generateBooklets, resolveBooklets } from "@/scripts/lib/conversion";

const value =
  process.argv.find((arg) => arg.startsWith("--booklet="))?.split("=")[1] ??
  process.env.BOOKLET;

const booklets = resolveBooklets(value);

if (booklets.length === 0) {
  throw new Error(`No booklet matched "${value ?? ""}".`);
}

await cleanGeneratedArtifacts();
await generateBooklets(booklets);

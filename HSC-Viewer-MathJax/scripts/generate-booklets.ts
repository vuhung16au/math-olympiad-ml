import { BOOKLETS } from "@/lib/booklets";
import { cleanGeneratedArtifacts, generateBooklets } from "@/scripts/lib/conversion";
import { logStep } from "@/scripts/lib/logger";

await cleanGeneratedArtifacts();
await generateBooklets(BOOKLETS);
logStep("Generated all booklet HTML artifacts.");

import { generateBooklets } from "@/scripts/lib/conversion";
import { BOOKLETS } from "@/lib/booklets";
import { watchBooklets } from "@/scripts/lib/watch";

await generateBooklets(BOOKLETS);
await watchBooklets();

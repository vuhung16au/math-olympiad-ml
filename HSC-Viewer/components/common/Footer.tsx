import Link from "next/link";
import { REPO_LINKS } from "@/lib/constants";

export default function Footer() {
  return (
    <footer className="border-t border-black/8 bg-white/80 px-4 py-4 text-sm text-[var(--color-charcoal)] sm:px-6 lg:px-8">
      <div className="mx-auto flex max-w-[1200px] flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <p>
          HSC Math Hub content is licensed under{" "}
          <a
            href={REPO_LINKS.license}
            target="_blank"
            rel="noreferrer"
            className="font-semibold text-[var(--color-purple)] underline decoration-[var(--color-red)] decoration-2 underline-offset-4"
          >
            CC BY 4.0
          </a>
          .
        </p>
        <div className="flex flex-wrap items-center gap-4">
          <a
            href={REPO_LINKS.substack}
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[var(--color-purple)] hover:underline"
          >
            Substack
          </a>
          <Link
            href="/faq"
            className="font-medium text-[var(--color-purple)] hover:underline"
          >
            FAQ
          </Link>
          <a
            href={REPO_LINKS.linkedin}
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[var(--color-purple)] hover:underline"
          >
            LinkedIn
          </a>
          <a
            href={REPO_LINKS.github}
            target="_blank"
            rel="noreferrer"
            className="font-medium text-[var(--color-purple)] hover:underline"
          >
            Source repository
          </a>
        </div>
      </div>
    </footer>
  );
}

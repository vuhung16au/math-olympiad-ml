"use client";

import { useEffect, useRef } from "react";
import { typesetMath } from "@/lib/mathjax";

export default function BookletContent({ html }: { html: string }) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    void typesetMath(containerRef.current);
  }, [html]);

  return (
    <div
      ref={containerRef}
      className="max-w-none px-4 py-6 sm:px-6 lg:px-10 [&_.booklet-document_h1]:text-4xl [&_.booklet-document_h1]:font-semibold [&_.booklet-document_h2]:mt-8 [&_.booklet-document_h2]:text-2xl [&_.booklet-document_h2]:font-semibold [&_.booklet-document_h3]:text-xl [&_.booklet-document_h3]:font-semibold [&_.booklet-document_pre]:rounded-2xl [&_.booklet-document_pre]:bg-[var(--color-charcoal)] [&_.booklet-document_pre]:p-4 [&_.booklet-document_pre]:text-[var(--color-ivory)] [&_.warning]:rounded-2xl [&_.warning]:border [&_.warning]:border-[var(--color-red)]/20 [&_.warning]:bg-[color:color-mix(in_srgb,var(--color-red)_8%,white)] [&_.warning]:p-4 [&_.eyebrow]:text-xs [&_.eyebrow]:font-semibold [&_.eyebrow]:uppercase [&_.eyebrow]:tracking-[0.24em] [&_.eyebrow]:text-[var(--color-red)] [&_.mathjax-block]:my-4 [&_.mathjax-block]:overflow-x-auto [&_.mathjax-inline]:whitespace-normal"
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
}

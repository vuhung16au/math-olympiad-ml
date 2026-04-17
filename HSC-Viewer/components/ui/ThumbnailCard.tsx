"use client";

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";
import { Clock3 } from "lucide-react";
import type { Booklet } from "@/lib/booklets";

export default function ThumbnailCard({ booklet }: { booklet: Booklet }) {
  const [imageFailed, setImageFailed] = useState(false);
  const hasThumbnail = !imageFailed;

  const content = (
    <article
      className={[
        "group relative overflow-hidden rounded-[28px] border p-5 shadow-[0_20px_50px_rgba(60,16,83,0.08)] transition duration-300",
        booklet.isAvailable
          ? "border-black/8 bg-white hover:-translate-y-1 hover:shadow-[0_24px_60px_rgba(60,16,83,0.16)]"
          : "border-black/6 bg-[color:color-mix(in_srgb,var(--color-stone)_18%,white)] opacity-70",
      ].join(" ")}
    >
      <div className="absolute inset-x-0 top-0 h-28 bg-[radial-gradient(circle_at_top_left,rgba(242,18,12,0.18),transparent_58%),linear-gradient(135deg,rgba(60,16,83,0.96),rgba(181,24,37,0.86))]" />
      <div className="relative flex min-h-[300px] flex-col justify-between gap-6">
        <div>
          <div
            className={[
              "mb-6 inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.22em] backdrop-blur-sm",
              booklet.isAvailable
                ? "border-white/25 bg-white/12 text-white"
                : "border-white/35 bg-white/85 text-[var(--color-charcoal)]",
            ].join(" ")}
          >
            {!booklet.isAvailable && <Clock3 size={12} aria-hidden="true" />}
            <span>{booklet.isAvailable ? "Available now" : "Coming soon"}</span>
          </div>
          <h2 className="max-w-[15ch] text-2xl font-semibold leading-tight text-white">
            {booklet.title}
          </h2>
        </div>

        <div className="overflow-hidden rounded-[24px] border border-black/6 bg-[color:color-mix(in_srgb,var(--color-ivory)_84%,white)]">
          {hasThumbnail ? (
            <Image
              src={booklet.thumbnailPath}
              alt={`${booklet.title} thumbnail`}
              width={640}
              height={832}
              onError={() => setImageFailed(true)}
              className="h-52 w-full object-cover"
            />
          ) : (
            <div className="flex h-52 items-center justify-center bg-[radial-gradient(circle_at_top,rgba(242,18,12,0.15),transparent_46%),linear-gradient(145deg,rgba(60,16,83,0.12),rgba(242,239,235,1))] p-6 text-center">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
                  Thumbnail pending
                </p>
                <p className="mt-3 text-lg font-semibold text-[var(--color-purple)]">
                  {booklet.title}
                </p>
              </div>
            </div>
          )}
          <div className="p-4">
            <p className="text-sm leading-6 text-[color:color-mix(in_srgb,var(--color-charcoal)_80%,white)]">
              {booklet.isAvailable
                ? "Open the booklet in the full-screen viewer with page controls, download, and print actions."
                : "This module does not have a published PDF yet. It will appear here once the release is added."}
            </p>
            <div className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-[var(--color-purple)]">
              {booklet.isAvailable ? "Open booklet" : "Unavailable"}
              <span aria-hidden="true">→</span>
            </div>
          </div>
        </div>
      </div>
    </article>
  );

  if (!booklet.isAvailable) {
    return <div>{content}</div>;
  }

  return (
    <Link href={`/booklets/${booklet.slug}`} className="block">
      {content}
    </Link>
  );
}

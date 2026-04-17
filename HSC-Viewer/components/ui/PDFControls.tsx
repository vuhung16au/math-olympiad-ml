"use client";

import {
  ChevronLeft,
  ChevronRight,
  Download,
  Expand,
  Moon,
  Minus,
  Palette,
  Plus,
  Printer,
  RotateCcw,
  Sun,
} from "lucide-react";

type ReadingTheme = "light" | "dark" | "sepia";

interface PDFControlsProps {
  bookletTitle: string;
  pdfUrl: string;
  currentPage: number;
  totalPages: number;
  scale: number;
  canGoPrevious: boolean;
  canGoNext: boolean;
  onPageChange: (page: number) => void;
  onPreviousPage: () => void;
  onNextPage: () => void;
  onZoomIn: () => void;
  onZoomOut: () => void;
  onResetZoom: () => void;
  onFitWidth: () => void;
  onFullscreen: () => void;
  onPrint: () => void;
  viewMode: "single" | "continuous";
  onToggleViewMode: () => void;
  readingTheme: ReadingTheme;
  onReadingThemeChange: (theme: ReadingTheme) => void;
  onPageInputEditingChange: (isEditing: boolean) => void;
}

function IconButton({
  children,
  label,
  onClick,
  disabled,
}: {
  children: React.ReactNode;
  label: string;
  onClick: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      title={label}
      className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-purple)] shadow-sm transition hover:border-[var(--color-purple)] disabled:cursor-not-allowed disabled:opacity-40"
    >
      {children}
    </button>
  );
}

export default function PDFControls({
  bookletTitle,
  pdfUrl,
  currentPage,
  totalPages,
  scale,
  canGoPrevious,
  canGoNext,
  onPageChange,
  onPreviousPage,
  onNextPage,
  onZoomIn,
  onZoomOut,
  onResetZoom,
  onFitWidth,
  onFullscreen,
  onPrint,
  viewMode,
  onToggleViewMode,
  readingTheme,
  onReadingThemeChange,
  onPageInputEditingChange,
}: PDFControlsProps) {
  return (
    <div className="flex flex-col gap-3 border-b border-black/8 px-4 py-4 sm:px-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
            Active booklet
          </p>
          <h1 className="text-xl font-semibold text-[var(--color-purple)] sm:text-2xl">
            {bookletTitle}
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={onFitWidth}
            className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm"
          >
            Fit width
          </button>
          {/* View mode toggle */}
          <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm">
            <button
              type="button"
              onClick={viewMode === "single" ? onToggleViewMode : undefined}
              aria-label="Continuous page view"
              title="Continuous page view"
              aria-pressed={viewMode === "continuous"}
              className={`px-4 py-2 text-sm font-medium transition ${
                viewMode === "continuous"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              Continuous
            </button>
            <button
              type="button"
              onClick={viewMode === "continuous" ? onToggleViewMode : undefined}
              aria-label="Single page view"
              title="Single page view"
              aria-pressed={viewMode === "single"}
              className={`px-4 py-2 text-sm font-medium transition ${
                viewMode === "single"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              Single Page
            </button>
          </div>
          <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm">
            <button
              type="button"
              onClick={() => onReadingThemeChange("light")}
              aria-label="Light reading theme"
              title="Light reading theme"
              aria-pressed={readingTheme === "light"}
              className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium transition ${
                readingTheme === "light"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              <Sun className="h-4 w-4" />
              <span className="hidden sm:inline">Light</span>
            </button>
            <button
              type="button"
              onClick={() => onReadingThemeChange("dark")}
              aria-label="Dark reading theme"
              title="Dark reading theme"
              aria-pressed={readingTheme === "dark"}
              className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium transition ${
                readingTheme === "dark"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              <Moon className="h-4 w-4" />
              <span className="hidden sm:inline">Dark</span>
            </button>
            <button
              type="button"
              onClick={() => onReadingThemeChange("sepia")}
              aria-label="Sepia reading theme"
              title="Sepia reading theme"
              aria-pressed={readingTheme === "sepia"}
              className={`inline-flex items-center gap-2 px-3 py-2 text-sm font-medium transition ${
                readingTheme === "sepia"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              <Palette className="h-4 w-4" />
              <span className="hidden sm:inline">Sepia</span>
            </button>
          </div>
          <button
            type="button"
            onClick={onPrint}
            className="inline-flex items-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm"
          >
            <Printer className="h-4 w-4" />
            Print
          </button>
          <a
            href={pdfUrl}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-2 rounded-full border border-black/10 bg-[var(--color-purple)] px-4 py-2 text-sm font-medium text-white shadow-sm"
          >
            <Download className="h-4 w-4" />
            Download PDF
          </a>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <IconButton label="Previous page" onClick={onPreviousPage} disabled={!canGoPrevious}>
            <ChevronLeft className="h-4 w-4" />
          </IconButton>
          <div className="rounded-full border border-black/10 bg-white px-3 py-2 text-sm shadow-sm">
            <label className="mr-2 text-[color:color-mix(in_srgb,var(--color-charcoal)_70%,white)]">
              Page
            </label>
            <input
              type="number"
              min={1}
              max={Math.max(totalPages, 1)}
              value={currentPage}
              onChange={(event) => onPageChange(Number(event.target.value) || 1)}
              onFocus={() => onPageInputEditingChange(true)}
              onBlur={() => onPageInputEditingChange(false)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  (event.currentTarget as HTMLInputElement).blur();
                }
              }}
              className="w-14 bg-transparent text-center font-semibold text-[var(--color-purple)] outline-none"
            />
            <span className="ml-2 text-[color:color-mix(in_srgb,var(--color-charcoal)_70%,white)]">
              / {totalPages || "-"}
            </span>
          </div>
          <IconButton label="Next page" onClick={onNextPage} disabled={!canGoNext}>
            <ChevronRight className="h-4 w-4" />
          </IconButton>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <IconButton label="Zoom out" onClick={onZoomOut}>
            <Minus className="h-4 w-4" />
          </IconButton>
          <div className="rounded-full border border-black/10 bg-white px-3 py-2 text-sm font-semibold text-[var(--color-purple)] shadow-sm">
            {Math.round(scale * 100)}%
          </div>
          <IconButton label="Zoom in" onClick={onZoomIn}>
            <Plus className="h-4 w-4" />
          </IconButton>
          <IconButton label="Reset zoom" onClick={onResetZoom}>
            <RotateCcw className="h-4 w-4" />
          </IconButton>
          <IconButton label="Fullscreen" onClick={onFullscreen}>
            <Expand className="h-4 w-4" />
          </IconButton>
        </div>
      </div>
    </div>
  );
}

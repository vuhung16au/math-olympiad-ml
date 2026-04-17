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
  RectangleHorizontal,
  RotateCcw,
  Rows3,
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
    <div className="fixed bottom-[calc(env(safe-area-inset-bottom)+0.5rem)] left-1/2 z-40 flex w-[calc(100%-1rem)] max-w-[1100px] -translate-x-1/2 flex-col gap-3 rounded-[24px] border border-white/45 bg-white/75 px-4 py-4 shadow-[0_16px_45px_rgba(39,18,67,0.2)] backdrop-blur-xl supports-[backdrop-filter]:bg-white/65 sm:w-[calc(100%-2rem)] sm:px-6 lg:bottom-4 lg:left-auto lg:right-4 lg:w-[260px] lg:max-w-[260px] lg:translate-x-0 lg:gap-2 lg:rounded-[20px] lg:px-3 lg:py-3">
      <div className="flex flex-wrap items-center justify-between gap-3 lg:flex-col lg:items-stretch lg:gap-2">
        <div className="lg:hidden">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
            Active booklet
          </p>
          <h1 className="text-xl font-semibold text-[var(--color-purple)] sm:text-2xl">
            {bookletTitle}
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2 lg:grid lg:grid-cols-2 lg:gap-2">
          <button
            type="button"
            onClick={onFitWidth}
            className="rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm lg:col-span-2"
          >
            Fit width
          </button>
          {/* View mode toggle */}
          <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm lg:col-span-2">
            <button
              type="button"
              onClick={viewMode === "single" ? onToggleViewMode : undefined}
              aria-label="Continuous page view"
              title="Continuous page view"
              aria-pressed={viewMode === "continuous"}
              className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium transition ${
                viewMode === "continuous"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              <Rows3 className="h-4 w-4 shrink-0" />
              <span className="hidden sm:inline">Continuous</span>
            </button>
            <button
              type="button"
              onClick={viewMode === "continuous" ? onToggleViewMode : undefined}
              aria-label="Single page view"
              title="Single page view"
              aria-pressed={viewMode === "single"}
              className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 text-sm font-medium transition ${
                viewMode === "single"
                  ? "bg-[var(--color-purple)] text-white"
                  : "text-[var(--color-purple)] hover:bg-black/5"
              }`}
            >
              <RectangleHorizontal className="h-4 w-4 shrink-0" />
              <span className="hidden sm:inline">Single Page</span>
            </button>
          </div>
          <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm lg:col-span-2">
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
            aria-label="Print"
            className="inline-flex items-center justify-center gap-2 rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm"
          >
            <Printer className="h-4 w-4" />
            <span className="lg:hidden">Print</span>
          </button>
          <a
            href={pdfUrl}
            target="_blank"
            rel="noreferrer"
            aria-label="Download PDF"
            className="inline-flex items-center justify-center gap-2 rounded-full border border-black/10 bg-[var(--color-purple)] px-4 py-2 text-sm font-medium text-white shadow-sm"
          >
            <Download className="h-4 w-4" />
            <span className="lg:hidden">Download PDF</span>
          </a>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 lg:flex-col lg:items-stretch lg:gap-2">
        <div className="flex items-center gap-2 lg:justify-between">
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

        <div className="flex flex-wrap items-center gap-2 lg:justify-between">
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

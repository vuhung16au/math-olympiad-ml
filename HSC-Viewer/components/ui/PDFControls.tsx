"use client";

import { useEffect, useRef, useState } from "react";
import type { MouseEvent as ReactMouseEvent } from "react";

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
  const panelRef = useRef<HTMLDivElement | null>(null);
  const dragOffsetRef = useRef<{ x: number; y: number } | null>(null);
  const [pageDraft, setPageDraft] = useState(String(currentPage));
  const [panelPosition, setPanelPosition] = useState<{ x: number; y: number } | null>(null);
  const [isDraggingPanel, setIsDraggingPanel] = useState(false);

  useEffect(() => {
    setPageDraft(String(currentPage));
  }, [currentPage]);

  const commitPageChange = () => {
    const parsed = Number(pageDraft);
    if (Number.isFinite(parsed)) {
      onPageChange(parsed);
    }
    setPageDraft(String(currentPage));
    onPageInputEditingChange(false);
  };

  useEffect(() => {
    if (!isDraggingPanel) {
      return;
    }

    const onMouseMove = (event: MouseEvent) => {
      const panel = panelRef.current;
      const dragOffset = dragOffsetRef.current;

      if (!panel || !dragOffset) {
        return;
      }

      const panelWidth = panel.offsetWidth;
      const panelHeight = panel.offsetHeight;
      const margin = 8;

      const nextX = Math.min(
        Math.max(event.clientX - dragOffset.x, margin),
        window.innerWidth - panelWidth - margin,
      );
      const nextY = Math.min(
        Math.max(event.clientY - dragOffset.y, margin),
        window.innerHeight - panelHeight - margin,
      );

      setPanelPosition({ x: nextX, y: nextY });
    };

    const onMouseUp = () => {
      setIsDraggingPanel(false);
      dragOffsetRef.current = null;
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, [isDraggingPanel]);

  const handlePanelDragStart = (event: ReactMouseEvent<HTMLDivElement>) => {
    if (event.button !== 0) {
      return;
    }

    if (!window.matchMedia("(min-width: 1024px)").matches) {
      return;
    }

    const panel = panelRef.current;

    if (!panel) {
      return;
    }

    const rect = panel.getBoundingClientRect();
    dragOffsetRef.current = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
    setPanelPosition({ x: rect.left, y: rect.top });
    setIsDraggingPanel(true);
    event.preventDefault();
  };

  return (
    <div
      ref={panelRef}
      style={panelPosition
        ? {
          left: `${panelPosition.x}px`,
          top: `${panelPosition.y}px`,
          right: "auto",
          bottom: "auto",
          transform: "none",
        }
        : undefined}
      className="fixed bottom-[calc(env(safe-area-inset-bottom)+0.5rem)] left-1/2 z-40 flex w-[calc(100%-1rem)] max-w-[1100px] -translate-x-1/2 flex-col gap-3 rounded-[24px] border border-white/45 bg-white/75 px-4 py-4 shadow-[0_16px_45px_rgba(39,18,67,0.2)] backdrop-blur-xl supports-[backdrop-filter]:bg-white/65 sm:w-[calc(100%-2rem)] sm:px-6 lg:bottom-5 lg:left-auto lg:right-5 lg:w-[260px] lg:max-w-[260px] lg:translate-x-0 lg:gap-2 lg:rounded-[20px] lg:px-3 lg:py-3"
    >
      <div
        role="button"
        tabIndex={0}
        aria-label="Drag toolbar"
        title="Drag toolbar"
        onMouseDown={handlePanelDragStart}
        onKeyDown={(event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
          }
        }}
        className={`hidden h-2 cursor-move rounded-full bg-[color:color-mix(in_srgb,var(--color-purple)_20%,white)] lg:block ${isDraggingPanel ? "opacity-90" : "opacity-60"}`}
      />
      <div className="flex flex-wrap items-center justify-between gap-3 lg:flex-col lg:items-stretch lg:gap-2">
        <div className="lg:hidden">
          <p className="text-xs font-semibold uppercase tracking-[0.24em] text-[var(--color-red)]">
            Active booklet
          </p>
          <h1 className="text-xl font-semibold text-[var(--color-purple)] sm:text-2xl">
            {bookletTitle}
          </h1>
        </div>

        <div className="flex w-full flex-col gap-2">
          <button
            type="button"
            onClick={onFitWidth}
            className="w-full rounded-full border border-black/10 bg-white px-4 py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm transition hover:border-[var(--color-purple)]"
          >
            Fit width
          </button>
          <div className="flex flex-wrap items-center justify-center gap-2 lg:justify-between">
            <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm">
              <button
                type="button"
                onClick={viewMode === "single" ? onToggleViewMode : undefined}
                aria-label="Continuous view"
                title="Continuous view"
                aria-pressed={viewMode === "continuous"}
                className={`inline-flex h-10 w-12 items-center justify-center transition ${
                  viewMode === "continuous"
                    ? "bg-[var(--color-purple)] text-white"
                    : "text-[var(--color-purple)] hover:bg-black/5"
                }`}
              >
                <Rows3 className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={viewMode === "continuous" ? onToggleViewMode : undefined}
                aria-label="Single page view"
                title="Single page view"
                aria-pressed={viewMode === "single"}
                className={`inline-flex h-10 w-12 items-center justify-center transition ${
                  viewMode === "single"
                    ? "bg-[var(--color-purple)] text-white"
                    : "text-[var(--color-purple)] hover:bg-black/5"
                }`}
              >
                <RectangleHorizontal className="h-4 w-4" />
              </button>
            </div>

            <div className="flex overflow-hidden rounded-full border border-black/10 bg-white shadow-sm">
              <button
                type="button"
                onClick={() => onReadingThemeChange("light")}
                aria-label="Light theme"
                title="Light theme"
                aria-pressed={readingTheme === "light"}
                className={`inline-flex h-10 w-12 items-center justify-center transition ${
                  readingTheme === "light"
                    ? "bg-[var(--color-purple)] text-white"
                    : "text-[var(--color-purple)] hover:bg-black/5"
                }`}
              >
                <Sun className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => onReadingThemeChange("dark")}
                aria-label="Dark theme"
                title="Dark theme"
                aria-pressed={readingTheme === "dark"}
                className={`inline-flex h-10 w-12 items-center justify-center transition ${
                  readingTheme === "dark"
                    ? "bg-[var(--color-purple)] text-white"
                    : "text-[var(--color-purple)] hover:bg-black/5"
                }`}
              >
                <Moon className="h-4 w-4" />
              </button>
              <button
                type="button"
                onClick={() => onReadingThemeChange("sepia")}
                aria-label="Sepia theme"
                title="Sepia theme"
                aria-pressed={readingTheme === "sepia"}
                className={`inline-flex h-10 w-12 items-center justify-center transition ${
                  readingTheme === "sepia"
                    ? "bg-[var(--color-purple)] text-white"
                    : "text-[var(--color-purple)] hover:bg-black/5"
                }`}
              >
                <Palette className="h-4 w-4" />
              </button>
            </div>

            <div className="flex items-center gap-2">
              <IconButton label="Print PDF" onClick={onPrint}>
                <Printer className="h-4 w-4" />
              </IconButton>
              <a
                href={pdfUrl}
                target="_blank"
                rel="noreferrer"
                aria-label="Download PDF"
                title="Download PDF"
                className="inline-flex h-10 w-10 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-purple)] shadow-sm transition hover:border-[var(--color-purple)]"
              >
                <Download className="h-4 w-4" />
              </a>
              <IconButton label="Fullscreen" onClick={onFullscreen}>
                <Expand className="h-4 w-4" />
              </IconButton>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 lg:flex-col lg:items-stretch lg:gap-2">
        <div className="flex items-center gap-2 lg:justify-between">
          <IconButton label="Previous page" onClick={onPreviousPage} disabled={!canGoPrevious}>
            <ChevronLeft className="h-4 w-4" />
          </IconButton>
          <div className="rounded-full border border-black/10 bg-white px-3 py-2 text-sm shadow-sm">
            <input
              type="number"
              min={1}
              max={Math.max(totalPages, 1)}
              value={pageDraft}
              onChange={(event) => setPageDraft(event.target.value)}
              onFocus={() => onPageInputEditingChange(true)}
              onBlur={() => {
                setPageDraft(String(currentPage));
                onPageInputEditingChange(false);
              }}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  event.preventDefault();
                  commitPageChange();
                  return;
                }

                if (event.key === "Escape") {
                  event.preventDefault();
                  setPageDraft(String(currentPage));
                  onPageInputEditingChange(false);
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
        </div>
      </div>
    </div>
  );
}

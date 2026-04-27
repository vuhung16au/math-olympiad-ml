"use client";

import { useEffect, useRef, useState } from "react";
import type { MouseEvent as ReactMouseEvent } from "react";

import {
  ChevronLeft,
  ChevronRight,
  ChevronsUp,
  Download,
  Expand,
  Facebook,
  Instagram,
  Link2,
  MoreHorizontal,
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
  bookletSlug: string;
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
  onShareAction?: (action: string) => void;
}

function TikTokIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className={className} fill="currentColor">
      <path d="M16.49 4.25c.49 1.4 1.61 2.52 3.01 3.01v3.21a8.1 8.1 0 0 1-3.01-.74v5.36a6.49 6.49 0 1 1-6.49-6.49c.26 0 .52.02.78.05v3.2a3.31 3.31 0 1 0 2.5 3.24V1h3.21v3.25Z" />
    </svg>
  );
}

function ShareButton({
  label,
  onClick,
  icon,
  className,
}: {
  label: string;
  onClick: () => void;
  icon: React.ReactNode;
  className: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`inline-flex h-11 w-11 items-center justify-center rounded-full text-white shadow-sm transition hover:brightness-105 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/75 ${className}`}
      aria-label={label}
      title={label}
    >
      <span className="inline-flex h-5 w-5 items-center justify-center">{icon}</span>
    </button>
  );
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
  bookletSlug,
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
  onShareAction,
}: PDFControlsProps) {
  const panelRef = useRef<HTMLDivElement | null>(null);
  const dragOffsetRef = useRef<{ x: number; y: number } | null>(null);
  const [pageDraft, setPageDraft] = useState(String(currentPage));
  const [panelPosition, setPanelPosition] = useState<{ x: number; y: number } | null>(null);
  const [isDraggingPanel, setIsDraggingPanel] = useState(false);
  const [shareMessage, setShareMessage] = useState<string | null>(null);
  const [isMobileMoreOpen, setIsMobileMoreOpen] = useState(false);

  const shareUrl = typeof window === "undefined"
    ? ""
    : `${window.location.origin}/booklets/${bookletSlug}/${Math.max(1, currentPage)}`;

  const shareTitle = `${bookletTitle} - HSC Maths Booklet`;
  const shareText = `Check out this awesome HSC math booklet on ${bookletTitle}! Perfect for students preparing for their exams.`;

  const openPopup = (url: string) => {
    const width = 640;
    const height = 640;
    const left = Math.round(window.screenX + (window.outerWidth - width) / 2);
    const top = Math.round(window.screenY + (window.outerHeight - height) / 2);

    window.open(
      url,
      "hsc-share",
      `width=${width},height=${height},left=${left},top=${top},noopener,noreferrer`,
    );
  };

  const showShareMessage = (message: string) => {
    setShareMessage(message);
  };

  const copyToClipboard = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      return true;
    } catch {
      return false;
    }
  };

  const copySharePayload = async () => {
    const copied = await copyToClipboard(`${shareText} ${shareUrl}`.trim());
    if (!copied) {
      showShareMessage("Could not access clipboard. Please copy the URL manually.");
      return false;
    }

    return true;
  };

  const handleFacebookShare = () => {
    const intent = new URL("https://www.facebook.com/sharer/sharer.php");
    intent.searchParams.set("u", shareUrl);
    intent.searchParams.set("quote", `${shareText} ${shareUrl}`.trim());
    openPopup(intent.toString());
    onShareAction?.("share_facebook");
  };

  const handleInstagramShare = async () => {
    const canUseNativeShare = typeof navigator.share === "function";
    if (canUseNativeShare) {
      try {
        await navigator.share({
          title: shareTitle,
          text: shareText,
          url: shareUrl,
        });
        onShareAction?.("share_instagram_native");
        return;
      } catch {
        // User may cancel native share; fallback handled below.
      }
    }

    const copied = await copySharePayload();
    window.open("https://www.instagram.com/", "_blank", "noopener,noreferrer");
    showShareMessage(
      copied
        ? "Caption and link copied. Paste it into your Instagram post."
        : "Instagram opened. Copy the link from the address bar.",
    );
    onShareAction?.("share_instagram_link");
  };

  const handleTikTokShare = async () => {
    const canUseNativeShare = typeof navigator.share === "function";
    if (canUseNativeShare) {
      try {
        await navigator.share({
          title: shareTitle,
          text: shareText,
          url: shareUrl,
        });
        onShareAction?.("share_tiktok_native");
        return;
      } catch {
        // User may cancel native share; fallback handled below.
      }
    }

    const copied = await copySharePayload();
    window.open("https://www.tiktok.com/upload", "_blank", "noopener,noreferrer");
    showShareMessage(
      copied
        ? "Caption and link copied. Paste it into your TikTok caption."
        : "TikTok opened. Copy the link from the address bar.",
    );
    onShareAction?.("share_tiktok_link");
  };

  const handleCopyLink = async () => {
    const copied = await copyToClipboard(shareUrl);
    showShareMessage(copied ? "Link copied to clipboard!" : "Unable to copy. Please copy the URL manually.");
    onShareAction?.("share_copy_link");
  };

  useEffect(() => {
    if (!shareMessage) {
      return;
    }

    const timer = window.setTimeout(() => setShareMessage(null), 2200);
    return () => window.clearTimeout(timer);
  }, [shareMessage]);

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

  const pageInput = (
    <div className="rounded-full border border-black/10 bg-white px-2 py-1.5 text-sm shadow-sm sm:px-3 sm:py-2">
      <input
        data-testid="page-number-input"
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
        className="w-12 bg-transparent text-center text-sm font-semibold text-[var(--color-purple)] outline-none sm:w-14"
      />
      <span className="ml-1 text-[color:color-mix(in_srgb,var(--color-charcoal)_70%,white)] sm:ml-2">
        / {totalPages || "-"}
      </span>
    </div>
  );

  const shareToolsBlock = (
    <div className="flex w-full flex-col gap-2">
      <div className="rounded-2xl border border-white/70 bg-[linear-gradient(115deg,rgba(80,67,154,0.95),rgba(224,83,114,0.92))] px-3 py-3 text-white shadow-[0_12px_30px_rgba(54,20,86,0.26)]">
        <p className="text-[10px] font-semibold uppercase tracking-[0.2em] text-white/80">
          Share this page
        </p>
        <div className="mt-2 flex flex-wrap items-center gap-2">
          <ShareButton
            label="Facebook"
            onClick={handleFacebookShare}
            icon={<Facebook className="h-4 w-4" />}
            className="bg-[#1877F2]"
          />
          <ShareButton
            label="Instagram"
            onClick={() => {
              void handleInstagramShare();
            }}
            icon={<Instagram className="h-4 w-4" />}
            className="bg-[radial-gradient(circle_at_30%_107%,#fdf497_0%,#fdf497_5%,#fd5949_45%,#d6249f_60%,#285AEB_90%)]"
          />
          <ShareButton
            label="TikTok"
            onClick={() => {
              void handleTikTokShare();
            }}
            icon={<TikTokIcon className="h-4 w-4" />}
            className="bg-[#111111]"
          />
          <ShareButton
            label="Copy link"
            onClick={() => {
              void handleCopyLink();
            }}
            icon={<Link2 className="h-4 w-4" />}
            className="bg-[color:color-mix(in_srgb,var(--color-purple)_86%,black)]"
          />
        </div>
        {shareMessage ? (
          <p className="mt-2 text-xs font-medium text-white/90" role="status" aria-live="polite">
            {shareMessage}
          </p>
        ) : null}
      </div>

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
  );

  const pageNavRow = (
    <div className="flex items-center justify-center gap-1 sm:gap-2 lg:justify-between">
      <IconButton label="Previous page" onClick={onPreviousPage} disabled={!canGoPrevious}>
        <ChevronLeft className="h-4 w-4" />
      </IconButton>
      {pageInput}
      <IconButton label="Next page" onClick={onNextPage} disabled={!canGoNext}>
        <ChevronRight className="h-4 w-4" />
      </IconButton>
    </div>
  );

  const zoomRowFull = (
    <div className="flex flex-wrap items-center justify-center gap-1 sm:gap-2 lg:justify-between">
      <IconButton label="Zoom out" onClick={onZoomOut}>
        <Minus className="h-4 w-4" />
      </IconButton>
      <div className="rounded-full border border-black/10 bg-white px-2 py-1.5 text-sm font-semibold text-[var(--color-purple)] shadow-sm sm:px-3 sm:py-2">
        <span data-testid="zoom-percentage">{Math.round(scale * 100)}%</span>
      </div>
      <IconButton label="Zoom in" onClick={onZoomIn}>
        <Plus className="h-4 w-4" />
      </IconButton>
      <IconButton label="Reset zoom" onClick={onResetZoom}>
        <RotateCcw className="h-4 w-4" />
      </IconButton>
    </div>
  );

  const zoomRowCompact = (
    <div className="flex flex-wrap items-center justify-center gap-1 sm:gap-2">
      <IconButton label="Zoom out" onClick={onZoomOut}>
        <Minus className="h-4 w-4" />
      </IconButton>
      <div className="rounded-full border border-black/10 bg-white px-2 py-1.5 text-sm font-semibold text-[var(--color-purple)] shadow-sm">
        <span data-testid="zoom-percentage">{Math.round(scale * 100)}%</span>
      </div>
      <IconButton label="Zoom in" onClick={onZoomIn}>
        <Plus className="h-4 w-4" />
      </IconButton>
    </div>
  );

  return (
    <>
      <div
        className={[
          "fixed bottom-[calc(env(safe-area-inset-bottom)+0.5rem)] left-1/2 z-40 w-[calc(100%-1rem)] max-w-[1100px] -translate-x-1/2 flex-col border border-white/45 bg-white/75 shadow-[0_16px_45px_rgba(39,18,67,0.2)] backdrop-blur-xl supports-[backdrop-filter]:bg-white/65 sm:w-[calc(100%-2rem)] lg:hidden",
          isMobileMoreOpen
            ? "flex gap-3 rounded-[24px] px-3 py-3 sm:px-5 sm:py-4"
            : "flex items-center justify-center gap-1 rounded-[20px] px-2 py-2",
        ].join(" ")}
      >
        {isMobileMoreOpen ? (
          <>
            {shareToolsBlock}
            <div className="flex w-full flex-col gap-2">
              {pageNavRow}
              {zoomRowFull}
            </div>
            <button
              type="button"
              onClick={() => setIsMobileMoreOpen(false)}
              className="inline-flex w-full items-center justify-center gap-2 rounded-full border border-black/10 bg-white py-2 text-sm font-medium text-[var(--color-purple)] shadow-sm"
              aria-label="Hide viewer tools"
              title="Hide viewer tools"
            >
              <ChevronsUp className="h-4 w-4" />
              Hide viewer tools
            </button>
          </>
        ) : (
          <div className="flex w-full flex-wrap items-center justify-center gap-x-1 gap-y-1 sm:gap-2">
            {pageNavRow}
            {zoomRowCompact}
            <button
              type="button"
              onClick={() => setIsMobileMoreOpen(true)}
              className="inline-flex h-10 w-10 shrink-0 items-center justify-center rounded-full border border-black/10 bg-white text-[var(--color-purple)] shadow-sm"
              aria-label="Show viewer tools"
              title="Show viewer tools"
              aria-expanded={false}
            >
              <MoreHorizontal className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>

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
        className="fixed bottom-5 right-5 z-40 hidden w-[260px] max-w-[260px] flex-col gap-2 rounded-[20px] border border-white/45 bg-white/75 px-3 py-3 shadow-[0_16px_45px_rgba(39,18,67,0.2)] backdrop-blur-xl supports-[backdrop-filter]:bg-white/65 lg:flex"
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
          className={`h-2 cursor-move rounded-full bg-[color:color-mix(in_srgb,var(--color-purple)_20%,white)] ${isDraggingPanel ? "opacity-90" : "opacity-60"}`}
        />
        {shareToolsBlock}
        <div className="flex w-full flex-col gap-2">
          {pageNavRow}
          {zoomRowFull}
        </div>
      </div>
    </>
  );
}

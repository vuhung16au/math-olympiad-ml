"use client";

import { useEffect, useRef, useState } from "react";
import type { MouseEvent as ReactMouseEvent } from "react";

import {
  ChevronLeft,
  ChevronRight,
  Download,
  Expand,
  Facebook,
  Instagram,
  Link2,
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

function DiscordIcon({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className={className} fill="currentColor">
      <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515a.074.074 0 0 0-.079.037c-.211.375-.445.864-.607 1.25a18.27 18.27 0 0 0-5.487 0c-.163-.386-.397-.875-.608-1.25a.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057a19.9 19.9 0 0 0 5.993 3.03a.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.042-.106c-.635-.2-1.235-.437-1.824-.718a.077.077 0 0 1-.008-.128c.122-.092.245-.19.363-.281a.075.075 0 0 1 .078-.01c3.928 1.793 8.18 1.793 12.062 0a.075.075 0 0 1 .079.009c.118.09.242.189.365.281a.077.077 0 0 1-.006.127a12.299 12.299 0 0 1-1.824.719a.077.077 0 0 0-.042.106c.352.699.764 1.365 1.224 1.993a.076.076 0 0 0 .084.028a19.839 19.839 0 0 0 6.002-3.03a.077.077 0 0 0 .032-.054c.5-4.718-.838-8.812-3.549-12.454a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.948-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.948 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419c0-1.333.948-2.419 2.157-2.419c1.21 0 2.176 1.096 2.157 2.42c0 1.333-.946 2.418-2.157 2.418Z" />
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

  const sharePath = `/booklets/${bookletSlug}/${Math.max(1, currentPage)}`;
  const getShareUrl = () =>
    typeof window === "undefined" ? sharePath : `${window.location.origin}${sharePath}`;

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
    const shareUrl = getShareUrl();
    const copied = await copyToClipboard(`${shareText} ${shareUrl}`.trim());
    if (!copied) {
      showShareMessage("Could not access clipboard. Please copy the URL manually.");
      return false;
    }

    return true;
  };

  const handleFacebookShare = () => {
    const shareUrl = getShareUrl();
    const intent = new URL("https://www.facebook.com/sharer/sharer.php");
    intent.searchParams.set("u", shareUrl);
    intent.searchParams.set("quote", `${shareText} ${shareUrl}`.trim());
    openPopup(intent.toString());
    onShareAction?.("share_facebook");
  };

  const handleInstagramShare = async () => {
    const shareUrl = getShareUrl();
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
    const shareUrl = getShareUrl();
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

  const handleDiscordShare = () => {
    window.open("https://discord.gg/MPT3FFkg", "_blank", "noopener,noreferrer");
    showShareMessage("Discord server opened. Join us!");
    onShareAction?.("share_discord");
  };

  const handleCopyLink = async () => {
    const shareUrl = getShareUrl();
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
                label="Discord"
                onClick={handleDiscordShare}
                icon={<DiscordIcon className="h-4 w-4" />}
                className="bg-[#5865F2]"
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
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 lg:flex-col lg:items-stretch lg:gap-2">
        <div className="flex items-center gap-2 lg:justify-between">
          <IconButton label="Previous page" onClick={onPreviousPage} disabled={!canGoPrevious}>
            <ChevronLeft className="h-4 w-4" />
          </IconButton>
          <div className="rounded-full border border-black/10 bg-white px-3 py-2 text-sm shadow-sm">
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
            <span data-testid="zoom-percentage">{Math.round(scale * 100)}%</span>
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

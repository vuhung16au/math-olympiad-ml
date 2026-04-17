"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import "react-pdf/dist/Page/AnnotationLayer.css";
import "react-pdf/dist/Page/TextLayer.css";
import type { Booklet } from "@/lib/booklets";
import PDFControls from "@/components/ui/PDFControls";
import LoadingSpinner from "@/components/ui/LoadingSpinner";
import ErrorBoundary from "@/components/ui/ErrorBoundary";
import { PDF_DEFAULTS } from "@/lib/constants";
import {
  trackBookletOpened,
  trackPdfAction,
  trackPdfNavigation,
  trackPdfZoom,
} from "@/lib/analytics";
import { validatePageNumber, validateScale } from "@/lib/pdf-helpers";

pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.mjs`;

type PDFViewerProps = {
  booklet: Booklet;
  initialPage?: number;
};

type ReadingTheme = "light" | "dark" | "sepia";

export default function PDFViewer({ booklet, initialPage = 1 }: PDFViewerProps) {
  const stageRef = useRef<HTMLDivElement | null>(null);
  const lastWheelNavigationRef = useRef(0);
  const syncUrlTimerRef = useRef<number | null>(null);
  const didInitialJumpRef = useRef(false);
  const pageRefs = useRef<Map<number, HTMLDivElement>>(new Map());
  const currentPageRef = useRef(1);
  const [numPages, setNumPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(Math.max(1, Math.floor(initialPage)));
  const [viewMode, setViewMode] = useState<"single" | "continuous">("continuous");
  const [readingTheme, setReadingTheme] = useState<ReadingTheme>("light");
  const [scale, setScale] = useState(PDF_DEFAULTS.defaultScale);
  const [containerWidth, setContainerWidth] = useState(900);
  const [containerHeight, setContainerHeight] = useState(700);
  const [error, setError] = useState<string | null>(null);
  const [isPageInputEditing, setIsPageInputEditing] = useState(false);
  const [isFullscreenStage, setIsFullscreenStage] = useState(false);
  const [isDesktopLandscape, setIsDesktopLandscape] = useState(false);

  // Keep ref in sync so effects can read latest value without stale closures
  currentPageRef.current = currentPage;

  useEffect(() => {
    trackBookletOpened(booklet.title);
  }, [booklet.title]);

  // Reset jump state whenever a new booklet/page combination is loaded.
  useEffect(() => {
    didInitialJumpRef.current = false;
  }, [booklet.slug, initialPage]);

  // Scroll to a specific page in continuous mode
  const scrollToPage = useCallback((pageNum: number) => {
    const el = pageRefs.current.get(pageNum);
    if (el) {
      el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    setCurrentPage(pageNum);
    trackPdfNavigation(booklet.title, pageNum, numPages);
  }, [booklet.title, numPages]);

  // IntersectionObserver: track the most-visible page in continuous mode
  useEffect(() => {
    if (viewMode !== "continuous" || numPages === 0) return;

    const ratioMap = new Map<number, number>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          const n = Number((entry.target as HTMLElement).dataset.pageNumber);
          if (n) ratioMap.set(n, entry.intersectionRatio);
        }
        let maxRatio = -1;
        let mostVisible = currentPageRef.current;
        ratioMap.forEach((ratio, pageNum) => {
          if (ratio > maxRatio) { maxRatio = ratio; mostVisible = pageNum; }
        });
        if (maxRatio > 0) setCurrentPage(mostVisible);
      },
      { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] },
    );

    pageRefs.current.forEach((el, pageNum) => {
      el.dataset.pageNumber = String(pageNum);
      observer.observe(el);
    });

    return () => observer.disconnect();
  }, [viewMode, numPages]);

  // For deep links like /booklets/:slug/:page, jump once after pages mount in continuous mode.
  useEffect(() => {
    if (didInitialJumpRef.current) {
      return;
    }

    if (viewMode !== "continuous" || numPages === 0) {
      return;
    }

    const targetPage = validatePageNumber(initialPage, numPages);
    if (targetPage <= 1) {
      didInitialJumpRef.current = true;
      return;
    }

    const timer = window.setTimeout(() => {
      const el = pageRefs.current.get(targetPage);
      if (!el) {
        return;
      }

      el.scrollIntoView({ block: "start" });
      setCurrentPage(targetPage);
      didInitialJumpRef.current = true;
    }, 120);

    return () => window.clearTimeout(timer);
  }, [initialPage, numPages, viewMode]);

  // When switching to continuous mode, scroll to the page that was active in single mode
  useEffect(() => {
    if (viewMode === "continuous" && numPages > 0) {
      const target = currentPageRef.current;
      setTimeout(() => {
        const el = pageRefs.current.get(target);
        if (el) el.scrollIntoView({ block: "start" });
      }, 80);
    }
    // Only run when viewMode or numPages changes, not on every page change
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [viewMode, numPages]);

  useEffect(() => {
    const node = stageRef.current;

    if (!node) {
      return;
    }

    const observer = new ResizeObserver((entries) => {
      const entry = entries[0];
      if (!entry) {
        return;
      }
      setContainerWidth(Math.max(280, Math.floor(entry.contentRect.width - 32)));
      setContainerHeight(Math.max(360, Math.floor(entry.contentRect.height - 24)));
    });

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const safePage = useMemo(
    () => validatePageNumber(currentPage, numPages),
    [currentPage, numPages],
  );

  const isTwoPageSpread = isFullscreenStage && isDesktopLandscape;
  const displayPage = isTwoPageSpread && safePage % 2 === 0 ? safePage - 1 : safePage;
  const spreadPageHeight = Math.max(320, Math.floor(containerHeight - 36));

  const pageStep = isTwoPageSpread ? 2 : 1;

  const pdfFilter = useMemo(() => {
    if (readingTheme === "dark") {
      // Invert + hue-rotate keeps black text readable on dark backgrounds.
      return "invert(1) hue-rotate(180deg) brightness(0.95) contrast(0.93)";
    }

    if (readingTheme === "sepia") {
      return "sepia(0.82) saturate(0.8) brightness(0.94) contrast(0.92)";
    }

    return "none";
  }, [readingTheme]);

  const canGoPrevious = viewMode === "continuous" ? currentPage > 1 : displayPage > 1;
  const canGoNext =
    viewMode === "continuous"
      ? numPages > 0 && currentPage < numPages
      : numPages > 0 && displayPage + pageStep <= numPages;

  const handlePageChange = useCallback(
    (page: number) => {
      const rawPage = validatePageNumber(page, numPages);
      if (viewMode === "continuous") {
        scrollToPage(rawPage);
        return;
      }
      const nextPage = isTwoPageSpread && rawPage % 2 === 0 ? rawPage - 1 : rawPage;
      setCurrentPage(nextPage);
      trackPdfNavigation(booklet.title, nextPage, numPages);
    },
    [booklet.title, isTwoPageSpread, numPages, scrollToPage, viewMode],
  );

  const handleNextPage = useCallback(() => {
    if (viewMode === "continuous") {
      const next = Math.min(currentPage + 1, numPages);
      if (next !== currentPage) scrollToPage(next);
      return;
    }
    if (!canGoNext) {
      return;
    }
    handlePageChange(displayPage + pageStep);
  }, [canGoNext, currentPage, displayPage, handlePageChange, numPages, pageStep, scrollToPage, viewMode]);

  const handlePreviousPage = useCallback(() => {
    if (viewMode === "continuous") {
      const prev = Math.max(currentPage - 1, 1);
      if (prev !== currentPage) scrollToPage(prev);
      return;
    }
    if (!canGoPrevious) {
      return;
    }
    handlePageChange(displayPage - pageStep);
  }, [canGoPrevious, currentPage, displayPage, handlePageChange, pageStep, scrollToPage, viewMode]);

  useEffect(() => {
    const updateViewportMode = () => {
      const isLandscape = window.matchMedia("(orientation: landscape)").matches;
      const isDesktop = window.matchMedia(`(min-width: ${PDF_DEFAULTS.desktopSpreadMinWidth}px)`).matches;
      setIsDesktopLandscape(isLandscape && isDesktop);
      setIsFullscreenStage(document.fullscreenElement === stageRef.current);
    };

    updateViewportMode();
    window.addEventListener("resize", updateViewportMode);
    window.addEventListener("orientationchange", updateViewportMode);
    document.addEventListener("fullscreenchange", updateViewportMode);

    return () => {
      window.removeEventListener("resize", updateViewportMode);
      window.removeEventListener("orientationchange", updateViewportMode);
      document.removeEventListener("fullscreenchange", updateViewportMode);
    };
  }, []);

  const handleFitWidth = () => {
    if (!containerWidth) {
      return;
    }

    const fitScale = validateScale(containerWidth / 800);
    setScale(fitScale);
    trackPdfAction(booklet.title, "fit_width");
  };

  const handleFullscreen = useCallback(async () => {
    if (!stageRef.current) {
      return;
    }

    try {
      if (document.fullscreenElement) {
        await document.exitFullscreen();
        trackPdfAction(booklet.title, "exit_fullscreen");
        return;
      }

      await stageRef.current.requestFullscreen();
      trackPdfAction(booklet.title, "enter_fullscreen");
    } catch {
      // Fullscreen can fail when blocked by browser settings or unsupported contexts.
    }
  }, [booklet.title]);

  useEffect(() => {
    const isInteractiveElement = (target: EventTarget | null): boolean => {
      if (!(target instanceof HTMLElement)) {
        return false;
      }
      const tagName = target.tagName;
      return (
        target.isContentEditable ||
        tagName === "INPUT" ||
        tagName === "TEXTAREA" ||
        tagName === "SELECT" ||
        tagName === "BUTTON"
      );
    };

    const onKeyDown = (event: KeyboardEvent) => {
      if (isInteractiveElement(event.target)) {
        return;
      }

      if (event.metaKey || event.ctrlKey || event.altKey) {
        return;
      }

      // In continuous mode, let the browser handle arrow/space scrolling naturally
      if (viewMode === "continuous") {
        if (event.key.toLowerCase() === "f") {
          if (event.repeat) return;
          event.preventDefault();
          void handleFullscreen();
        }
        return;
      }

      if (
        event.key === "ArrowRight" ||
        event.key === "ArrowDown" ||
        event.key === "PageDown" ||
        event.key === " " ||
        event.code === "Space"
      ) {
        event.preventDefault();
        handleNextPage();
        return;
      }

      if (event.key === "ArrowLeft" || event.key === "ArrowUp" || event.key === "PageUp") {
        event.preventDefault();
        handlePreviousPage();
        return;
      }

      if (event.key.toLowerCase() === "f") {
        if (event.repeat) {
          return;
        }
        event.preventDefault();
        void handleFullscreen();
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [handleFullscreen, handleNextPage, handlePreviousPage, viewMode]);

  useEffect(() => {
    const stage = stageRef.current;

    if (!stage) {
      return;
    }

    const onWheel = (event: WheelEvent) => {
      if (document.fullscreenElement !== stage) {
        return;
      }

      // In continuous mode let native scrolling work
      if (viewMode === "continuous") {
        return;
      }

      if (Math.abs(event.deltaY) < 12) {
        return;
      }

      const now = Date.now();
      if (now - lastWheelNavigationRef.current < 220) {
        event.preventDefault();
        return;
      }

      const isScrollDown = event.deltaY > 0;
      if (isScrollDown && canGoNext) {
        event.preventDefault();
        lastWheelNavigationRef.current = now;
        handleNextPage();
        return;
      }

      if (!isScrollDown && canGoPrevious) {
        event.preventDefault();
        lastWheelNavigationRef.current = now;
        handlePreviousPage();
      }
    };

    stage.addEventListener("wheel", onWheel, { passive: false });
    return () => stage.removeEventListener("wheel", onWheel);
  }, [canGoNext, canGoPrevious, handleNextPage, handlePreviousPage, viewMode]);

  const handlePrint = () => {
    const printWindow = window.open(booklet.pdfUrl, "_blank", "noopener,noreferrer");
    printWindow?.focus();
    trackPdfAction(booklet.title, "print");
  };

  // Keep URL in sync with the current page using replaceState — no Next.js navigation,
  // so the component never remounts and TextLayer tasks are never aborted.
  useEffect(() => {
    if (numPages === 0) {
      return;
    }

    if (isPageInputEditing) {
      return;
    }

    const pageForUrl = viewMode === "continuous"
      ? validatePageNumber(currentPage, numPages)
      : validatePageNumber(displayPage, numPages);
    const nextPath = `/booklets/${booklet.slug}/${pageForUrl}`;

    if (window.location.pathname === nextPath) {
      return;
    }

    if (viewMode === "continuous") {
      if (syncUrlTimerRef.current) {
        window.clearTimeout(syncUrlTimerRef.current);
      }

      syncUrlTimerRef.current = window.setTimeout(() => {
        window.history.replaceState(null, "", nextPath);
        syncUrlTimerRef.current = null;
      }, 220);

      return;
    }

    window.history.replaceState(null, "", nextPath);
  }, [booklet.slug, currentPage, displayPage, isPageInputEditing, numPages, viewMode]);

  useEffect(() => {
    return () => {
      if (syncUrlTimerRef.current) {
        window.clearTimeout(syncUrlTimerRef.current);
      }
    };
  }, []);

  return (
    <ErrorBoundary>
      <section className="px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <div className="mx-auto max-w-[1280px] overflow-hidden rounded-[32px] border border-black/8 bg-white shadow-[0_24px_70px_rgba(60,16,83,0.08)]">
          <PDFControls
            bookletTitle={booklet.title}
            pdfUrl={booklet.pdfUrl}
            currentPage={viewMode === "continuous" ? currentPage : displayPage}
            totalPages={numPages}
            scale={scale}
            canGoPrevious={canGoPrevious}
            canGoNext={canGoNext}
            onPageChange={handlePageChange}
            onPreviousPage={handlePreviousPage}
            onNextPage={handleNextPage}
            viewMode={viewMode}
            onToggleViewMode={() => setViewMode((m) => (m === "continuous" ? "single" : "continuous"))}
            readingTheme={readingTheme}
            onReadingThemeChange={(theme) => {
              setReadingTheme(theme);
              trackPdfAction(booklet.title, `reading_theme_${theme}`);
            }}
            onPageInputEditingChange={setIsPageInputEditing}
            onZoomIn={() => {
              setScale((current) => {
                const nextScale = validateScale(current + PDF_DEFAULTS.scaleStep);
                trackPdfZoom(booklet.title, Math.round(nextScale * 100));
                return nextScale;
              });
            }}
            onZoomOut={() => {
              setScale((current) => {
                const nextScale = validateScale(current - PDF_DEFAULTS.scaleStep);
                trackPdfZoom(booklet.title, Math.round(nextScale * 100));
                return nextScale;
              });
            }}
            onResetZoom={() => {
              setScale(PDF_DEFAULTS.defaultScale);
              trackPdfZoom(booklet.title, Math.round(PDF_DEFAULTS.defaultScale * 100));
            }}
            onFitWidth={handleFitWidth}
            onFullscreen={() => {
              void handleFullscreen();
            }}
            onPrint={handlePrint}
          />

          {error ? (
            <div className="p-6">
              <div className="rounded-[28px] border border-red-200 bg-red-50 p-6 text-red-700">
                <p className="font-semibold">Failed to load PDF.</p>
                <p className="mt-2 text-sm leading-6">
                  Please check your connection and try again. If the issue persists, open the raw PDF directly in a new tab.
                </p>
                <a
                  href={booklet.pdfUrl}
                  target="_blank"
                  rel="noreferrer"
                  onClick={() => trackPdfAction(booklet.title, "open_raw_pdf")}
                  className="mt-4 inline-flex rounded-full bg-red-600 px-4 py-2 text-sm font-medium text-white"
                >
                  Open raw PDF
                </a>
              </div>
            </div>
          ) : null}

          <div ref={stageRef} data-pdf-stage className="min-h-[70vh] bg-[color:color-mix(in_srgb,var(--color-ivory)_72%,white)] p-3 sm:p-5">
            <Document
              file={booklet.pdfUrl}
              loading={<LoadingSpinner label="Loading PDF document" />}
              onLoadSuccess={({ numPages: loadedPages }) => {
                setNumPages(loadedPages);
                setCurrentPage((page) => validatePageNumber(page, loadedPages));
                setError(null);
              }}
              onLoadError={() => {
                setError("load-error");
              }}
              error={null}
              className="max-w-full"
            >
              {viewMode === "continuous" ? (
                /* Continuous mode: all pages stacked, native browser scroll */
                <div className="flex flex-col items-center gap-6 py-2">
                  {Array.from({ length: numPages }, (_, i) => i + 1).map((pageNum) => (
                    <div
                      key={pageNum}
                      ref={(el) => {
                        if (el) pageRefs.current.set(pageNum, el);
                        else pageRefs.current.delete(pageNum);
                      }}
                      style={{ filter: pdfFilter }}
                    >
                      <Page
                        pageNumber={pageNum}
                        scale={scale}
                        width={Math.min(containerWidth, 1080)}
                        loading={pageNum === 1 ? <LoadingSpinner label="Rendering page" /> : undefined}
                        renderTextLayer
                        renderAnnotationLayer
                        className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                      />
                    </div>
                  ))}
                </div>
              ) : (
                /* Single page mode (original behavior) */
                <div className="mx-auto flex max-w-full justify-center overflow-auto">
                  <div
                    className={`flex max-w-full ${isTwoPageSpread ? "items-start justify-center gap-5 -mt-2" : "justify-center"}`}
                    style={{ filter: pdfFilter }}
                  >
                    <Page
                      pageNumber={displayPage}
                      scale={isTwoPageSpread ? 1 : scale}
                      width={isTwoPageSpread ? undefined : Math.min(containerWidth, 1080)}
                      height={isTwoPageSpread ? spreadPageHeight : undefined}
                      loading={<LoadingSpinner label="Rendering page" />}
                      renderTextLayer
                      renderAnnotationLayer
                      className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                    />
                    {isTwoPageSpread && displayPage + 1 <= numPages ? (
                      <Page
                        pageNumber={displayPage + 1}
                        scale={1}
                        height={spreadPageHeight}
                        loading={<LoadingSpinner label="Rendering page" />}
                        renderTextLayer
                        renderAnnotationLayer
                        className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                      />
                    ) : null}
                  </div>
                </div>
              )}
            </Document>
          </div>
        </div>
      </section>
    </ErrorBoundary>
  );
}

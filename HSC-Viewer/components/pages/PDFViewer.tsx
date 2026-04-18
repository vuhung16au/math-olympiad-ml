"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { MouseEvent as ReactMouseEvent } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import { FileText, ListTree } from "lucide-react";
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
import {
  getLastPageForSlug,
  getPref,
  PREF_KEYS,
  setLastPageForSlug,
  setPref,
} from "@/lib/preferences";

pdfjs.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.mjs`;

// PDF.js frequently cancels in-flight text layer tasks during rerenders/navigation.
// Suppress this known benign warning at module scope so it is filtered before
// any pdf.js rendering begins (useEffect fires too late).
if (typeof window !== "undefined") {
  const _filterTextLayerWarning = (original: (...a: unknown[]) => void) =>
    (...args: unknown[]) => {
      const msg = typeof args[0] === "string" ? args[0] : "";
      if (msg.includes("AbortException: TextLayer task cancelled")) return;
      original(...args);
    };
  console.warn = _filterTextLayerWarning(console.warn);
  console.error = _filterTextLayerWarning(console.error);
}

type PDFViewerProps = {
  booklet: Booklet;
  initialPage?: number;
};

type ReadingTheme = "light" | "dark" | "sepia";

type OutlineTab = "pages" | "outline";

type OutlineItem = {
  id: string;
  title: string;
  page: number;
  level: number;
};

type E2EPdfMockMode = "off" | "success" | "error";

const E2E_MOCK_TOTAL_PAGES = 8;
const E2E_MOCK_OUTLINE: OutlineItem[] = [
  { id: "e2e-outline-1", title: "Introduction", page: 1, level: 0 },
  { id: "e2e-outline-2", title: "Chapter 1", page: 2, level: 0 },
  { id: "e2e-outline-3", title: "Chapter 2", page: 4, level: 0 },
  { id: "e2e-outline-4", title: "Worked Example", page: 5, level: 1 },
  { id: "e2e-outline-5", title: "Exercises", page: 7, level: 0 },
];
const IS_E2E_PDF_MOCK_ENABLED = process.env.NEXT_PUBLIC_E2E_MOCK_PDF === "1";

type PdfReference = {
  num: number;
  gen: number;
};

type PdfOutlineNode = {
  title?: string;
  dest?: unknown;
  items?: PdfOutlineNode[];
};

type PdfDocumentLike = {
  getOutline: () => Promise<PdfOutlineNode[] | null>;
  getDestination: (destination: string) => Promise<unknown>;
  getPageIndex: (ref: PdfReference) => Promise<number>;
};

function isPdfReference(value: unknown): value is PdfReference {
  if (!value || typeof value !== "object") {
    return false;
  }

  const maybeRef = value as Partial<PdfReference>;
  return typeof maybeRef.num === "number" && typeof maybeRef.gen === "number";
}

async function resolveOutlinePage(
  pdf: PdfDocumentLike,
  destination: unknown,
  namedDestinationCache: Map<string, number>,
  referenceCache: Map<string, number>,
): Promise<number | null> {
  if (!destination) {
    return null;
  }

  let explicitDestination: unknown = destination;

  if (typeof destination === "string") {
    const cachedPage = namedDestinationCache.get(destination);
    if (cachedPage) {
      return cachedPage;
    }

    explicitDestination = await pdf.getDestination(destination);
    if (!explicitDestination) {
      return null;
    }
  }

  if (!Array.isArray(explicitDestination) || explicitDestination.length === 0) {
    return null;
  }

  const target = explicitDestination[0];

  if (typeof target === "number" && Number.isFinite(target)) {
    return target + 1;
  }

  if (!isPdfReference(target)) {
    return null;
  }

  const refKey = `${target.num}_${target.gen}`;
  const cachedRefPage = referenceCache.get(refKey);

  if (cachedRefPage) {
    return cachedRefPage;
  }

  const pageIndex = await pdf.getPageIndex(target);
  const page = pageIndex + 1;
  referenceCache.set(refKey, page);

  return page;
}

async function extractOutlineItems(pdf: PdfDocumentLike, totalPages: number): Promise<OutlineItem[]> {
  const rawOutline = await pdf.getOutline();
  if (!rawOutline || rawOutline.length === 0) {
    return [];
  }

  const outline: OutlineItem[] = [];
  const namedDestinationCache = new Map<string, number>();
  const referenceCache = new Map<string, number>();
  let idCounter = 0;

  const walk = async (nodes: PdfOutlineNode[], level: number) => {
    for (const node of nodes) {
      const resolvedPage = await resolveOutlinePage(
        pdf,
        node.dest,
        namedDestinationCache,
        referenceCache,
      );

      if (resolvedPage && resolvedPage >= 1 && resolvedPage <= totalPages) {
        outline.push({
          id: `outline-${idCounter}`,
          title: (node.title ?? "Untitled section").trim() || "Untitled section",
          page: resolvedPage,
          level,
        });
        idCounter += 1;
      }

      if (node.items && node.items.length > 0) {
        await walk(node.items, level + 1);
      }
    }
  };

  await walk(rawOutline, 0);

  return outline;
}

export default function PDFViewer({ booklet, initialPage = 1 }: PDFViewerProps) {
  const stageRef = useRef<HTMLDivElement | null>(null);
  const navigatorRef = useRef<HTMLElement | null>(null);
  const lastWheelNavigationRef = useRef(0);
  const syncUrlTimerRef = useRef<number | null>(null);
  const didInitialJumpRef = useRef(false);
  const navigatorDragOffsetRef = useRef<{ x: number; y: number } | null>(null);
  const pageRefs = useRef<Map<number, HTMLDivElement>>(new Map());
  const currentPageRef = useRef(1);
  const [numPages, setNumPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(Math.max(1, Math.floor(initialPage)));
  const [viewMode, setViewMode] = useState<"single" | "continuous">("continuous");
  const [readingTheme, setReadingTheme] = useState<ReadingTheme>("light");
  const [scale, setScale] = useState(PDF_DEFAULTS.defaultScale);
  const [arePrefsHydrated, setArePrefsHydrated] = useState(false);
  const [containerWidth, setContainerWidth] = useState(900);
  const [containerHeight, setContainerHeight] = useState(700);
  const [error, setError] = useState<string | null>(null);
  const [isPageInputEditing, setIsPageInputEditing] = useState(false);
  const [isFullscreenStage, setIsFullscreenStage] = useState(false);
  const [isDesktopLandscape, setIsDesktopLandscape] = useState(false);
  const [outlineTab, setOutlineTab] = useState<OutlineTab>("pages");
  const [outlineItems, setOutlineItems] = useState<OutlineItem[]>([]);
  const [isOutlineLoading, setIsOutlineLoading] = useState(false);
  const [outlineError, setOutlineError] = useState<string | null>(null);
  const [navigatorPosition, setNavigatorPosition] = useState<{ x: number; y: number } | null>(null);
  const [isDraggingNavigator, setIsDraggingNavigator] = useState(false);
  const [e2ePdfMockMode, setE2EPdfMockMode] = useState<E2EPdfMockMode>("off");

  // Keep ref in sync so effects can read latest value without stale closures
  useEffect(() => {
    currentPageRef.current = currentPage;
  }, [currentPage]);

  useEffect(() => {
    const requestedMode = new URLSearchParams(window.location.search).get("e2ePdfMock");
    if (requestedMode === "success") {
      setE2EPdfMockMode("success");
      return;
    }

    if (requestedMode === "off") {
      setE2EPdfMockMode("off");
      return;
    }

    if (requestedMode === "error") {
      setE2EPdfMockMode("error");
      return;
    }

    setE2EPdfMockMode(IS_E2E_PDF_MOCK_ENABLED ? "success" : "off");
  }, []);

  useEffect(() => {
    if (e2ePdfMockMode === "off") {
      return;
    }

    if (e2ePdfMockMode === "error") {
      setNumPages(0);
      setError("load-error");
      setOutlineItems([]);
      setIsOutlineLoading(false);
      setOutlineError(null);
      return;
    }

    setNumPages(E2E_MOCK_TOTAL_PAGES);
    setError(null);
    setCurrentPage((page) => validatePageNumber(page, E2E_MOCK_TOTAL_PAGES));
    setOutlineItems(E2E_MOCK_OUTLINE);
    setIsOutlineLoading(false);
    setOutlineError(null);
  }, [e2ePdfMockMode]);

  // Hydrate client-only toolbar preferences after mount to avoid SSR hydration mismatches.
  useEffect(() => {
    const savedViewMode = getPref(PREF_KEYS.viewMode);
    if (savedViewMode === "single" || savedViewMode === "continuous") {
      setViewMode(savedViewMode);
    }

    const savedReadingTheme = getPref(PREF_KEYS.readingTheme);
    if (savedReadingTheme === "light" || savedReadingTheme === "dark" || savedReadingTheme === "sepia") {
      setReadingTheme(savedReadingTheme);
    }

    const savedScale = getPref(PREF_KEYS.scale);
    if (savedScale) {
      const parsed = parseFloat(savedScale);
      setScale(validateScale(Number.isFinite(parsed) ? parsed : PDF_DEFAULTS.defaultScale));
    }

    const savedOutlineTab = getPref(PREF_KEYS.outlineTab);
    if (savedOutlineTab === "pages" || savedOutlineTab === "outline") {
      setOutlineTab(savedOutlineTab);
    }

    const savedNavPanelPos = getPref(PREF_KEYS.navPanelPos);
    if (savedNavPanelPos && window.matchMedia("(min-width: 1024px)").matches) {
      const [rawX, rawY] = savedNavPanelPos.split(",");
      const x = Number(rawX);
      const y = Number(rawY);

      if (Number.isFinite(x) && Number.isFinite(y)) {
        setNavigatorPosition({ x, y });
      }
    }

    if (initialPage === 1) {
      const savedPageForBooklet = getLastPageForSlug(booklet.slug);
      if (savedPageForBooklet) {
        setCurrentPage(Math.max(1, Math.floor(savedPageForBooklet)));
      }
    }

    setArePrefsHydrated(true);
  }, [booklet.slug, initialPage]);

  // Persist toolbar preferences to cookies
  useEffect(() => {
    if (!arePrefsHydrated) return;
    setPref(PREF_KEYS.viewMode, viewMode);
  }, [arePrefsHydrated, viewMode]);

  useEffect(() => {
    if (!arePrefsHydrated) return;
    setPref(PREF_KEYS.readingTheme, readingTheme);
  }, [arePrefsHydrated, readingTheme]);

  useEffect(() => {
    if (!arePrefsHydrated) return;
    setPref(PREF_KEYS.scale, String(scale));
  }, [arePrefsHydrated, scale]);

  useEffect(() => {
    if (!arePrefsHydrated) return;
    setPref(PREF_KEYS.outlineTab, outlineTab);
  }, [arePrefsHydrated, outlineTab]);

  useEffect(() => {
    if (!arePrefsHydrated || !navigatorPosition || isDraggingNavigator) {
      return;
    }

    setPref(PREF_KEYS.navPanelPos, `${Math.round(navigatorPosition.x)},${Math.round(navigatorPosition.y)}`);
  }, [arePrefsHydrated, isDraggingNavigator, navigatorPosition]);

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

  const safeCurrentPage = useMemo(
    () => validatePageNumber(currentPage, numPages),
    [currentPage, numPages],
  );

  const isTwoPageSpread = isFullscreenStage && isDesktopLandscape;
  const spreadStartPage = isTwoPageSpread && safeCurrentPage % 2 === 0
    ? safeCurrentPage - 1
    : safeCurrentPage;
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

  const canGoPrevious = viewMode === "continuous" ? currentPage > 1 : spreadStartPage > 1;
  const canGoNext =
    viewMode === "continuous"
      ? numPages > 0 && currentPage < numPages
      : numPages > 0 && spreadStartPage + pageStep <= numPages;

  const handlePageChange = useCallback(
    (page: number) => {
      const rawPage = validatePageNumber(page, numPages);
      if (viewMode === "continuous") {
        scrollToPage(rawPage);
        return;
      }
      setCurrentPage(rawPage);
      trackPdfNavigation(booklet.title, rawPage, numPages);
    },
    [booklet.title, numPages, scrollToPage, viewMode],
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
    handlePageChange(spreadStartPage + pageStep);
  }, [canGoNext, currentPage, handlePageChange, numPages, pageStep, scrollToPage, spreadStartPage, viewMode]);

  const handlePreviousPage = useCallback(() => {
    if (viewMode === "continuous") {
      const prev = Math.max(currentPage - 1, 1);
      if (prev !== currentPage) scrollToPage(prev);
      return;
    }
    if (!canGoPrevious) {
      return;
    }
    handlePageChange(spreadStartPage - pageStep);
  }, [canGoPrevious, currentPage, handlePageChange, pageStep, scrollToPage, spreadStartPage, viewMode]);

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

  const handleTextLayerError = useCallback((textLayerError: Error) => {
    // PDF.js cancels in-flight text layer tasks when pages rerender quickly.
    // Treat AbortException as expected behavior to avoid noisy console warnings.
    if (textLayerError?.name === "AbortException") {
      return;
    }

    console.error("Text layer render failed:", textLayerError);
  }, []);

  // Keep URL in sync with the current page using replaceState — no Next.js navigation,
  // so the component never remounts and TextLayer tasks are never aborted.
  useEffect(() => {
    if (numPages === 0) {
      return;
    }

    if (isPageInputEditing) {
      return;
    }

    const pageForUrl = validatePageNumber(currentPage, numPages);
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
        setPref(PREF_KEYS.lastUrl, nextPath);
        setPref(PREF_KEYS.lastSlug, booklet.slug);
        setLastPageForSlug(booklet.slug, pageForUrl);
        syncUrlTimerRef.current = null;
      }, 220);

      return;
    }

    window.history.replaceState(null, "", nextPath);
    setPref(PREF_KEYS.lastUrl, nextPath);
    setPref(PREF_KEYS.lastSlug, booklet.slug);
    setLastPageForSlug(booklet.slug, pageForUrl);
  }, [booklet.slug, currentPage, isPageInputEditing, numPages, viewMode]);

  useEffect(() => {
    return () => {
      if (syncUrlTimerRef.current) {
        window.clearTimeout(syncUrlTimerRef.current);
      }
    };
  }, []);

  useEffect(() => {
    if (!isDraggingNavigator) {
      return;
    }

    const onMouseMove = (event: MouseEvent) => {
      const panel = navigatorRef.current;
      const dragOffset = navigatorDragOffsetRef.current;

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

      setNavigatorPosition({ x: nextX, y: nextY });
    };

    const onMouseUp = () => {
      setIsDraggingNavigator(false);
      navigatorDragOffsetRef.current = null;
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);

    return () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };
  }, [isDraggingNavigator]);

  const handleNavigatorDragStart = (event: ReactMouseEvent<HTMLDivElement>) => {
    if (event.button !== 0) {
      return;
    }

    if (!window.matchMedia("(min-width: 1024px)").matches) {
      return;
    }

    const panel = navigatorRef.current;

    if (!panel) {
      return;
    }

    const rect = panel.getBoundingClientRect();
    navigatorDragOffsetRef.current = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
    };
    setNavigatorPosition({ x: rect.left, y: rect.top });
    setIsDraggingNavigator(true);
    event.preventDefault();
  };

  return (
    <ErrorBoundary>
      <section className="px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <div className="mx-auto max-w-[1280px] overflow-hidden rounded-[32px] border border-black/8 bg-white shadow-[0_24px_70px_rgba(60,16,83,0.08)]">
          <PDFControls
            bookletTitle={booklet.title}
            bookletSlug={booklet.slug}
            pdfUrl={booklet.pdfUrl}
            currentPage={viewMode === "continuous" ? currentPage : safeCurrentPage}
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
            onShareAction={(action) => {
              trackPdfAction(booklet.title, action);
            }}
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

          <div ref={stageRef} data-pdf-stage className="min-h-[70vh] bg-[color:color-mix(in_srgb,var(--color-ivory)_72%,white)] p-3 pb-[calc(env(safe-area-inset-bottom)+7.5rem)] sm:p-5 sm:pb-[calc(env(safe-area-inset-bottom)+7rem)] lg:pb-5">
            <div className="grid min-h-[66vh] gap-4 lg:grid-cols-[minmax(0,1fr)_260px]">
              <div className="order-2 lg:order-1">
                {e2ePdfMockMode === "success" ? (
                  viewMode === "continuous" ? (
                    <div className="flex flex-col items-center gap-6 py-2">
                      {Array.from({ length: numPages }, (_, i) => i + 1).map((pageNum) => (
                        <div
                          key={`mock-page-${pageNum}`}
                          ref={(el) => {
                            if (el) pageRefs.current.set(pageNum, el);
                            else pageRefs.current.delete(pageNum);
                          }}
                          style={{ filter: pdfFilter }}
                          className="w-full max-w-[1080px]"
                        >
                          <div
                            data-testid={`mock-pdf-page-${pageNum}`}
                            className="flex min-h-[520px] items-center justify-center rounded-[20px] border border-black/10 bg-white/95 text-sm font-semibold text-[var(--color-purple)] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                          >
                            Mock PDF Page {pageNum}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="mx-auto flex max-w-full justify-center overflow-auto">
                      <div
                        className={`flex max-w-full ${isTwoPageSpread ? "items-start justify-center gap-5 -mt-2" : "justify-center"}`}
                        style={{ filter: pdfFilter }}
                      >
                        <div
                          data-testid={`mock-pdf-page-${spreadStartPage}`}
                          className="flex min-h-[520px] w-[min(1080px,100%)] items-center justify-center rounded-[20px] border border-black/10 bg-white/95 text-sm font-semibold text-[var(--color-purple)] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                        >
                          Mock PDF Page {spreadStartPage}
                        </div>
                        {isTwoPageSpread && spreadStartPage + 1 <= numPages ? (
                          <div
                            data-testid={`mock-pdf-page-${spreadStartPage + 1}`}
                            className="flex min-h-[520px] w-[min(1080px,100%)] items-center justify-center rounded-[20px] border border-black/10 bg-white/95 text-sm font-semibold text-[var(--color-purple)] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                          >
                            Mock PDF Page {spreadStartPage + 1}
                          </div>
                        ) : null}
                      </div>
                    </div>
                  )
                ) : e2ePdfMockMode === "error" ? (
                  <div className="h-[2px] w-full" aria-hidden="true" />
                ) : (
                  <Document
                    file={booklet.pdfUrl}
                    loading={<LoadingSpinner label="Loading PDF document" />}
                    onLoadSuccess={(loadedDocument) => {
                      const { numPages: loadedPages } = loadedDocument;

                      setNumPages(loadedPages);
                      setCurrentPage((page) => validatePageNumber(page, loadedPages));
                      setError(null);
                      setOutlineItems([]);
                      setOutlineError(null);
                      setIsOutlineLoading(true);

                      void (async () => {
                        try {
                          const outline = await extractOutlineItems(
                            loadedDocument as unknown as PdfDocumentLike,
                            loadedPages,
                          );
                          setOutlineItems(outline);
                        } catch {
                          setOutlineError("outline-error");
                        } finally {
                          setIsOutlineLoading(false);
                        }
                      })();
                    }}
                    onLoadError={() => {
                      setError("load-error");
                      setOutlineItems([]);
                      setIsOutlineLoading(false);
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
                              onRenderTextLayerError={handleTextLayerError}
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
                            pageNumber={spreadStartPage}
                            scale={isTwoPageSpread ? 1 : scale}
                            width={isTwoPageSpread ? undefined : Math.min(containerWidth, 1080)}
                            height={isTwoPageSpread ? spreadPageHeight : undefined}
                            loading={<LoadingSpinner label="Rendering page" />}
                            renderTextLayer
                            renderAnnotationLayer
                            onRenderTextLayerError={handleTextLayerError}
                            className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                          />
                          {isTwoPageSpread && spreadStartPage + 1 <= numPages ? (
                            <Page
                              pageNumber={spreadStartPage + 1}
                              scale={1}
                              height={spreadPageHeight}
                              loading={<LoadingSpinner label="Rendering page" />}
                              renderTextLayer
                              renderAnnotationLayer
                              onRenderTextLayerError={handleTextLayerError}
                              className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                            />
                          ) : null}
                        </div>
                      </div>
                    )}
                  </Document>
                )}
              </div>

              <aside
                ref={navigatorRef}
                style={navigatorPosition
                  ? {
                    position: "fixed",
                    left: `${navigatorPosition.x}px`,
                    top: `${navigatorPosition.y}px`,
                    right: "auto",
                    transform: "none",
                    zIndex: 45,
                  }
                  : undefined}
                className="order-1 max-h-[66vh] overflow-hidden rounded-[20px] border border-black/10 bg-white/88 lg:order-2 lg:sticky lg:top-5 lg:self-start lg:max-h-[calc(100vh-18rem)] lg:w-[260px]"
                aria-label="PDF navigation sidebar"
              >
                <div
                  role="button"
                  tabIndex={0}
                  aria-label="Drag navigator"
                  title="Drag navigator"
                  onMouseDown={handleNavigatorDragStart}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" || event.key === " ") {
                      event.preventDefault();
                    }
                  }}
                  className={`hidden h-2 cursor-move rounded-full bg-[color:color-mix(in_srgb,var(--color-purple)_20%,white)] lg:mx-2 lg:mt-2 lg:block ${isDraggingNavigator ? "opacity-90" : "opacity-60"}`}
                />
                <div className="border-b border-black/8 p-2">
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      type="button"
                      onClick={() => setOutlineTab("pages")}
                      aria-pressed={outlineTab === "pages"}
                      className={`inline-flex items-center justify-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition ${
                        outlineTab === "pages"
                          ? "bg-[var(--color-purple)] text-white"
                          : "text-[var(--color-purple)] hover:bg-[color:color-mix(in_srgb,var(--color-purple)_10%,white)]"
                      }`}
                    >
                      <FileText className="h-4 w-4" />
                      Pages
                    </button>
                    <button
                      type="button"
                      onClick={() => setOutlineTab("outline")}
                      aria-pressed={outlineTab === "outline"}
                      className={`inline-flex items-center justify-center gap-2 rounded-xl px-3 py-2 text-sm font-medium transition ${
                        outlineTab === "outline"
                          ? "bg-[var(--color-purple)] text-white"
                          : "text-[var(--color-purple)] hover:bg-[color:color-mix(in_srgb,var(--color-purple)_10%,white)]"
                      }`}
                    >
                      <ListTree className="h-4 w-4" />
                      Outline
                    </button>
                  </div>
                </div>

                {outlineTab === "pages" ? (
                  <div className="max-h-[calc(66vh-58px)] overflow-y-auto p-3 lg:max-h-[calc(100vh-21.5rem)]">
                    {numPages > 0 ? (
                      <div className="grid grid-cols-4 gap-2">
                        {Array.from({ length: numPages }, (_, i) => i + 1).map((pageNum) => (
                          <button
                            key={`page-jump-${pageNum}`}
                            type="button"
                            onClick={() => handlePageChange(pageNum)}
                            className={`rounded-lg border px-1.5 py-1.5 text-xs font-medium transition ${
                              pageNum === currentPage
                                ? "border-[var(--color-purple)] bg-[color:color-mix(in_srgb,var(--color-purple)_90%,white)] text-white"
                                : "border-black/10 bg-white text-[var(--color-purple)] hover:border-[var(--color-purple)]"
                            }`}
                            aria-label={`Jump to page ${pageNum}`}
                          >
                            {pageNum}
                          </button>
                        ))}
                      </div>
                    ) : (
                      <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_66%,white)]">
                        Page navigation will appear after the document loads.
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="max-h-[calc(66vh-58px)] overflow-y-auto p-3 lg:max-h-[calc(100vh-21.5rem)]">
                    {isOutlineLoading ? (
                      <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_66%,white)]">
                        Reading PDF chapters and bookmarks...
                      </p>
                    ) : outlineError ? (
                      <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_66%,white)]">
                        Outline could not be read for this file.
                      </p>
                    ) : outlineItems.length === 0 ? (
                      <p className="text-sm text-[color:color-mix(in_srgb,var(--color-charcoal)_66%,white)]">
                        No embedded outline found in this PDF.
                      </p>
                    ) : (
                      <ul className="space-y-1" aria-label="PDF outline list">
                        {outlineItems.map((item) => (
                          <li key={item.id}>
                            <button
                              type="button"
                              onClick={() => handlePageChange(item.page)}
                              className={`w-full rounded-lg border px-3 py-2 text-left text-sm transition ${
                                currentPage === item.page
                                  ? "border-[var(--color-purple)] bg-[color:color-mix(in_srgb,var(--color-purple)_8%,white)] text-[var(--color-purple)]"
                                  : "border-transparent text-[color:color-mix(in_srgb,var(--color-charcoal)_86%,white)] hover:border-black/10 hover:bg-white"
                              }`}
                              style={{ paddingLeft: `${12 + item.level * 14}px` }}
                              aria-label={`Jump to ${item.title} on page ${item.page}`}
                            >
                              <span className="block truncate font-medium">{item.title}</span>
                              <span className="block text-xs text-[color:color-mix(in_srgb,var(--color-charcoal)_58%,white)]">
                                Page {item.page}
                              </span>
                            </button>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </aside>
            </div>
          </div>
        </div>
      </section>
    </ErrorBoundary>
  );
}

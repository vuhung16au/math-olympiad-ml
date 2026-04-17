"use client";

import { useEffect, useMemo, useRef, useState } from "react";
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

export default function PDFViewer({ booklet }: { booklet: Booklet }) {
  const stageRef = useRef<HTMLDivElement | null>(null);
  const [numPages, setNumPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [scale, setScale] = useState(PDF_DEFAULTS.defaultScale);
  const [containerWidth, setContainerWidth] = useState(900);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    trackBookletOpened(booklet.title);
  }, [booklet.title]);

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
    });

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const safePage = useMemo(
    () => validatePageNumber(currentPage, numPages),
    [currentPage, numPages],
  );

  const canGoPrevious = safePage > 1;
  const canGoNext = numPages > 0 && safePage < numPages;

  const handleFitWidth = () => {
    if (!containerWidth) {
      return;
    }

    const fitScale = validateScale(containerWidth / 800);
    setScale(fitScale);
    trackPdfAction(booklet.title, "fit_width");
  };

  const handleFullscreen = async () => {
    if (!stageRef.current) {
      return;
    }

    if (document.fullscreenElement) {
      await document.exitFullscreen();
      trackPdfAction(booklet.title, "exit_fullscreen");
      return;
    }

    await stageRef.current.requestFullscreen();
    trackPdfAction(booklet.title, "enter_fullscreen");
  };

  const handlePrint = () => {
    const printWindow = window.open(booklet.pdfUrl, "_blank", "noopener,noreferrer");
    printWindow?.focus();
    trackPdfAction(booklet.title, "print");
  };

  return (
    <ErrorBoundary>
      <section className="px-4 py-6 sm:px-6 lg:px-8 lg:py-8">
        <div className="mx-auto max-w-[1280px] overflow-hidden rounded-[32px] border border-black/8 bg-white shadow-[0_24px_70px_rgba(60,16,83,0.08)]">
          <PDFControls
            bookletTitle={booklet.title}
            pdfUrl={booklet.pdfUrl}
            currentPage={safePage}
            totalPages={numPages}
            scale={scale}
            canGoPrevious={canGoPrevious}
            canGoNext={canGoNext}
            onPageChange={(page) => {
              const nextPage = validatePageNumber(page, numPages);
              setCurrentPage(nextPage);
              trackPdfNavigation(booklet.title, nextPage, numPages);
            }}
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
            onFullscreen={handleFullscreen}
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
            <div className="mx-auto flex max-w-full justify-center overflow-auto">
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
                <Page
                  pageNumber={safePage}
                  scale={scale}
                  width={Math.min(containerWidth, 1080)}
                  loading={<LoadingSpinner label="Rendering page" />}
                  renderTextLayer
                  renderAnnotationLayer
                  className="overflow-hidden rounded-[20px] shadow-[0_24px_60px_rgba(0,0,0,0.12)]"
                />
              </Document>
            </div>
          </div>
        </div>
      </section>
    </ErrorBoundary>
  );
}

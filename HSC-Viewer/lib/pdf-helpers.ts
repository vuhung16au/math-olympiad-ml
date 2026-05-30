export async function fetchPdf(url: string): Promise<ArrayBuffer> {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.arrayBuffer();
  } catch (error) {
    throw new Error(`Failed to fetch PDF: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export interface PDFState {
  numPages: number | null;
  currentPage: number;
  scale: number;
  isLoading: boolean;
  error: string | null;
}

export const DEFAULT_PDF_STATE: PDFState = {
  numPages: null,
  currentPage: 1,
  scale: 1.5,
  isLoading: true,
  error: null,
};

export function validatePageNumber(page: number, totalPages: number | null): number {
  if (!totalPages) return 1;
  if (page < 1) return 1;
  if (page > totalPages) return totalPages;
  return Math.floor(page);
}

export function validateScale(scale: number, min: number = 0.5, max: number = 3): number {
  if (scale < min) return min;
  if (scale > max) return max;
  return Math.round(scale * 100) / 100;
}

/** A4 aspect ratio used to reserve scroll space for not-yet-rendered PDF pages. */
export const PDF_PAGE_ASPECT_RATIO = 1.414;

/** Pages mounted above/below the viewport in continuous scroll mode. */
export const CONTINUOUS_RENDER_BUFFER = 2;

export function expandPageWindow(
  center: number,
  totalPages: number,
  buffer: number = CONTINUOUS_RENDER_BUFFER,
): Set<number> {
  const pages = new Set<number>();
  const start = Math.max(1, center - buffer);
  const end = Math.min(totalPages, center + buffer);

  for (let page = start; page <= end; page += 1) {
    pages.add(page);
  }

  return pages;
}

export function isMobilePdfViewport(): boolean {
  if (typeof window === "undefined") {
    return false;
  }

  return window.matchMedia("(max-width: 1023px)").matches;
}

export function fitWidthScale(containerWidth: number, referenceWidth = 800): number {
  return validateScale(containerWidth / referenceWidth);
}

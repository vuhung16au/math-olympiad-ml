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

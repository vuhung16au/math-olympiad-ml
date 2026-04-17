import { track } from "@vercel/analytics";

export function trackBookletOpened(bookletTitle: string) {
  track("booklet_opened", {
    booklet: bookletTitle,
  });
}

export function trackPdfNavigation(bookletTitle: string, page: number, totalPages: number) {
  track("pdf_page_navigation", {
    booklet: bookletTitle,
    page,
    totalPages,
  });
}

export function trackPdfZoom(bookletTitle: string, zoomPercent: number) {
  track("pdf_zoom", {
    booklet: bookletTitle,
    zoomPercent,
  });
}

export function trackPdfAction(bookletTitle: string, action: string) {
  track("pdf_action", {
    booklet: bookletTitle,
    action,
  });
}

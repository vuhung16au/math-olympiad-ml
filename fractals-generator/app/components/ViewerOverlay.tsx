'use client';

type Props = {
  isRendering: boolean;
  onDownloadPng: () => void;
  onDownloadTikz: () => void;
  onDownloadTex: () => void;
  onFullscreenToggle: () => void;
  isFullscreen: boolean;
};

export function ViewerOverlay({
  isRendering,
  onDownloadPng,
  onDownloadTikz,
  onDownloadTex,
  onFullscreenToggle,
  isFullscreen,
}: Props) {
  return (
    <div className="viewer-overlay" aria-hidden={!isRendering}>
      {isRendering ? (
        <div className="viewer-overlay__loading" role="status" aria-label="Rendering">
          <div className="spinner" aria-hidden="true" />
          <div className="viewer-overlay__label">Rendering…</div>
        </div>
      ) : null}

      <div className="viewer-overlay__actions" aria-label="Viewer actions">
        <button type="button" className="overlay-button" onClick={onDownloadPng} aria-label="Download PNG" title="Download PNG">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              fill="currentColor"
              d="M12 3a1 1 0 0 1 1 1v8.6l2.3-2.3a1 1 0 1 1 1.4 1.4l-4 4a1 1 0 0 1-1.4 0l-4-4a1 1 0 1 1 1.4-1.4L11 12.6V4a1 1 0 0 1 1-1zM5 19a1 1 0 0 1 1-1h12a1 1 0 1 1 0 2H6a1 1 0 0 1-1-1z"
            />
          </svg>
        </button>
        <button type="button" className="overlay-button" onClick={onDownloadTikz} aria-label="Download TikZ snippet" title="Download TikZ (.tikz)">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              fill="currentColor"
              d="M4 4h16v2H4V4zm2 4h12v12H6V8zm2 2v8h8v-8H8zm2 2h4v4h-4v-4z"
            />
          </svg>
        </button>
        <button type="button" className="overlay-button" onClick={onDownloadTex} aria-label="Download standalone TeX" title="Download standalone LaTeX (.tex)">
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              fill="currentColor"
              d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6zm4 18H6V4h7v5h5v11zM8 12h8v2H8v-2zm0 4h8v2H8v-2zm0-8h3v2H8v-2z"
            />
          </svg>
        </button>
        <button
          type="button"
          className="overlay-button"
          onClick={onFullscreenToggle}
          aria-label={isFullscreen ? 'Exit fullscreen' : 'Enter fullscreen'}
          title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
        >
          <svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true">
            <path
              fill="currentColor"
              d="M7 3a1 1 0 0 0-1 1v3a1 1 0 1 0 2 0V5h2a1 1 0 1 0 0-2H7zm10 0h-3a1 1 0 1 0 0 2h2v2a1 1 0 1 0 2 0V4a1 1 0 0 0-1-1zM6 17a1 1 0 0 0-2 0v3a1 1 0 0 0 1 1h3a1 1 0 1 0 0-2H6v-2zm14 0a1 1 0 1 0-2 0v2h-2a1 1 0 1 0 0 2h3a1 1 0 0 0 1-1v-3z"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}


'use client';

type Props = {
  isRendering: boolean;
  onDownloadPng: () => void;
  onFullscreenToggle: () => void;
  isFullscreen: boolean;
};

export function ViewerOverlay({ isRendering, onDownloadPng, onFullscreenToggle, isFullscreen }: Props) {
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


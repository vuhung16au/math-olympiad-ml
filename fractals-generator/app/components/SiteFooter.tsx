type Props = {
  versionLabel?: string;
};

export function SiteFooter({ versionLabel = 'v1.0' }: Props) {
  return (
    <footer className="site-footer" aria-label="Site footer">
      <div className="site-footer__inner">
        <div className="site-footer__left">Fractals Generator · {versionLabel}</div>
        <div className="site-footer__right">
          <a
            className="icon-link"
            href="https://github.com/vuhung16au/math-olympiad-ml/tree/main/fractals-generator"
            target="_blank"
            rel="noreferrer"
            aria-label="View source on GitHub"
            title="GitHub"
          >
            <svg viewBox="0 0 24 24" width="18" height="18" role="img" aria-hidden="true">
              <path
                fill="currentColor"
                d="M12 2C6.48 2 2 6.58 2 12.24c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.48 0-.24-.01-.88-.01-1.73-2.78.62-3.37-1.37-3.37-1.37-.45-1.18-1.11-1.49-1.11-1.49-.9-.64.07-.62.07-.62 1 .07 1.52 1.05 1.52 1.05.89 1.56 2.34 1.11 2.91.85.09-.66.35-1.11.63-1.37-2.22-.26-4.56-1.14-4.56-5.09 0-1.12.39-2.03 1.03-2.75-.1-.26-.45-1.31.1-2.74 0 0 .84-.27 2.75 1.05a9.2 9.2 0 0 1 2.5-.35c.85 0 1.71.12 2.5.35 1.9-1.32 2.74-1.05 2.74-1.05.56 1.43.21 2.48.11 2.74.64.72 1.03 1.63 1.03 2.75 0 3.96-2.34 4.82-4.58 5.08.36.32.68.95.68 1.92 0 1.39-.01 2.51-.01 2.85 0 .27.18.59.69.48A10.1 10.1 0 0 0 22 12.24C22 6.58 17.52 2 12 2z"
              />
            </svg>
          </a>
          <span className="site-footer__meta">MIT · Vu Hung Nguyen</span>
        </div>
      </div>
    </footer>
  );
}


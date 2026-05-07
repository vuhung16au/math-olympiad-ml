"use client";

import Script from "next/script";

export default function MathJaxScript() {
  return (
    <>
      <Script id="mathjax-config" strategy="afterInteractive">
        {`
          window.MathJax = {
            tex: {
              inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
              displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
              processEscapes: true,
              packages: {
                '[+]': ['ams', 'newcommand', 'configmacros']
              }
            },
            options: {
              skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            },
            chtml: {
              matchFontHeight: false,
              scale: 1
            }
          };
        `}
      </Script>
      <Script
        id="mathjax-runtime"
        strategy="lazyOnload"
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml-full.js"
      />
    </>
  );
}

import Script from "next/script";
import { GOOGLE_ANALYTICS_MEASUREMENT_ID } from "@/lib/constants";

/**
 * GA4 via gtag.js. Loaded after hydration so it does not block LCP.
 */
export default function GoogleAnalytics() {
  return (
    <>
      <Script
        src={`https://www.googletagmanager.com/gtag/js?id=${GOOGLE_ANALYTICS_MEASUREMENT_ID}`}
        strategy="afterInteractive"
      />
      <Script id="google-analytics" strategy="afterInteractive">
        {`
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${GOOGLE_ANALYTICS_MEASUREMENT_ID}');
        `}
      </Script>
    </>
  );
}

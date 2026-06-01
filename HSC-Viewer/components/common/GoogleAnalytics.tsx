import Script from "next/script";
import { GOOGLE_ANALYTICS_MEASUREMENT_ID } from "@/lib/constants";

const SHOULD_LOAD_GA =
  process.env.NODE_ENV === "production" &&
  process.env.NEXT_PUBLIC_IS_E2E !== "1";

/**
 * GA4 via gtag.js. Loaded after hydration so it does not block LCP.
 */
export default function GoogleAnalytics() {
  if (!SHOULD_LOAD_GA) {
    return null;
  }

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

import type { Metadata } from "next";
import { Analytics } from "@vercel/analytics/react";
import "./globals.css";
import { APP_DESCRIPTION, APP_NAME } from "@/lib/constants";
import { getGeneratedManifest } from "@/lib/generated-content";
import AppShell from "@/components/layout/AppShell";
import MathJaxScript from "@/components/reader/MathJaxScript";

export const metadata: Metadata = {
  title: APP_NAME,
  description: APP_DESCRIPTION,
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const manifest = await getGeneratedManifest();

  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body>
        <MathJaxScript />
        <AppShell booklets={manifest}>{children}</AppShell>
        <Analytics />
      </body>
    </html>
  );
}

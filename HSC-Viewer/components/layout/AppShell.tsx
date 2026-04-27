"use client";

import { useEffect, useMemo, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { PanelLeftOpen } from "lucide-react";
import Header from "@/components/layout/Header";
import ReaderMobileTopBar from "@/components/layout/ReaderMobileTopBar";
import Sidebar from "@/components/layout/Sidebar";
import MobileMenu from "@/components/layout/MobileMenu";
import Footer from "@/components/common/Footer";
import OfflineBanner from "@/components/common/OfflineBanner";
import { getBookletBySlug } from "@/lib/booklets";
import {
  getLastPageForSlug,
  getPref,
  getResumeMode,
  PREF_KEYS,
  setPref,
} from "@/lib/preferences";

function getCurrentTitle(pathname: string): string | null {
  if (!pathname.startsWith("/booklets/")) {
    return null;
  }

  const slug = pathname.replace("/booklets/", "").split("/")[0];
  return getBookletBySlug(slug)?.title ?? null;
}

function resolveResumeTarget(pathname: string): string | null {
  const resumeMode = getResumeMode();
  if (resumeMode === "off") {
    return null;
  }

  if (pathname === "/") {
    const lastUrl = getPref(PREF_KEYS.lastUrl);
    if (lastUrl && lastUrl.startsWith("/booklets/")) {
      return lastUrl;
    }

    const lastSlug = getPref(PREF_KEYS.lastSlug);
    if (!lastSlug) {
      return null;
    }

    const savedPage = getLastPageForSlug(lastSlug);
    return savedPage && savedPage > 1
      ? `/booklets/${lastSlug}/${savedPage}`
      : `/booklets/${lastSlug}`;
  }

  const slugRouteMatch = pathname.match(/^\/booklets\/([^/]+)$/);
  if (!slugRouteMatch) {
    return null;
  }

  const slug = slugRouteMatch[1];
  const savedPage = getLastPageForSlug(slug);

  if (!savedPage || savedPage <= 1) {
    return null;
  }

  return `/booklets/${slug}/${savedPage}`;
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const currentTitle = useMemo(() => getCurrentTitle(pathname), [pathname]);
  const isReaderRoute = pathname.startsWith("/booklets/");

  // Load persisted sidebar preference only after mount to keep SSR and hydration output identical.
  useEffect(() => {
    setIsSidebarCollapsed(getPref(PREF_KEYS.sidebarCollapsed) === "1");
  }, []);

  // Restore last visited route for home and per-booklet landing routes.
  useEffect(() => {
    const target = resolveResumeTarget(pathname);
    if (!target || target === pathname) {
      return;
    }

    const resumeMode = getResumeMode();
    if (resumeMode === "prompt") {
      const shouldResume = window.confirm("Resume where you left off?");
      if (!shouldResume) {
        return;
      }
    }

    router.replace(target);
  }, [pathname, router]);

  const handleToggleSidebar = () => {
    setIsSidebarCollapsed((prev) => {
      const next = !prev;
      setPref(PREF_KEYS.sidebarCollapsed, next ? "1" : "0");
      return next;
    });
  };

  return (
    <div className="min-h-screen bg-[var(--color-ivory)] text-[var(--color-charcoal)]">
      <OfflineBanner />
      {!isReaderRoute ? (
        <Header
          currentTitle={currentTitle}
          onOpenMenu={() => setIsMobileMenuOpen(true)}
        />
      ) : (
        <ReaderMobileTopBar
          bookletTitle={currentTitle}
          onOpenMenu={() => setIsMobileMenuOpen(true)}
        />
      )}
      {isSidebarCollapsed ? (
        <button
          type="button"
          onClick={handleToggleSidebar}
          className={[
            "fixed left-4 z-30 hidden items-center gap-2 rounded-full border border-black/10 bg-white px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] text-[var(--color-purple)] shadow-sm transition hover:border-[var(--color-purple)] lg:inline-flex",
            isReaderRoute ? "top-4" : "top-20",
          ].join(" ")}
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen className="h-4 w-4" />
          Booklets
        </button>
      ) : null}
      <div className={[
        "mx-auto flex w-full max-w-[1600px]",
        isReaderRoute ? "min-h-screen" : "min-h-[calc(100vh-4rem)]",
      ].join(" ")}>
        <Sidebar
          pathname={pathname}
          isCollapsed={isSidebarCollapsed}
          isReaderMode={isReaderRoute}
          onToggleCollapse={handleToggleSidebar}
        />
        <MobileMenu
          isOpen={isMobileMenuOpen}
          pathname={pathname}
          onClose={() => setIsMobileMenuOpen(false)}
        />
        <div className="flex min-w-0 flex-1 flex-col">
          <main className="flex-1">{children}</main>
          <Footer />
        </div>
      </div>
    </div>
  );
}

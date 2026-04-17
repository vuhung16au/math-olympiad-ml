"use client";

import { useEffect, useMemo, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { PanelLeftOpen } from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import MobileMenu from "@/components/layout/MobileMenu";
import Footer from "@/components/common/Footer";
import { getBookletBySlug } from "@/lib/booklets";
import { getPref, setPref, PREF_KEYS } from "@/lib/preferences";

function getCurrentTitle(pathname: string): string | null {
  if (!pathname.startsWith("/booklets/")) {
    return null;
  }

  const slug = pathname.replace("/booklets/", "").split("/")[0];
  return getBookletBySlug(slug)?.title ?? null;
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

  // Redirect to last visited booklet when landing on the home page
  useEffect(() => {
    if (pathname !== "/") return;
    const lastUrl = getPref(PREF_KEYS.lastUrl);
    if (lastUrl && lastUrl.startsWith("/booklets/")) {
      router.replace(lastUrl);
    }
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
      {!isReaderRoute ? (
        <Header
          currentTitle={currentTitle}
          onOpenMenu={() => setIsMobileMenuOpen(true)}
        />
      ) : null}
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

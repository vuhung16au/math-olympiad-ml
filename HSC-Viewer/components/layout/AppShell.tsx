"use client";

import { useMemo, useState } from "react";
import { usePathname } from "next/navigation";
import { PanelLeftOpen } from "lucide-react";
import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";
import MobileMenu from "@/components/layout/MobileMenu";
import Footer from "@/components/common/Footer";
import { getBookletBySlug } from "@/lib/booklets";

function getCurrentTitle(pathname: string): string | null {
  if (!pathname.startsWith("/booklets/")) {
    return null;
  }

  const slug = pathname.replace("/booklets/", "").split("/")[0];
  return getBookletBySlug(slug)?.title ?? null;
}

export default function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const currentTitle = useMemo(() => getCurrentTitle(pathname), [pathname]);
  const isReaderRoute = pathname.startsWith("/booklets/");

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
          onClick={() => setIsSidebarCollapsed(false)}
          className={[
            "fixed left-4 z-30 hidden items-center gap-2 rounded-full border border-black/10 bg-white px-3 py-2 text-xs font-semibold uppercase tracking-[0.14em] text-[var(--color-purple)] shadow-sm transition hover:border-[var(--color-purple)] lg:inline-flex",
            isReaderRoute ? "top-4" : "top-20",
          ].join(" ")}
          aria-label="Expand sidebar"
        >
          <PanelLeftOpen className="h-4 w-4" />
          Menu
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
          onToggleCollapse={() => setIsSidebarCollapsed((value) => !value)}
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

"use client";

import { useMemo, useState } from "react";
import { usePathname } from "next/navigation";
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
  const currentTitle = useMemo(() => getCurrentTitle(pathname), [pathname]);

  return (
    <div className="min-h-screen bg-[var(--color-ivory)] text-[var(--color-charcoal)]">
      <Header
        currentTitle={currentTitle}
        onOpenMenu={() => setIsMobileMenuOpen(true)}
      />
      <div className="mx-auto flex min-h-[calc(100vh-4rem)] w-full max-w-[1600px]">
        <Sidebar pathname={pathname} />
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

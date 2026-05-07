"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { getVisibleBooklets, type BookletManifestEntry } from "@/lib/booklets";
import Footer from "@/components/common/Footer";
import Header from "@/components/layout/Header";
import MobileMenu from "@/components/layout/MobileMenu";
import Sidebar from "@/components/layout/Sidebar";

export default function AppShell({
  children,
  booklets,
}: {
  children: React.ReactNode;
  booklets: BookletManifestEntry[];
}) {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);
  const visibleBooklets = getVisibleBooklets(booklets);

  return (
    <div className="min-h-screen text-[var(--color-charcoal)]">
      <Header title="Online booklet reader" onOpenMenu={() => setIsOpen(true)} />
      <div className="mx-auto flex max-w-[1600px]">
        <Sidebar pathname={pathname} booklets={visibleBooklets} />
        <MobileMenu
          isOpen={isOpen}
          pathname={pathname}
          booklets={visibleBooklets}
          onClose={() => setIsOpen(false)}
        />
        <div className="flex min-w-0 flex-1 flex-col">
          <main className="flex-1">{children}</main>
          <Footer />
        </div>
      </div>
    </div>
  );
}

'use client';

import type { ReactNode } from 'react';

type Props = {
  title: string;
  breadcrumbs?: string;
  rightSlot?: ReactNode;
};

export function AppHeader({ title, breadcrumbs, rightSlot }: Props) {
  return (
    <header className="app-header" aria-label="App header">
      <div className="app-header__inner">
        <div className="app-header__left">
          <div className="app-header__title">{title}</div>
          {breadcrumbs ? <div className="app-header__crumbs">{breadcrumbs}</div> : null}
        </div>
        <div className="app-header__right">{rightSlot}</div>
      </div>
    </header>
  );
}


// src/components/layout/Layout.tsx
import React from 'react';
import Sidebar from './SideBar';
import Header from './Header';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): React.JSX.Element {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 transition-colors duration-300">
      <Sidebar />
      <main className="ml-44 p-4"> {/* ← Agora inclui o Header */}
        <Header />
        {children}
      </main>
    </div>
  );
}


// src/components/layout/Layout.tsx
import React from 'react';
import { useAppContext } from '../../context/AppContext';
import { Sidebar } from '../layout';
import { Header } from '../layout';

interface LayoutProps {
  children: React.ReactNode;
}
// src/components/layout/Layout.tsx 
 export default function Layout({ children }: LayoutProps) {
  const { isDarkMode } = useAppContext();
  
  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark' : ''}`}>
      <div className="min-h-screen bg-light dark:bg-dark text-black dark:text-white transition-colors duration-300">
        <Sidebar />
        <Header />
        <main className="ml-0 md:ml-56 p-4">
          {children}
        </main>
      </div>
    </div>
  );
}
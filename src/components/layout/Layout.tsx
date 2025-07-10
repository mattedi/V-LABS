import React from 'react';
import UnifiedLayout from './UnifiedLayout';

interface LayoutProps {
  children: React.ReactNode;
  pageTitle?: string;
  showTopBar?: boolean;
}

export default function Layout({ 
  children, 
  pageTitle = "Documentos",
  showTopBar = true 
}: LayoutProps) {
  return (
    <UnifiedLayout 
      pageTitle={pageTitle}
      showTopBar={showTopBar}
    >
      {children}
    </UnifiedLayout>
  );
}
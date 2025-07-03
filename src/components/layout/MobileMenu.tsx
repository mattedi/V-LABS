
import { FiMenu, FiX } from 'react-icons/fi';
import React, { useState, ReactNode } from 'react';


interface MobileMenuProps {
  children: ReactNode;
}

export default function MobileMenu({ children }: MobileMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="md:hidden">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="fixed top-4 left-4 z-50 p-2 rounded-full bg-primary text-white"
      >
        {isOpen ? <FiX size={24} /> : <FiMenu size={24} />}
      </button>

      <div 
        className={`fixed inset-0 bg-dark z-40 transform ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } transition-transform duration-300 ease-in-out`}
      >
        <div className="pt-16 px-4">
          {children}
        </div>
      </div>
    </div>
  );
}
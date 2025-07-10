// src/pages/IconTest.tsx
import React from 'react';
import { FiFileText } from 'react-icons/fi';

export default function IconTest() {
  return (
    <div className="text-4xl text-blue-600 flex items-center gap-2 p-10">
      <FiFileText />
      Documento
    </div>
  );
}

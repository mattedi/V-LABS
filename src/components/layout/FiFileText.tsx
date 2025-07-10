// src/components/icons/FileIcon.tsx
import React from 'react';

export const FileIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 32,
  color = 'currentColor',
}) => (
  <svg
    width={size}
    height={size}
    fill="none"
    viewBox="0 0 24 24"
    stroke={color}
    strokeWidth={2}
    xmlns="http://www.w3.org/2000/svg"
  >
    <path
      strokeLinecap="round"
      strokeLinejoin="round"
      d="M7 2h8l5 5v13a2 2 0 01-2 2H7a2 2 0 01-2-2V4a2 2 0 012-2z"
    />
    <path strokeLinecap="round" strokeLinejoin="round" d="M14 2v6h6" />
  </svg>
);

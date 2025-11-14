import React from 'react';
import { Link } from 'react-router-dom';

export default function Logo({ size = 'md', showText = true }) {
  const heights = {
    sm: 'h-8',
    md: 'h-10',
    lg: 'h-12'
  };

  return (
    <Link 
      to="/" 
      aria-label="CyberSathi — Cybercrime Helpline 1930" 
      className="flex items-center gap-3 hover:opacity-80 transition-opacity"
    >
      <img
        src="/assets/logo.png"
        alt="CyberSathi Logo"
        className={`${heights[size]} w-auto drop-shadow-md`}
        loading="lazy"
        decoding="async"
      />
      {showText && (
        <span className="hidden md:inline font-semibold text-xl text-gray-800">
          CyberSathi
        </span>
      )}
    </Link>
  );
}

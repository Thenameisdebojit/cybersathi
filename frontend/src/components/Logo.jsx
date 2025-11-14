import React from 'react';
import { Link } from 'react-router-dom';
import { ShieldLogo } from './ShieldLogo';

export default function Logo({ size = 'md', showText = true }) {
  const heights = {
    sm: 'h-8',
    md: 'h-10',
    lg: 'h-12',
    large: 'h-14'
  };

  return (
    <Link 
      to="/" 
      aria-label="CyberSathi — Cybercrime Helpline 1930" 
      className="flex items-center gap-3 hover:opacity-80 transition-opacity"
    >
      <ShieldLogo className={`${heights[size]} w-auto`} />
      {showText && (
        <span className="hidden md:inline font-semibold text-xl text-white">
          CyberSathi
        </span>
      )}
    </Link>
  );
}

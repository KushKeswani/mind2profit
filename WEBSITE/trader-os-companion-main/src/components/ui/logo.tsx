import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

export const Logo: React.FC<LogoProps> = ({ 
  className = '', 
  size = 'md', 
  showText = true 
}) => {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-20 h-20',
    lg: 'w-24 h-24'
  };

  const textSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base'
  };

  return (
    <div className={`flex flex-col items-center ${className}`}>
      {/* Brain Icon */}
      <svg 
        className={`${sizeClasses[size]} text-primary mb-1`}
        viewBox="0 0 24 24" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Brain outline */}
        <path 
          d="M12 2C8.5 2 6 4.5 6 8c0 2 1 3.5 2 4.5C6.5 13.5 5 15.5 5 18c0 1.5 0.5 2.5 1.5 3.5C7.5 22.5 9 23 12 23s4.5-0.5 5.5-1.5C18.5 20.5 19 19.5 19 18c0-2.5-1.5-4.5-3-5.5C17 11.5 18 10 18 8c0-3.5-2.5-6-6-6z" 
          stroke="currentColor" 
          strokeWidth="1.5" 
          fill="none"
        />
        {/* Brain hemispheres division */}
        <path 
          d="M12 2v21" 
          stroke="currentColor" 
          strokeWidth="1" 
          opacity="0.6"
        />
        {/* Left hemisphere details */}
        <path 
          d="M8 6c0.5 1 1.5 2 3 2.5" 
          stroke="currentColor" 
          strokeWidth="1" 
          opacity="0.8"
        />
        <path 
          d="M7 9c0.5 0.5 1.5 1 2.5 1.5" 
          stroke="currentColor" 
          strokeWidth="1" 
          opacity="0.6"
        />
        {/* Right hemisphere details */}
        <path 
          d="M16 6c-0.5 1-1.5 2-3 2.5" 
          stroke="currentColor" 
          strokeWidth="1" 
          opacity="0.8"
        />
        <path 
          d="M17 9c-0.5 0.5-1.5 1-2.5 1.5" 
          stroke="currentColor" 
          strokeWidth="1" 
          opacity="0.6"
        />
      </svg>
      
      {/* Text */}
      {showText && (
        <span className={`font-semibold text-primary ${textSizes[size]}`}>
          Mind2Profit
        </span>
      )}
    </div>
  );
}; 
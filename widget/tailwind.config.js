/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand gradient colors - Updated to match your designs
        'brand-red': '#FF1F38',
        'brand-purple': '#8629FF',
        'brand-secondary': '#C5BAFF',
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(135deg, #8629FF 0%, #FF1F38 100%)',
        'gradient-brand-horizontal': 'linear-gradient(90deg, #8629FF 0%, #FF1F38 100%)',
        'gradient-brand-reverse': 'linear-gradient(135deg, #FF1F38 0%, #8629FF 100%)',
      },
      boxShadow: {
        'brand': '0 4px 12px rgba(134, 41, 255, 0.25)',
        'brand-lg': '0 10px 40px rgba(134, 41, 255, 0.35)',
      },
      animation: {
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'pulse-ring': 'pulseRing 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        slideUp: {
          'from': {
            opacity: '0',
            transform: 'translateY(20px)',
          },
          'to': {
            opacity: '1',
            transform: 'translateY(0)',
          },
        },
        slideInRight: {
          'from': {
            opacity: '0',
            transform: 'translateX(100px)',
          },
          'to': {
            opacity: '1',
            transform: 'translateX(0)',
          },
        },
        pulseRing: {
          '0%, 100%': {
            transform: 'scale(1)',
            opacity: '1',
          },
          '50%': {
            transform: 'scale(1.1)',
            opacity: '0.5',
          },
        },
      },
    },
  },
  plugins: [],
}
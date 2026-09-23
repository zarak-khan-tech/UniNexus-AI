/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Fraunces', 'Georgia', 'serif'],
      },
      colors: {
        ink: {
          50: '#f5f7fa', 100: '#e4eaf2', 200: '#c9d5e5', 300: '#9eb1c9',
          400: '#6b85a6', 500: '#4a6483', 600: '#365070', 700: '#2a3f59',
          800: '#1f2f44', 900: '#161f2e', 950: '#0b1220',
        },
        gold: {
          50: '#fefbea', 100: '#fcf3c4', 200: '#f9e68a', 300: '#f5d14b',
          400: '#eeb91f', 500: '#d19e0b', 600: '#a87a09', 700: '#7d5a0c',
        },
      },
      boxShadow: {
        // English: Realistic layered shadows — multiple transparent layers create true depth.
        // Roman Urdu: Layered shadow — multiple transparent layers se asli gehraai aati hai.
        'card': '0 0 0 1px rgba(15,23,42,0.03), 0 1px 1px rgba(15,23,42,0.02), 0 4px 8px rgba(15,23,42,0.04), 0 12px 24px rgba(15,23,42,0.05)',
        'card-hover': '0 0 0 1px rgba(15,23,42,0.05), 0 2px 4px rgba(15,23,42,0.04), 0 12px 20px rgba(15,23,42,0.08), 0 24px 48px rgba(15,23,42,0.10)',
        'float': '0 8px 16px rgba(15,23,42,0.08), 0 24px 48px rgba(15,23,42,0.12)',
        'inset-soft': 'inset 0 1px 2px rgba(15,23,42,0.04)',
        'nav-active': '0 2px 4px rgba(11,18,32,0.20), 0 8px 16px rgba(11,18,32,0.15)',
      },
      animation: {
        'slide-up': 'slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1)',
        'fade-in': 'fadeIn 0.4s ease-out',
      },
      keyframes: {
        slideUp: {
          '0%': { opacity: 0, transform: 'translateY(8px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        fadeIn: {
          '0%': { opacity: 0 },
          '100%': { opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}

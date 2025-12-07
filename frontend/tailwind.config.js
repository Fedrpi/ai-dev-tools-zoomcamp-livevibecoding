/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tech-green': '#00ff41',
        'tech-orange': '#ff6b35',
        'tech-cyan': '#00d9ff',
        'tech-yellow': '#ffdd00',
        'dark-base': '#0a0e27',
        'dark-elevated': '#151933',
        'dark-border': '#1e2542',
        'light-base': '#f5f5f0',
        'light-elevated': '#ffffff',
        'light-border': '#d4d4c8',
      },
      fontFamily: {
        'display': ['Space Mono', 'monospace'],
        'code': ['JetBrains Mono', 'monospace'],
        'body': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'slide-in': 'slide-in 0.5s ease-out',
        'fade-in-up': 'fade-in-up 0.6s ease-out',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.5' },
        },
        'slide-in': {
          'from': { transform: 'translateX(-100%)', opacity: '0' },
          'to': { transform: 'translateX(0)', opacity: '1' },
        },
        'fade-in-up': {
          'from': { transform: 'translateY(20px)', opacity: '0' },
          'to': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

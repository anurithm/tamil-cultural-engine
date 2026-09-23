/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        heritage: {
          50: '#fff9f0',
          100: '#fdf1dc',
          200: '#fbe2b8',
          300: '#f7ce89',
          400: '#f2b353',
          500: '#ea9729',
          600: '#ce771c',
          700: '#a65818',
          800: '#86461b',
          900: '#6f3b19',
        },
        cultural: {
          maroon: '#6B1D2F',
          gold: '#C59B27',
          copper: '#B85D19',
          indigo: '#1F3A52',
          forest: '#1E4338',
          sand: '#F7F4EE',
          slate: '#2B3542'
        }
      },
      fontFamily: {
        tamil: ['"Noto Sans Tamil"', '"Mukta Malar"', 'system-ui', 'sans-serif'],
        serif: ['"Cinzel"', 'Georgia', 'serif']
      },
      fontSize: {
        '2xs': ['0.65rem', { lineHeight: '1rem' }],
        '3xs': ['0.55rem', { lineHeight: '0.875rem' }],
      }
    },
  },
  plugins: [],
}

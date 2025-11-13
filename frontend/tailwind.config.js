export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#E8F8F5',
          100: '#D4F1EB',
          200: '#A8E6CF',
          300: '#7DD9B3',
          400: '#51CC97',
          500: '#2ECC71',
          600: '#27AE60',
          700: '#229954',
          800: '#1E7E48',
          900: '#145A32',
        },
        success: {
          50: '#E8FCF7',
          100: '#D1F9EF',
          200: '#A3F3E0',
          300: '#75EDD0',
          400: '#47E7C1',
          500: '#06D6A0',
          600: '#05B589',
          700: '#049472',
          800: '#03735B',
          900: '#025244',
        },
        dark: {
          50: '#E5EBE9',
          100: '#CCD7D3',
          200: '#99AEA6',
          300: '#66867A',
          400: '#335D4D',
          500: '#0D3B2C',
          600: '#0B3224',
          700: '#09291C',
          800: '#071F15',
          900: '#05160D',
        },
      },
      fontFamily: {
        sans: ['Inter', 'SF Pro Display', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 2px 8px 0 rgba(99, 99, 99, 0.08)',
        'medium': '0 4px 16px 0 rgba(99, 99, 99, 0.12)',
        'large': '0 8px 32px 0 rgba(99, 99, 99, 0.16)',
        'glass': '0 8px 32px 0 rgba(31, 38, 135, 0.1)',
      },
      backdropBlur: {
        'glass': '12px',
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in',
        'slide-up': 'slideUp 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

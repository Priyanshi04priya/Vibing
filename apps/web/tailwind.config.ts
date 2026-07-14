import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        midnight: '#050816',
        aurora: '#7c3aed',
        coral: '#ff6b6b',
        mint: '#34d399',
      },
    },
  },
  plugins: [],
} satisfies Config;

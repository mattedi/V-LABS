import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import autoprefixer from 'autoprefixer';

// Importe o plugin corretamente
import tailwindcssPlugin from '@tailwindcss/postcss';

export default defineConfig({
  plugins: [react()],
  css: {
    postcss: {
      plugins: [
        tailwindcssPlugin(),  // Note o uso dos parênteses para invocar a função
        autoprefixer
      ],
    },
  },
});
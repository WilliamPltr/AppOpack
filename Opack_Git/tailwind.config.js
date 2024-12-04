module.exports = {
  content: [
    './templates/**/*.html', // Tous les templates HTML
    './core/templates/**/*.html', // Sous-dossiers dans core
    './static/css/**/*.css', // Fichiers CSS dans static/css
    './static/**/*.js', // Fichiers JS dans static
  ],
  theme: {
    extend: {
      borderRadius: {
        '1.5xl': '1.125rem', // Entre "xl" (1rem) et "2xl" (1.5rem)
      },
    },
  },
  daisyui: {
    themes: [
      {
        opack: {
          primary: '#2c3b2f', // Vert foncé
          secondary: '#ebc151', // Jaune
          accent: '#fffefb', // Blanc cassé
          neutral: '#3d4451', // Couleur neutre supplémentaire
          'base-100': '#fffefb', // Fond blanc cassé
          info: '#3abff8',
          success: '#36d399',
          warning: '#fbbd23',
          error: '#f87272',
        },
      },
    ],
  },
  plugins: [require('daisyui')],
};

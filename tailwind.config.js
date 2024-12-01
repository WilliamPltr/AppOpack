module.exports = {
  content: [
    './templates/**/*.html',   // Tous les fichiers HTML dans le dossier templates
    './core/templates/**/*.html', // Si tes templates Django sont dans un sous-dossier
    './static/**/*.js',        // Tous les fichiers JavaScript dans le dossier static
    './static/**/*.css', // Ajout pour CSS
  ],
  theme: {
    extend: {},
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

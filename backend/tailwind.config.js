// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx,css}',
    './pages/**/*.html',
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
    './node_modules/flowbite/**/*.js',
    '**/src/**/*.{html,js,css}', // node modules being included here
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};

// tailwind.config.js
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx,css,scss}',
    './pages/**/*.html',
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
    './node_modules/flowbite/**/*.js',
    '**/src/**/*.{html,js,css,scss}', // node modules being included here
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};

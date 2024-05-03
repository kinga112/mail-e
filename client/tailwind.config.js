/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      borderRadius: {
        '4xl': '3rem',
      },
      left:{
        '18': '4.5rem',
      },
      width: {
        '200': 'calc(100% - 125px)',
        '210': 'calc(100% - 65px)',
       }
    },
  },
  plugins: [],
}


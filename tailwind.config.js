/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.{html,js,css}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "var(--color-blue-500)",
          hover: "var(--color-blue-600)",
          on: "var(--color-white)",
        },
        surface: {
          DEFAULT: "var(--color-slate-50)",
          container: "var(--color-slate-100)",
          "container-high": "var(--color-slate-200)",
          inverse: "var(--color-slate-900)",
        },
      },
    },
  },
  plugins: [],
}


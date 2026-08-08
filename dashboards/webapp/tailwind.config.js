/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: "#0B132B",
          800: "#1C2541",
          700: "#3A506B"
        },
        gold: {
          500: "#D4AF37",
          400: "#F4C430"
        }
      }
    }
  },
  plugins: []
};

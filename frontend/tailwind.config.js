/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html","./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
  // 关闭 preflight，避免覆盖 Element Plus 基础样式
  corePlugins: { preflight: false }
}

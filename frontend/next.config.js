/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // This is for static export, remove if you want SSR
  trailingSlash: true,
  reactStrictMode: true,
  swcMinify: true,
};

module.exports = nextConfig;
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Job apply links / employer logos come from many hosts; allow remote images.
  images: { remotePatterns: [{ protocol: "https", hostname: "**" }] },
};

export default nextConfig;

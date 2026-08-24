import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  /* config options here */
  typescript: {
    ignoreBuildErrors: true,
  },
  reactStrictMode: false,
  // Low-bandwidth optimization: compress all responses
  compress: true,
  // Power optimizations for mobile users in emerging markets
  poweredByHeader: false,
};

export default nextConfig;

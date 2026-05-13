/** @type {import('next').NextConfig} */
const isGithubPages = process.env.GITHUB_ACTIONS === 'true';
const repoName = 'AgentGraph';

const nextConfig = {
  reactStrictMode: true,
  compress: true,

  async rewrites() {
    if (isGithubPages) {
      return [];
    }
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.BACKEND_URL ?? 'http://localhost:8000'}/:path*`,
      },
    ];
  },

  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          { key: 'X-Frame-Options', value: 'DENY' },
          { key: 'X-Content-Type-Options', value: 'nosniff' },
          { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
          { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
        ],
      },
    ];
  },

  images: {
    unoptimized: true,
  },

  generateEtags: true,
  poweredByHeader: false,

  experimental: {
    optimizePackageImports: ['react', 'react-dom'],
  },

  output: isGithubPages ? 'export' : (process.env.NODE_ENV === 'production' ? 'standalone' : undefined),
  trailingSlash: isGithubPages,
  basePath: isGithubPages ? `/${repoName}` : '',
  assetPrefix: isGithubPages ? `/${repoName}/` : undefined,
};

module.exports = nextConfig;

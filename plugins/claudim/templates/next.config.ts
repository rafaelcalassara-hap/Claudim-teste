import type { NextConfig } from "next";

const config: NextConfig = {
  // Erro de tipo derruba o build de propósito: é a única verificação
  // automática que este projeto tem.
  typescript: { ignoreBuildErrors: false },
  eslint: { ignoreDuringBuilds: false },
};

export default config;

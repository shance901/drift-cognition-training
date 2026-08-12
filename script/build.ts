import { build as viteBuild } from "vite";
import * as esbuild from "esbuild";
import path from "path";

async function main() {
  const root = path.resolve(import.meta.dirname, "..");

  await viteBuild({ configFile: path.resolve(root, "vite.config.ts") });

  await esbuild.build({
    entryPoints: [path.resolve(root, "server", "index.ts")],
    bundle: true,
    platform: "node",
    format: "esm",
    target: "node20",
    outfile: path.resolve(root, "dist", "index.mjs"),
    packages: "external",
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});

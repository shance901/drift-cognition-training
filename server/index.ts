import express, { type Request, type Response, type NextFunction } from "express";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
  const start = Date.now();
  const requestPath = req.path;
  let capturedJsonResponse: unknown;

  const originalResJson = res.json.bind(res);
  res.json = (body, ...args) => {
    capturedJsonResponse = body;
    return originalResJson(body, ...args);
  };

  res.on("finish", () => {
    if (!requestPath.startsWith("/api")) return;
    const duration = Date.now() - start;
    let line = `${req.method} ${requestPath} ${res.statusCode} in ${duration}ms`;
    if (capturedJsonResponse !== undefined) {
      line += ` :: ${JSON.stringify(capturedJsonResponse)}`;
    }
    log(line.length > 120 ? line.slice(0, 119) + "…" : line);
  });

  next();
});

(async () => {
  const server = await registerRoutes(app);

  app.use((err: Error & { status?: number; statusCode?: number }, _req: Request, res: Response, _next: NextFunction) => {
    const status = err.status ?? err.statusCode ?? 500;
    res.status(status).json({ message: err.message || "Internal Server Error" });
  });

  if (process.env.NODE_ENV !== "production") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  const port = Number(process.env.PORT) || 5000;
  server.listen(port, "0.0.0.0", () => {
    log(`serving on port ${port}`);
  });
})();

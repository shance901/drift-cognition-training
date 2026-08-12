import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { insertWaitlistSignupSchema } from "@shared/schema";

export async function registerRoutes(app: Express): Promise<Server> {
  app.post("/api/waitlist", async (req, res) => {
    const parsed = insertWaitlistSignupSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ message: parsed.error.issues[0]?.message ?? "Invalid submission" });
    }

    const existing = await storage.getWaitlistSignupByEmail(parsed.data.email);
    if (existing) {
      return res.status(409).json({ message: "You're already on the list — we'll be in touch soon." });
    }

    const signup = await storage.createWaitlistSignup(parsed.data);
    res.status(201).json({ id: signup.id, name: signup.name });
  });

  app.get("/api/waitlist/count", async (_req, res) => {
    const count = await storage.getWaitlistCount();
    res.json({ count });
  });

  const httpServer = createServer(app);
  return httpServer;
}

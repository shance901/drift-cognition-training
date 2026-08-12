import { pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const waitlistSignups = pgTable("waitlist_signups", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull(),
  email: text("email").notNull().unique(),
  persona: text("persona").notNull(),
  why: text("why"),
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const insertWaitlistSignupSchema = createInsertSchema(waitlistSignups)
  .pick({ name: true, email: true, persona: true, why: true })
  .extend({
    name: z.string().trim().min(1, "Tell us your name").max(120),
    email: z.string().trim().email("That email doesn't look right"),
    persona: z.enum([
      "high-schooler",
      "career-changer",
      "later-in-life",
      "small-business",
      "curious",
    ]),
    why: z.string().trim().max(500).optional().or(z.literal("")),
  });

export type InsertWaitlistSignup = z.infer<typeof insertWaitlistSignupSchema>;
export type WaitlistSignup = typeof waitlistSignups.$inferSelect;

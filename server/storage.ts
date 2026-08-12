import { randomUUID } from "crypto";
import type { InsertWaitlistSignup, WaitlistSignup } from "@shared/schema";

export interface IStorage {
  createWaitlistSignup(signup: InsertWaitlistSignup): Promise<WaitlistSignup>;
  getWaitlistCount(): Promise<number>;
  getWaitlistSignupByEmail(email: string): Promise<WaitlistSignup | undefined>;
}

export class MemStorage implements IStorage {
  private signups = new Map<string, WaitlistSignup>();

  async createWaitlistSignup(signup: InsertWaitlistSignup): Promise<WaitlistSignup> {
    const record: WaitlistSignup = {
      id: randomUUID(),
      name: signup.name,
      email: signup.email,
      persona: signup.persona,
      why: signup.why || null,
      createdAt: new Date(),
    };
    this.signups.set(record.email.toLowerCase(), record);
    return record;
  }

  async getWaitlistCount(): Promise<number> {
    return this.signups.size;
  }

  async getWaitlistSignupByEmail(email: string): Promise<WaitlistSignup | undefined> {
    return this.signups.get(email.toLowerCase());
  }
}

export const storage = new MemStorage();

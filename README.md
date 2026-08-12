# why·AI — Discover Your Why, Design Your AI

A human-centered framework that uses storytelling to uncover your strengths, assess your AI readiness, and design personalized AI copilots — delivered in two-minute micro-lessons instead of another course nobody finishes.

Built for high schoolers, career changers, later-in-life learners, and small business owners who can't afford to fall behind on AI or the cybersecurity habits that come with it.

## Stack

- **Client:** React 19, Vite, Tailwind CSS v4, Radix UI primitives
- **Server:** Express, TypeScript
- **Data:** Drizzle ORM (PostgreSQL), in-memory storage by default for local dev

## Getting started

```bash
npm install
npm run dev       # starts the Express server + Vite dev middleware on :5000
```

## Scripts

- `npm run dev` — development server with hot reload
- `npm run build` — builds the client (Vite) and server (esbuild) into `dist/`
- `npm start` — runs the production build
- `npm run check` — TypeScript type-checking
- `npm run db:push` — push the Drizzle schema to `DATABASE_URL`

## Structure

- `client/` — React app (landing page: framework, personas, interactive micro-lesson demo, security, waitlist)
- `server/` — Express API (`/api/waitlist`)
- `shared/` — Drizzle schema + Zod validation shared between client and server

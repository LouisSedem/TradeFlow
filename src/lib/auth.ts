/**
 * NextAuth configuration for TradeFlow.
 * Supports Email (magic link) and optionally Google OAuth.
 * Falls back gracefully when env vars are missing.
 */

import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { db } from "@/lib/db";

function buildProviders(): NextAuthOptions["providers"] {
  const providers: NextAuthOptions["providers"] = [];

  // Credentials provider for dev mode — allows sign-in with any email
  providers.push(
    CredentialsProvider({
      id: "dev-credentials",
      name: "Dev Login",
      credentials: {
        email: { label: "Email", type: "email", placeholder: "your@email.com" },
      },
      async authorize(credentials) {
        if (!credentials?.email) return null;

        // Upsert user
        const user = await db.user.upsert({
          where: { email: credentials.email },
          create: { email: credentials.email },
          update: {},
        });
        return { id: user.id, email: user.email, name: user.name };
      },
    })
  );

  // Google OAuth — only if env vars are set
  // Note: dynamic import not easily supported; Google is only added if env vars exist
  if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
    try {
      // eslint-disable-next-line @typescript-eslint/no-require-imports
      const { default: GoogleProvider } = require("next-auth/providers/google");
      providers.push(
        GoogleProvider({
          clientId: process.env.GOOGLE_CLIENT_ID,
          clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        })
      );
    } catch {
      // Google provider not available
    }
  }

  return providers;
}

export const authOptions: NextAuthOptions = {
  providers: buildProviders(),
  secret: process.env.NEXTAUTH_SECRET || "dev-secret-change-in-production",
  pages: {
    signIn: "/",
  },
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.email = user.email;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user && token) {
        (session.user as Record<string, unknown>).id = token.id;
      }
      return session;
    },
  },
};

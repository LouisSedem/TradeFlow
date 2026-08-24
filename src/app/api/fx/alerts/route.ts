import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { db } from "@/lib/db";

const CreateAlertSchema = z.object({
  email: z.string().email(),
  baseCurrency: z.string().length(3),
  quoteCurrency: z.string().length(3),
  targetRate: z.number().positive(),
  direction: z.enum(["above", "below"]),
});

/** POST /api/fx/alerts — create a new rate alert */
export async function POST(request: NextRequest) {
  const body = await request.json();
  const parsed = CreateAlertSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Invalid request", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const { email, baseCurrency, quoteCurrency, targetRate, direction } = parsed.data;

  try {
    const id = crypto.randomUUID().replace(/-/g, "").slice(0, 20);
    await db.$executeRawUnsafe(
      `INSERT INTO RateAlert (id, email, baseCurrency, quoteCurrency, targetRate, direction, active, createdAt) VALUES ('${id}', '${email}', '${baseCurrency}', '${quoteCurrency}', ${targetRate}, '${direction}', 1, datetime('now'))`
    );
    return NextResponse.json({
      id,
      email,
      baseCurrency,
      quoteCurrency,
      targetRate,
      direction,
      active: true,
      createdAt: new Date().toISOString(),
    }, { status: 201 });
  } catch (e) {
    console.error("Failed to create alert:", e);
    return NextResponse.json(
      { error: "Failed to create alert" },
      { status: 500 }
    );
  }
}

/** GET /api/fx/alerts?email=... — list alerts for an email */
export async function GET(request: NextRequest) {
  const email = request.nextUrl.searchParams.get("email");
  if (!email) {
    return NextResponse.json(
      { error: "Email query parameter required" },
      { status: 400 }
    );
  }

  try {
    const alerts = await db.$queryRawUnsafe(
      `SELECT * FROM RateAlert WHERE email = '${email}' AND active = 1 ORDER BY createdAt DESC LIMIT 20`
    );
    return NextResponse.json(alerts);
  } catch (e) {
    console.error("Failed to list alerts:", e);
    return NextResponse.json(
      { error: "Failed to list alerts" },
      { status: 500 }
    );
  }
}

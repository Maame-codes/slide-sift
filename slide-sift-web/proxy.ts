import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const response = NextResponse.next();

  // Permanent block for the Vercel/Next dev toolbar and overlays
  response.headers.set("x-vercel-skip-toolbar", "1");
  response.headers.set("x-nextjs-hide-dev-overlay", "1");

  return response;
}

// Ensure this covers every single page of your SlideSift app
export const config = {
  matcher: "/:path*",
};

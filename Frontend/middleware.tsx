import type { NextRequest } from 'next/server'
import CheckIfAllowed from './app/_middleware/data';

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === "/scoreboard") {
    return CheckIfAllowed(request);
  }
}
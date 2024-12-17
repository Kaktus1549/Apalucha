import type { NextRequest } from 'next/server'
import CheckIfAllowed from './app/_middleware/data';
import { SetToken } from './app/_middleware/data';
import { errorLogin } from './app/_middleware/data';

export function middleware(request: NextRequest) {
  if (request.nextUrl.pathname === "/scoreboard") {
    return CheckIfAllowed(request);
  }
  if (request.nextUrl.pathname === "/login") {
    return SetToken(request);
  }
  if (request.nextUrl.pathname === "/error/login") {
    return errorLogin(request);
  }
}
"use server";

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { cookies } from 'next/headers'
import { headers } from "next/headers";


const url = process.env.BACKEND_URL;

export default async function CheckIfAllowed(request: NextRequest) {
    const cookieStore = cookies()
    const headersList = headers();
    const ip = headersList.get("X-REAL-IP") || request.ip || "";
    let token = cookieStore.get("token");
    if (token === undefined) {
        return NextResponse.redirect(new URL("/login", request.url));
    }

    async function getData(){
        try{
          let result = await fetch(url + "/scoreboard", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "X-REAL-IP": ip,
              "Cookie": "token=" + token?.value
              }
          });
          return (await result.json()) as ScoreboardAPI;
        }
        catch (e) {
            console.error(e);
            NextResponse.redirect(new URL("/error/500", request.url));
            return {error:"500"} as ScoreboardAPI;
        }
    }
    let data: ScoreboardAPI = await getData();
    if (data.error === "Failed to authenticate" ||
    data.error === "Token not found") {
      return NextResponse.redirect(new URL("/login", request.url));
    }
    else if(data.error === "Access denied"){
      return NextResponse.redirect(new URL("/error/403", request.url));
    }
    else {
      return NextResponse.next();
    }
}
export async function SetToken(request: NextRequest) {
  try{
    const url = new URL(request.url);
    const token = url.searchParams.get('token');

    if (token !== null){
      const response = NextResponse.redirect(new URL("/voting", request.url));
      response.cookies.set('token', token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        path: '/',
      });
      return response;
    }
    else{
      return NextResponse.next();
    }
  }
  catch(e){
      console.error("Error while parsing token" + e);
      return NextResponse.next();
  }

}
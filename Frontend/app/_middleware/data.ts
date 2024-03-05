"use server";

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { cookies } from 'next/headers'

const url = process.env.BACKEND_URL + '/api/';

export default async function CheckIfAllowed(request: NextRequest) {
    const cookieStore = cookies()
    let token = cookieStore.get("token");
    if (token === undefined) {
        return NextResponse.redirect(new URL("/login", request.url));
    }

    async function getData(){
        try{
            let result = await fetch(url + "scoreboard", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
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

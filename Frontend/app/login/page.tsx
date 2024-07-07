'use client';

import '../style/login.css'
import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react';
import { useEffect, useState } from 'react';
import LanguageConfig from '../Language/texts.json';

async function login(username: string | null, password: string | null, origin: string | null = null){
    let loginData = LanguageConfig.login;
    if (username === null && password === null){
        return;
    }
    let jsonData = {
            username: username,
            password: password
        }
    const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    });
    const data: APIResponse = await response.json() as APIResponse;
    if (data.message === 'OK'){
        if (origin !== null){
            // if someone sets invalid path, its their skill issue
            window.location.href = origin;
        }
        else{
            window.location.href = '/scoreboard';
        }
    }
    else{
        if (data.error == "Invalid username or password"){
            alert(loginData.wrong_credentials);
            return;
        }
        alert(loginData.login_error);
        console.error(data.error);
    }
}

export default function Login(){    
    let loginData = LanguageConfig.login;
    let origin = null as string | null;
    try{
        const searchParams = useSearchParams();
        origin = searchParams.get('origin') as string;
    }
    catch{
        console.error("Error while parsing origin");
    }

    function loginButton(){
        const username = (document.getElementById('username') as HTMLInputElement).value;
        const password = (document.getElementById('password') as HTMLInputElement).value;
        login(username, password, origin);
    }

    return(
        <Suspense>
            <div className="login-main-container">
                <div className="login">
                    <h1 className='login-h1'>{loginData.h1}</h1>
                    <div className="login-container">
                        <div className="option-container">
                            <p>{loginData.username_p}</p>
                            <input id="username" placeholder={loginData.username_placeholder}></input>
                        </div>
                        <div className="option-container">
                            <p>{loginData.password_p}</p>
                            <input id="password" type="password" placeholder={loginData.password_placeholder}></input>
                        </div>
                        <button onClick={loginButton}>{loginData.login_button}</button>
                    </div>
                </div>
            </div>
        </Suspense>
    );
}
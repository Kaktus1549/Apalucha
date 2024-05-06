'use client';

import '../style/login.css'
import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react';
import { useEffect, useState } from 'react';
import LanguageConfig from '../Language/texts.json';

async function login(username: string | null, password: string | null, token: string | null, origin: string | null = null){
    let loginData = LanguageConfig.login;
    if (username === null && password === null && token === null){
        return;
    }
    let jsonData;
    if (password === null && username === null && token !== null){
        jsonData = {
            token: token
        }
    }
    else{
        jsonData = {
            username: username,
            password: password
        }
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
        if (token !== null){
            window.location.href = '/voting';
        }
        else if (origin !== null){
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

export default function Voting(){    
    let loginData = LanguageConfig.login;
    let origin = null as string | null;
    try{
        const searchParams = useSearchParams();
        const token = searchParams.get('token');
        origin = searchParams.get('origin') as string;

        if (token !== null){
            login(null, null, token);
        }
    }
    catch{
        console.error("Error while parsing token or origin");
    }

    function loginButton(){
        const username = (document.getElementById('username') as HTMLInputElement).value;
        const password = (document.getElementById('password') as HTMLInputElement).value;
        login(username, password, null, origin);
    }

    // adds "login-body" class to body
    useEffect(() => {
        document.body.classList.add("login-body");
        return () => {
            document.body.classList.remove("login-body");
        }
    }, []);

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
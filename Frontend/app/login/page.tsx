'use client';

import '../style/login.css'
import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react';
import { useEffect } from 'react';
import LanguageConfig from '../Language/texts.json';

async function login(username: string | null, password: string | null, token: string | null){
    let loginData = LanguageConfig.login;
    if (username === null && password === null && token === null){
        return;
    }
    let jsonData;
    if (username === "" && password === "" || password === null && username === null){
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
function loginButton(){
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;
    login(username, password, null);
}

export default function Voting(){    
    let loginData = LanguageConfig.login;
    try{
        const searchParams = useSearchParams();
        const token = searchParams.get('token');

        if (token !== null){
            login(null, null, token);
        }
    }
    catch{
        console.error("Error while parsing token");
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
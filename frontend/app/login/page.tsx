'use client';

import '../style/login.css'
import { useSearchParams } from 'next/navigation'
import { Suspense } from 'react';

async function login(username: string | null, password: string | null, token: string | null){
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
            alert("Špatné uživatelské jméno nebo heslo");
            return;
        }
        alert("Něco se pokazilo, zkuste to prosím znovu");
        console.error(data.error);
    }
}
function loginButton(){
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;
    login(username, password, null);
}

export default function Voting(){
    const searchParams = useSearchParams();
    const token = searchParams.get('token');

    if (token !== null){
        login(null, null, token);
    }

    return(
        <Suspense>
            <div className="main-container">
                <div className="login">
                    <h1>Login</h1>
                    <div className="login-container">
                        <div className="option-container">
                            <p>Username</p>
                            <input id="username" placeholder="Enter username">
                            </input>
                        </div>
                        <div className="option-container">
                            <p>Password</p>
                            <input id="password" type="password" placeholder="Enter password"></input>
                        </div>
                        <button onClick={loginButton}>Login</button>
                    </div>
                </div>
            </div>
        </Suspense>
    );
}
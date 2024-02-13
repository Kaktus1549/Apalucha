'use client';

import '../style/login.css'
import { redirect, useSearchParams } from 'next/navigation'

export default function Voting(){
    const searchParams = useSearchParams();
    const token = searchParams.get('token');

    return(
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
                <button>Login</button>
            </div>
        </div>
    </div>
    );
}
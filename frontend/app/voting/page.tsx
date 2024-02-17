'use server'

import '../style/voting.css'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation'
import Film from './film';

export default async function Voting() {
    const cookieStore = cookies()
    const token = cookieStore.get('token')
    let data: APIResponse

    try{
        let api_url = process.env.BACKEND_URL + '/voting'
        let response = await fetch(api_url, { headers: { 'Cookie': `token=${token?.value}` } })
        data = await response.json() as APIResponse
    }
    catch (error){
        console.error(error)
        return(
            <div className="main-container">
                <h1 className='error-message'>Něco se pokazilo, zkuste to prosím znovu</h1>
            </div>
        )
    }
    if (data.error === "Failed to authenticate" || data.error === "Token not found") {
        redirect('/login')
    }
    else if (data.error === "Voting has not started") {
        return (
            <div className="main-container">
                <h1 className='error-message'>Voting has not started yet</h1>
            </div>
        );
    }

    return (
        <div className="main-container">
            <h1>Koho dnes zvolíš?</h1>
            <Film data={data} />
        </div>
    );
}
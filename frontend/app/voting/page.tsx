import '../style/voting.css'
import { cookies } from 'next/headers'
import { redirect } from 'next/navigation';
import Film from './film';

export default async function Voting() {
    const cookieStore = cookies()
    const token = cookieStore.get('token')

    let response = await fetch('https://apalucha.kaktusgame.eu/api/voting', { headers: { 'Cookie': `token=${token?.value}` } })
    let data: APIResponse = await response.json() as APIResponse
    if (data.error === "Failed to authenticate" || data.error === "Token not found") {
        return redirect('/login')
    }
    else if (data.error === "Voting has not started") {
        return (
            <div className="main-container">
                <h1>Voting has not started yet</h1>
            </div>
        );
    }

    return (
        <div className="main-container">
            <h1>Koho dnes zvolíš?</h1>
            <Film data={data} token={token?.value} />
        </div>
    );
}

function buttonClicked() {
    const buttons = document.querySelectorAll('button')
    buttons.forEach(button => {
        button.disabled = false
    })


}
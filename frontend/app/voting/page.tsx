import '../style/voting.css'
import { cookies } from 'next/headers'

export default async function Voting(){
    const cookieStore = cookies()
    const token = cookieStore.get('token')

    let data = await fetch('https://apalucha.kaktusgame.eu/api/voting', { headers: { 'Cookie': `token=${token}` } })
    data = await data.json()
    console.log(data)

    return(
        <div className="main-container">
        <h1>Koho dnes zvolíš?</h1>
        <div className="options-container">
        
        </div>
        <footer className="none">
            <button id="send">
                <p>Odeslat!</p>
            </button>
        </footer>
    </div>
    );
}
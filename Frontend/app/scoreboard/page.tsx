import '../style/scoreboard.css'
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers'
import StartButton from "./startbutton";

export default async function Scoreboard(){
    const cookieStore = cookies()
    const token = cookieStore.get('token')

    if(token === undefined){
        return redirect('/login')
    }

    return(
        <div className="scoreboard-main-container">
            <StartButton />
        </div>
    );
}
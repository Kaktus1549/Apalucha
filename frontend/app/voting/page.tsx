import '../style/voting.css'

export  default async function Voting(){
    
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
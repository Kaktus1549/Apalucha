import './style/landing.css';
import Link from 'next/link';

export default  function Home() {

  return (
    <div className="main-container">
        <h1>Film voting!</h1>
        <div className="vote-container">
            <div className="option-container">
                <Link href={"/voting"}>
                    <img src="images/voting.png" alt="Voting"/>
                </Link>
                <p>Zvol si svůj film!</p>
            </div>
            <div className="option-container">
                <Link href={"/scoreboard"}>
                    <img src="/images/scoreboard.png" alt="Scoreboard"/>
                </Link>
                <p>Scoreboard</p>
            </div>
        </div>
    </div>
  )
}

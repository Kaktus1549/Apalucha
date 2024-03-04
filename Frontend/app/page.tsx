import './style/landing.css';
import Image from 'next/image';
import Link from 'next/link';

export default function Home() {

  return (
    <div className="main-container">
        <h1>Film voting!</h1>
        <div className="vote-container">
            <div className="option-container">
                <Link href={"/voting"}>
                    <Image src="/images/voting.png" alt="Voting" width={1463} height={1352}/>
                </Link>
                <p>Zvol si svůj film!</p>
            </div>
            <div className="option-container">
                <Link href={"/scoreboard"}>
                    <Image src="/images/scoreboard.png" alt="Scoreboard" width={662} height={586} />
                </Link>
                <p>Scoreboard</p>
            </div>
        </div>
    </div>
  )
}

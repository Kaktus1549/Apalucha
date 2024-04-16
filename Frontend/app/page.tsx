import './style/landing.css';
import Image from 'next/image';
import Link from 'next/link';
import LanguageConfig from './Language/texts.json';

export default function Home() {
    let landingData = LanguageConfig.landing;
    return (
        <div className="main-container">
            <h1>{landingData.h1}</h1>
            <div className="vote-container">
                <div className="option-container">
                    <Link href={"/voting"}>
                        <Image src="/images/voting.png" alt="Voting" width={1463} height={1352} priority={true} />
                    </Link>
                    <p>{landingData.voting_p}</p>
                </div>
                <div className="option-container">
                    <Link href={"/scoreboard"}>
                        <Image src="/images/scoreboard.png" alt="Scoreboard" width={662} height={586} priority={true} />
                    </Link>
                    <p>{landingData.scoreboard_p}</p>
                </div>
            </div>
        </div>
    )
}

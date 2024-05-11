"use client";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import DisplayFilms from "./Films";
import CustomError from '../_error/error'
import LanguageConfig from '../Language/texts.json';

export default function StartButton() {
  let scoreboardData = LanguageConfig.scoreboard;
  const router = useRouter();
  const [time, setTime] = useState<number | string>("Start");
  const [films, setFilms] = useState<Films>({});
  const [ended, setEnded] = useState<boolean | null>(null);
  const [allowed, setAllowed] = useState<boolean>(true);
  const [votes, setVotes] = useState<number[]>([]);

  async function Countdown(time: number) {
    if (time === 0) {
      setTime(scoreboardData.end_voting_button);
      return;
    }
    let buttonText = scoreboardData.button_countdown + " " + time.toString()
    setTime(buttonText);
    setTimeout(() => Countdown(time - 1), 1000);
  }
  async function startButton() {
    try {
      let result = await fetch("/api/scoreboard", {
        method: "POST",
      });

      let data: ScoreboardAPI = (await result.json()) as ScoreboardAPI;
      if (data.error === "Failed to authenticate" ||
        data.error === "Token not found") {
        router.push("/login");
      }
      if(data.error === "Access denied"){
        setAllowed(false);
      }
      if (data.voteEnd === false) {
        setEnded(true);
        setFilms(data.films);
        setVotes(data.votes);
        return;
      }
      else {
        setEnded(false);
      }

      Countdown(Math.round(data.voteDuration));
      setFilms(data.films);
      setVotes(data.votes);
    }
    catch (e) {
      console.error(e);
      alert(scoreboardData.error_message);
    }
  }
  function revealLastFilms() {
    try{
      // selects all elements with class hidden
      let elements = document.getElementsByClassName("hidden");
      // sorts the elements by their id
      let sortedElements = Array.from(elements).sort((a, b) => {
        return parseInt(a.id) - parseInt(b.id);
      });
      // for highest id element, remove class hidden
      sortedElements[sortedElements.length - 1].classList.replace("hidden", "reveal");
    }
    catch(e){
      return;
    }
  }

  useEffect(() => {
    const keyDownHandler = (event: KeyboardEvent) => {
      if (event.key === 'Enter') {
        event.preventDefault();
        if (ended === true){
          revealLastFilms();
        }
      }
    };

    document.addEventListener('keydown', keyDownHandler);

    return () => {
      document.removeEventListener('keydown', keyDownHandler);
    };
  }, [ended, revealLastFilms]);
  
  return (
    <>
      
        {ended === null && allowed === true? (
          <>
            <button id="start" onClick={startButton}>
              {time}
            </button>
            <div className="apalucha">
              <h1 className="rotated">Apalucha 2024</h1>
            </div>
          </>
        ) :
          ended === false && allowed === true? (
            <>
              <button id="start" onClick={startButton}>
                {time}
              </button>
              <div className="vote-run">
                <DisplayFilms inputFilms={films || {}} ended={ended || false}  votes={votes || []}/>
              </div>
            </>
          ) : 
          allowed === true && ended === true? (
            <>
              <h1 className="scoreboard-h1">{scoreboardData.h1}</h1>
              <div className="header-frame">
                <p className="id">{scoreboardData.order_p}</p>
                <p className="name">{scoreboardData.name_p}</p>
                <p className="votes">{scoreboardData.votes_p}</p>
              </div>
              <div className="films">
                <DisplayFilms inputFilms={films || {}} ended={ended || false}  votes={votes || []} />
              </div>
            </>
          ):
          <CustomError statusCode={403} />
        }
    </>
  );
}

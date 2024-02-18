"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";
import DisplayFilms from "./Films";


export default function StartButton() {
  const router = useRouter();
  const [time, setTime] = useState<number | string>("Start");
  const [films, setFilms] = useState<Films>({});
  const [ended, setEnded] = useState<boolean | null>(null);
  const [votes, setVotes] = useState<number[]>([]);

  async function Countdown(time: number) {
    if (time === 0) {
      setTime("Show results");
      return;
    }
    setTime(time);
    setTimeout(() => Countdown(time - 1), 1000);
  }
  async function startButton() {
    try {
      let result = await fetch("/api/scoreboard", {
        method: "POST",
      });

      let data: ScoreboardAPI = (await result.json()) as ScoreboardAPI;
      if (data.error === "Failed to authenticate" ||
        data.error === "Token not found" ||
        data.error === "Access denied") {
        router.push("/login");
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
      alert("Něco se pokazilo, zkuste to prosím znovu");
    }
  }

  return (
    <>
      {ended === null ? (
        <button id="start" onClick={startButton}>
          {time}
        </button>
      ) :
        ended === false ? (
          <>
            <button id="start" onClick={startButton}>
              {time}
            </button>
            <div className="vote-run">
              <DisplayFilms inputFilms={films || {}} ended={ended || false}  votes={votes || []}/>
            </div>
          </>
        ) : (
          <>
            <h1>Apalucha 2024</h1>
            <div className="header-frame">
              <p className="id">Pořadí</p>
              <p className="name">Jméno filmu</p>
              <p className="votes">Počet hlasů</p>
            </div>
            <div className="films">
              <DisplayFilms inputFilms={films || {}} ended={ended || false}  votes={votes || []} />
            </div>
          </>
        )}
    </>
  );
}

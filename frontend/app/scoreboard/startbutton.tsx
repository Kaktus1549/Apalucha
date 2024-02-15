"use client";
import "../style/scoreboard.css";
import { useRouter } from "next/navigation";
import { useState } from "react";

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
    let result = await fetch("/api/scoreboard", {
      method: "POST",
    });

    let data: ScoreboardAPI = (await result.json()) as ScoreboardAPI;
    if (
      data.error === "Failed to authenticate" ||
      data.error === "Token not found" ||
      data.error === "Access denied"
    ) {
      router.push("/login");
    }
    if (data.voteEnd === false){
      setEnded(true);
      setFilms(data.films);
      setVotes(data.votes);
      return;
    }
    else{
      setEnded(false);
    }

    Countdown(Math.round(data.voteDuration));
    setFilms(data.films);
    setVotes(data.votes);
  }
  function DisplayFilms({ inputFilms }: { inputFilms: Films }) {
    let returnFilms = [];
    let length = Object.keys(inputFilms).length;
    if (length === 0) {
      return <></>;
    }
    if (ended === false) {
      let third = Math.floor(Object.keys(inputFilms).length / 3);
      for (let i = 0; i < third; i++) {
        returnFilms.push(
          <div key={"fimls-"+i.toString()} className="film">
            <p className="id">{i + 1}</p>
            <p className="name">{inputFilms[i + 1]}</p>
          </div>
        );
        returnFilms.push(
          <div key={(i + third).toString()} className="film">
            <p className="id">{i + third + 1}</p>
            <p className="name">{inputFilms[i + third + 1]}</p>
          </div>
        );
        returnFilms.push(
          <div key={(i + 2 * third).toString()} className="film">
            <p className="id">{i + 2 * third + 1}</p>
            <p className="name">{inputFilms[i + 2 * third + 1]}</p>
          </div>
        );
      }
      if (length % 3 === 1) {
        returnFilms.push(
          <div key={(length - 1).toString()} className="film">
            <p className="id">{length}</p>
            <p className="name">{inputFilms[length]}</p>
          </div>
        );
      } else if (length % 3 === 2) {
        returnFilms.push(
          <div key={(length - 2).toString()} className="film">
            <p className="id">{length - 1}</p>
            <p className="name">{inputFilms[length - 1]}</p>
          </div>
        );
        returnFilms.push(
          <div key={(length - 1).toString()} className="film">
            <p className="id">{length}</p>
            <p className="name">{inputFilms[length]}</p>
          </div>
        );
      }
      return returnFilms;
    }
    else if (ended === true) {
        let half = Math.floor(Object.keys(inputFilms).length / 2);
        let winningFilm = []
        let nonWinningFilms = []
        for(let i = 0; i < half; i++){
          if (i === 0){
            winningFilm.push(
              <div key={"winning-aura"} className="winning-aura">
                  <div className="film" key="winning-film">
                    <p className="id">{i + 1}.</p>
                    <p className="name">{inputFilms[i + 1]}</p>
                    <p className="votes">{votes[i]}</p>
                  </div>
              </div>
            );
          }
          else{
            nonWinningFilms.push(
                <div className="film" key={i+1}>
                  <p className="id">{i + 1}.</p>
                  <p className="name">{inputFilms[i + 1]}</p>
                  <p className="votes">{votes[i]}</p>
                </div>
            );
            if (length % 2 === 0){
              nonWinningFilms.push(
                  <div className="film" key={i + half}>
                    <p className="id">{i + half}.</p>
                    <p className="name">{inputFilms[i + half ]}</p>
                    <p className="votes">{votes[i + half - 1]}</p>
                  </div>
              );
            }
            else{
              nonWinningFilms.push(
                  <div className="film" key={ i + half + 1}>
                    <p className="id">{i + half + 1}.</p>
                    <p className="name">{inputFilms[i + half + 1]}</p>
                    <p className="votes">{votes[i + half]}</p>
                  </div>
              );
            }
          }
        }
        if (length % 2 === 1){
          nonWinningFilms.push(
            <div className="film" key={half+1}>
              <p className="id">{half+1}.</p>
              <p className="name">{inputFilms[half+1]}</p>
              <p className="votes">{votes[half]}</p>
            </div>
          );
          nonWinningFilms.push(
            <div className="film" key={length}>
              <p className="id">{length}.</p>
              <p className="name">{inputFilms[length]}</p>
              <p className="votes">{votes[length-1]}</p>
            </div>
          );
        }
        else if (length % 2 === 0 ){
          nonWinningFilms.push(
            <div className="film" key={length}>
              <p className="id">{length}.</p>
              <p className="name">{inputFilms[length]}</p>
              <p className="votes">{votes[length-1]}</p>
            </div>
          );
        }
        returnFilms.push(
          <>
            {winningFilm}
            <div className="non-winning">
              {nonWinningFilms}
            </div>
          </>
        )
        return returnFilms;
    }
  }

  return (
    <>
      {
      ended === null ? (
        <button id="start" onClick={startButton}>
          {time}
        </button>
      ):
      ended === false ? (
        <>
          <button id="start" onClick={startButton}>
            {time}
          </button>
          <div className="vote-run">
            <DisplayFilms inputFilms={films || {}} />
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
            <DisplayFilms inputFilms={films || {}} />
          </div>
        </>
      )}
    </>
  );
}

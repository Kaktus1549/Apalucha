function checkFilmName(name: string){
    // if name is longer than 16 characters, cut it off on 13th character and add "..."
    if (name.length > 20) {
      return name.slice(0, 17) + "...";
    }
    return name;
}
function voteRunFilmName(name: string){
    // if name is longer than 16 characters, cut it off on 13th character and add "..."
    if (name.length > 17) {
      return name.slice(0, 14) + "...";
    }
    return name;
}
function endDelay(order: number, filmLength: number){
  if ([1, 2, 3].includes(order)){
      return "0s";
  }
  let max = filmLength + 1;
  let time = max - order;
  return time + "s" as string;
}


export default function DisplayFilms({ inputFilms, ended, votes }: { inputFilms: Films; ended: boolean; votes: number[];}) {
  const delay = 3.5;
  const finalDelay = 1;
  let returnFilms = [];
  let length = Object.keys(inputFilms).length;
  if (length === 0) {
    return <></>;
  }
  if (ended === false) {
    let third = Math.floor(Object.keys(inputFilms).length / 3);
    for (let i = 0; i < third; i++) {
      returnFilms.push(
        <div style={{animationDelay: (i/delay).toString() + "s"}} key={"fimls-" + i.toString()} className="film">
          <p className="id">{i + 1}</p>
          <p className="name">{voteRunFilmName(inputFilms[i + 1])}</p>
        </div>
      );
      returnFilms.push(
        <div style={{animationDelay: ((i + third)/delay).toString() + "s"}} key={(i + third).toString()} className="film">
          <p className="id">{i + third + 1}</p>
          <p className="name">{voteRunFilmName(inputFilms[i + third + 1])}</p>
        </div>
      );
      returnFilms.push(
        <div style={{animationDelay: ((i + third *2)/delay).toString() + "s"}} key={(i + 2 * third).toString()} className="film">
          <p className="id">{i + 2 * third + 1}</p>
          <p className="name">{voteRunFilmName(inputFilms[i + 2 * third + 1])}</p>
        </div>
      );
    }
    if (length % 3 === 1) {
      returnFilms.push(
        <div style={{animationDelay: ((length-1)/delay).toString() + "s"}} key={(length - 1).toString()} className="film">
          <p className="id">{length}</p>
          <p className="name">{voteRunFilmName(inputFilms[length])}</p>
        </div>
      );
    } else if (length % 3 === 2) {
      returnFilms.push(
        <div style={{animationDelay: ((length-2)/delay).toString() + "s"}} key={(length - 2).toString()} className="film">
          <p className="id">{length - 1}</p>
          <p className="name">{voteRunFilmName(inputFilms[length - 1])}</p>
        </div>
      );
      returnFilms.push(
        <div style={{animationDelay: ((length-1)/delay).toString() + "s"}} key={(length - 1).toString()} className="film">
          <p className="id">{length}</p>
          <p className="name">{voteRunFilmName(inputFilms[length])}</p>
        </div>
      );
    }
    return returnFilms;
  }
  else if (ended === true) {
    let half = Math.floor(Object.keys(inputFilms).length / 2);
    let winningFilm = [];
    let nonWinningFilms = [];
    for (let i = 0; i < half; i++) {
      if (i === 0) {
        winningFilm.push(
          <div style={{animationDelay: endDelay(i + 1, length)}} key={"winning-aura"} className="winning-aura hidden" id={(i+1).toString()}>
            <div className="film" key="winning-film">
              <p className="id">{i + 1}.</p>
              <p className="name">{inputFilms[i + 1]}</p>
              <p className="votes">{votes[i]}</p>
            </div>
          </div>
        );
      }
      else {
        nonWinningFilms.push(
          <div style={{animationDelay: endDelay(i + 1, length)}} className={ [1, 2, 3].includes((i + 1)) ? "film hidden" : "film"} key={i + 1} id={(i+1).toString()}>
            <p className="id">{i + 1}.</p>
            <p className="name">{checkFilmName(inputFilms[i + 1])}</p>
            <p className="votes">{votes[i]}</p>
          </div>
        );
        if (length % 2 === 0) {
          nonWinningFilms.push(
            <div style={{animationDelay: endDelay(i + half, length)}} className={ [1, 2, 3].includes((i + half)) ? "film hidden" : "film"} key={i + half} id={(i+half).toString()}>
              <p className="id">{i + half}.</p>
              <p className="name">{checkFilmName(inputFilms[i + half])}</p>
              <p className="votes">{votes[i + half - 1]}</p>
            </div>
          );
        }
        else {
          nonWinningFilms.push(
            <div style={{animationDelay: endDelay(i + half + 1, length)}} className={ [1, 2, 3].includes((i + half + 1))? "film hidden" : "film"} key={i + half + 1} id={(i+half+1).toString()}>
              <p className="id">{i + half + 1}.</p>
              <p className="name">{checkFilmName(inputFilms[i + half + 1])}</p>
              <p className="votes">{votes[i + half]}</p>
            </div>
          );
        }
      }
    }
    if (length % 2 === 1) {
      nonWinningFilms.push(
        <div style={{animationDelay: endDelay(half + 1, length)}} className={ [1, 2, 3].includes((half + 1)) ? "film hidden" : "film"} key={half + 1} id={(half+1).toString()}>
          <p className="id">{half + 1}.</p>
          <p className="name">{checkFilmName(inputFilms[half + 1])}</p>
          <p className="votes">{votes[half]}</p>
        </div>
      );
      nonWinningFilms.push(
        <div style={{animationDelay: endDelay(length, length)}} className={ [1, 2, 3].includes(length)? "film hidden" : "film"} key={length} id={length.toString()}>
          <p className="id">{length}.</p>
          <p className="name">{checkFilmName(inputFilms[length])}</p>
          <p className="votes">{votes[length - 1]}</p>
        </div>
      );
    }
    else if (length % 2 === 0) {
      nonWinningFilms.push(
        <div style={{animationDelay: endDelay(length, length)}} className={ [1, 2, 3].includes(length) ? "film hidden" : "film"} key={length} id={length.toString()}>
          <p className="id">{length}.</p>
          <p className="name">{checkFilmName(inputFilms[length])}</p>
          <p className="votes">{votes[length - 1]}</p>
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
    );
    return returnFilms;
  }
}
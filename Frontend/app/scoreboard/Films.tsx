function endDelay(order: number, filmLength: number){
  if ([1, 2, 3].includes(order)){
      return "0s";
  }
  let max = filmLength + 1;
  let time = max - order;
  return time + "s" as string;
}
function voteRunFilm(i: number, filmKeys: string[], films: Films, delay: number){
  return(
      <>
        <div style={{animationDelay: (i/delay).toString() + "s"}} key={"fimls-" + i.toString()} className="film">
          <p className="id">{filmKeys[i]}</p>
          <p className="name">{films[parseInt(filmKeys[i])]}</p>
        </div>
      </>
    );
}
function endedRunFilm(i: number, filmKeys: string[], films: Films, votes: number[]){
  if (i === 0){
    return(
      <>
        <div style={{animationDelay: endDelay(i + 1, filmKeys.length)}} key={"winning-aura"} className="winning-aura hidden" id={(i+1).toString()}>
          <div className="film" key="winning-film">
            <p className="id">{i + 1}.</p>
            <p className="name">{films[parseInt(filmKeys[i])]}</p>
            <p className="votes">{votes[i]}</p>
          </div>
        </div>
      </>
    );
  }
  else{
    return(
      <>
        <div style={{animationDelay: endDelay(i + 1, filmKeys.length)}} className={ [1, 2, 3].includes((i + 1)) ? "film hidden" : "film"} key={i + 1} id={(i+1).toString()}>
          <p className="id">{i + 1}.</p>
          <p className="name">{films[parseInt(filmKeys[i])]}</p>
          <p className="votes">{votes[i]}</p>
        </div>
      </>
    );
  
  }
}


export default function DisplayFilms({ inputFilms, ended, votes }: { inputFilms: Films; ended: boolean; votes: number[];}) {
  const delay = 3.5;
  let returnFilms = [];
  let length = Object.keys(inputFilms).length;
  let keys = Object.keys(inputFilms);
  if (length === 0) {
    return <></>;
  }
  if (ended === false) {
    let third = Math.floor(Object.keys(inputFilms).length / 3);
    for (let i = 0; i < third; i++) {
      returnFilms.push(voteRunFilm(i, keys, inputFilms, delay));
      returnFilms.push(voteRunFilm(i + third, keys, inputFilms, delay));
      returnFilms.push(voteRunFilm(i + 2 * third, keys, inputFilms, delay));
    }
    if (length % 3 === 1) {
      returnFilms.push(voteRunFilm(length - 1, keys, inputFilms, delay));
    } else if (length % 3 === 2) {
      returnFilms.push(voteRunFilm(length - 2, keys, inputFilms, delay));
      returnFilms.push(voteRunFilm(length - 1, keys, inputFilms, delay));
    }
    return returnFilms;
  }
  else if (ended === true) {
    let half = Math.floor(Object.keys(inputFilms).length / 2);
    let winningFilm = [];
    let nonWinningFilms = [];
    for (let i = 0; i < half; i++) {
      if (i === 0) {
        winningFilm.push(endedRunFilm(i, keys, inputFilms, votes));
      }
      else {
        nonWinningFilms.push(endedRunFilm(i, keys, inputFilms, votes));
        if (length % 2 === 0) {
          nonWinningFilms.push(endedRunFilm(i + half - 1, keys, inputFilms, votes));
        }
        else {
          nonWinningFilms.push(endedRunFilm(i + half, keys, inputFilms, votes));
        }
      }
    }
    if (length % 2 === 1) {
      nonWinningFilms.push(endedRunFilm(half, keys, inputFilms, votes));
      nonWinningFilms.push(endedRunFilm(length-1, keys, inputFilms, votes));
    }
    else if (length % 2 === 0) {
      nonWinningFilms.push(endedRunFilm(length-1, keys, inputFilms, votes));
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
// Gets config file
var apiEndpoint;
var websiteUrl;
var scoreBoardHeader;

fetch('config.json')
    .then(response => response.json())
    .then(data => {
        // Sets the URL
        apiEndpoint = data["apiEndpoint"];
        websiteUrl = data["websiteUrl"];
        scoreBoardHeader = data["scoreBoardHeader"];
    })
    .catch(error => console.error(error));

function addFilm(voteEnded, isWinner, filmName, filmId, filmVotes = null){
    if(voteEnded === true){
        var filmsDiv = document.getElementsByClassName("films")[0];
        if(isWinner === true){
            var winningAura = document.getElementsByClassName("winning-aura")[0];
            var film = document.createElement("div");
            film.className = "film";
            winningAura.appendChild(film);
        }
        else{
            var nonWinning = document.getElementsByClassName("non-winning")[0];
            var film = document.createElement("div");
            film.className = "film";
            nonWinning.appendChild(film);
        }
    }
    else{
        var filmsDiv = document.getElementsByClassName("vote-run")[0];
        var film = document.createElement("div");   
        film.className = "film";
        filmsDiv.appendChild(film);
    }
    var id = document.createElement("p");
    id.className = "id";
    id.innerHTML = filmId + ".";
    film.appendChild(id);
    var name = document.createElement("p");
    name.className = "name";
    name.innerHTML = filmName;
    film.appendChild(name);
    if(filmVotes !== null){
        var votes = document.createElement("p");
        votes.className = "votes";
        votes.innerHTML = filmVotes;
        film.appendChild(votes);
    }
}
// what happens when timer ends
function timerEnd(){
    var test;
}

// Countdown function for button, also disables button
function countdown(time, button){
    var timeLeft = time;
    button.disabled = true;
    button.innerText = timeLeft;

    var intervalId = setInterval(function() {
        timeLeft--;
        button.innerText = timeLeft;

        if (timeLeft <= 0) {
            clearInterval(intervalId);
            button.innerText = "Start";
            button.disabled = false;
        }
    }, 1000);
}
// Countdown button
function buttonClick(){
    var button = document.getElementById("start");
    
    // sends POST with start message to API
    fetch(apiEndpoint + "/scoreboard", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Token": localStorage.getItem("token")
        },
        body: JSON.stringify({
            "message": "start"
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data["message"] === "OK"){
            // Starts countdown
            countdown(data["time"], button);
        } 
        else if (data["message"] === "401"){
            window.location.href = websiteUrl + "/login";
        }
        else{
            console.log(data);
            alert("Something went wrong");
        }
    })
}


function insertFilms(voteEnded, filmData){
    var mainDiv = document.getElementsByClassName("main-container")[0];
    
    // If voting ended
    if(voteEnded === true){
        // Remove vote-run with all its children
        var voteRun = document.getElementsByClassName("vote-run")[0];
        voteRun.parentNode.removeChild(voteRun);
        voteRun.remove();

        // Creates header
        var headerFrame = document.createElement("div");
        headerFrame.className = "header-frame";
        mainDiv.appendChild(headerFrame);
        var idHeader = document.createElement("p");
        idHeader.className = "id";
        idHeader.innerHTML = scoreBoardHeader[0];
        headerFrame.appendChild(idHeader);
        var nameHeader = document.createElement("p");
        nameHeader.className = "name";
        nameHeader.innerHTML = scoreBoardHeader[1];
        headerFrame.appendChild(nameHeader);
        var votesHeader = document.createElement("p");
        votesHeader.className = "votes";
        votesHeader.innerHTML = scoreBoardHeader[2];
        headerFrame.appendChild(votesHeader);

        // Creates films div
        var filmsDiv = document.createElement("div");
        filmsDiv.className = "films";
        mainDiv.appendChild(filmsDiv);
        // Winning aura
        var winningAura = document.createElement("div");
        winningAura.className = "winning-aura";
        filmsDiv.appendChild(winningAura);
        // Non-winning films
        var nonWinning = document.createElement("div");
        nonWinning.className = "non-winning";
        filmsDiv.appendChild(nonWinning);

        half = Math.floor(Object.keys(filmData).length / 2);
        for(var i = 0; i < half; i++){
            if(i === 0){
                addFilm(true, true, filmData[i+1][0], i+1, filmData[i+1][1]);
            }
            else{
                addFilm(true, false, filmData[i+1][0], i+1, filmData[i+1][1]);
                addFilm(true, false, filmData[half+i+1][0], half+i+1, filmData[half+i+1][1]);
            }
        }
        if(Object.keys(filmData).length % 2 === 1){
            addFilm(true, false, filmData[half+1][0], half+1, filmData[half+1][1]);
            addFilm(true, false, filmData[Object.keys(filmData).length][0], Object.keys(filmData).length, filmData[Object.keys(filmData).length][1]);
        }
    }
    if(voteEnded === false){
        var voteRun = document.getElementsByClassName("vote-run")[0];

        third = Math.floor(Object.keys(filmData).length / 3);
        for(var i = 0; i < third; i++){
            addFilm(false, false, filmData[i+1][0], i+1);
            addFilm(false, false, filmData[third+i+1][0], third+i+1);
            addFilm(false, false, filmData[2*third+i+1][0], 2*third+i+1);
        }
        if(Object.keys(filmData).length % 3 === 1){
            addFilm(false, false, filmData[Object.keys(filmData).length][0], Object.keys(filmData).length);
        }
        if(Object.keys(filmData).length % 3 === 2){
            addFilm(false, false, filmData[Object.keys(filmData).length-1][0], Object.keys(filmData).length-1);
            addFilm(false, false, filmData[Object.keys(filmData).length][0], Object.keys(filmData).length);
        }
    }
}
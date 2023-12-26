// Gets config file
var apiEndpoint;
var websiteUrl;
var tooFastMessage;
var myVote;

fetch('config.json')
    .then(response => response.json())
    .then(data => {
        // Sets the URL
        apiEndpoint = data["apiEndpoint"];
        websiteUrl = data["websiteUrl"];
        tooFastMessage = data["tooFastMessage"];
    })
    .catch(error => console.error(error));

// When button is clicked, it will undisable all buttons and disable the clicked one, then it will send post request to API to vote for film
function buttonClicked(){
    var buttons = document.getElementsByTagName("button");
    var footer = document.getElementsByTagName("footer")[0];

    for(var i = 0; i < buttons.length; i++){
        buttons[i].disabled = false;
    }
    this.disabled = true;
    myVote = this.id;

    footer.classList.remove("none");
    footer.classList.add("element-appear");
}
function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}
async function sendVote(){
    var sendButton = document.getElementById("send");
    sendButton.disabled = true;
    fetch(apiEndpoint + "/voting", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Token': localStorage.getItem("token")
        },
        body: JSON.stringify({
            "vote": myVote
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data["error"] != undefined){
            if(data["error"] == "401"){
                window.location.href = websiteUrl + "/login";
            }
            else if(data["error"] == "tooFast"){
                tooFast();
            }
            else{
                alert("Error: " + data["error"]);
            }
        }
    })
    .catch(error => console.error(error) && alert("Error: " + error));
    await sleep(2000);
    sendButton.disabled = false;
}

// As input takes object with films, then it inserts them into the page
function insertFilms(films){
    var container = document.getElementsByClassName("options-container")[0];
    for(var i = 0; i < Object.keys(films).length; i++){
        var filmId = Object.keys(films)[i];
        var filmName = films[filmId];
        var option = document.createElement("div");
        option.className = "option";
        var button = document.createElement("button");
        button.id = filmId;
        button.onclick = buttonClicked;
        var film = document.createElement("div");
        film.className = "film";
        var filmNameParagraph = document.createElement("p");
        filmNameParagraph.innerHTML = filmName;
        film.appendChild(filmNameParagraph);
        option.appendChild(button);
        option.appendChild(film);
        container.appendChild(option);
    }
}
function tooFast(){
    var main = document.getElementsByClassName("options-container")[0];
    var h2 = document.createElement("h2");
    h2.innerHTML = tooFastMessage;
    main.appendChild(h2);
}
// Sends get request to API to get films, if ok server returns {"1": "film1", "2": "film2", "3": "film3"}, if not server returns {"error": "error message"}, example -> {"error":"401"} user not logged in
// if voting is not active, server returns {"error": "tooFast"}
function getFilms(){
    fetch(apiEndpoint + "/voting", {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Token': localStorage.getItem("token")
        }
    })
    .then(response => response.json())
    .then(data => {
        if(data["error"] != undefined){
            if(data["error"] == "401"){
                window.location.href = websiteUrl + "/login";
            }
            else if(data["error"] == "tooFast"){
                tooFast();
            }
            else{
                alert("Error: " + data["error"]);
            }
        }
        else{
            insertFilms(data);
        }
    })
    .catch(error => console.error(error) && alert("Error: " + error));
}

window.onload = getFilms;
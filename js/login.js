// Gets config file
var apiEndpoint;
var websiteUrl;

fetch('config.json')
    .then(response => response.json())
    .then(data => {
        // Sets the URL
        apiEndpoint = data["apiEndpoint"];
        websiteUrl = data["websiteUrl"];
    })
    .catch(error => console.error(error));

// Login via token in url (for voting)
function loginViaToken(){
    // Gets the token from the url
    var url = new URL(window.location.href);
    var token = url.searchParams.get("token");

    // If token is not null, saves securely token to cokie and redirects to voting page
    if(token != null){
        console.log(token);
        document.cookie = "token=" + token + "; HttpOnly; path=/"
        window.location.href = websiteUrl + "/voting";
        console.log(document.cookie);
    }
}
// Login button click event (for scoreboard)
function login(){
    // Get the username and password from the input fields
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    // Prepare data in JSON format
    var data = JSON.stringify({"username":username, "password":password});

    // Sends a POST request to /api/login endpoint
    // response {"success": true, "token": <token>} or {"success": false, "error": <error>}
    fetch(apiEndpoint + "/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: data
    })
    .then(response => response.json())
    .then(data => {
        // If login is successful, saves token securely to cookie and redirects to scoreboard
        if(data["success"]){
            document.cookie = "token=" + data["token"] + "; HttpOnly; path=/"
            window.location.href = websiteUrl + "/scoreboard";
        }
        // If login is not successful, shows the error
        else{
            alert(data["error"]);
        }
    })
    .catch(error => alert(error) && console.error(error)); 
}
window.onload = loginViaToken;
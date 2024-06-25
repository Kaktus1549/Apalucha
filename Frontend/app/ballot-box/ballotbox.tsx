'use client';

import { useState, useEffect } from "react";
import LanguageConfig from '../Language/texts.json';

async function getToken(){
    let response = await fetch('/api/managment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            "action": "ballotbox",
            "data": {}
        })
    });
    if (response.status === 500) {
        return "500";
    }
    else if (response.status === 401 || response.status === 403) {
        // redirects to /login
        window.location.href = "/login?origin=/ballot-box";
    }
    else if (response.status === 200) {
        return "200";
    }
    //ballotbox token will be set as a cookie by the server response, which has Set-Cookie header
}

export default function BallotBox() {
    let ballotData = LanguageConfig.ballot;
    const [disabledButton, setDisabledButton] = useState<string | null>(null)
    const [renderList, setRenderList] = useState<string[]>([]);
    const [sending, setSending] = useState<boolean>(false)
    const [data, setData] = useState<APIResponse>({error : "null"} as APIResponse)
    const [time, setTime] = useState<string>();

    async function fetchData() {
        let responseData: APIResponse
        try{
            let response = await fetch('/api/ballotbox')
            responseData = await response.json() as APIResponse
        }
        catch(err){
            console.error("Something went wrong while fetching data" + err)
            setData({error: "Could not retrieve films"} as APIResponse)
            return
        }
        if (responseData.error === "Voting has not started") {
            setData({error: "Voting has not started"} as APIResponse)
        }
        else if (responseData.error === "Token not found" || responseData.error === "Failed to authenticate") {
            getToken();
        }
        else if (responseData.error === "Failed to retrieve films") {
            setData({error: "Could not retrieve films"} as APIResponse)
        }
        else if (responseData.error === "You have to wait to vote again"){
            setData({error: "You have to wait to vote again", time: responseData.remaining} as APIResponse)
            Countdown(parseInt(responseData.remaining))
        }
        else{
            setData(responseData)
        }
    }
    async function Countdown(time: number) {
        if (time === 0) {
            // try to fetch data again
            fetchData();
            return;
        }
        let buttonText = ballotData.wait_message  + " " + time.toString()
        setTime(buttonText);
        setTimeout(() => Countdown(time - 1), 1000);
    }
    function handleSelect(id: string) {
        setDisabledButton(id)
    }
    async function sendVote(id: string | null) {
        if (id === null) {
            return;
        }
        setSending(true)
        let response = await fetch('/api/ballotbox', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "vote": id })
        });
    
        let responseJson = await response.json();
        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
                window.location.href = "/login?origin=/ballot-box";
            }
            if (response.status === 500) {
                let alert_text = ballotData.error_message
                alert(alert_text)
                console.error(response)
            }
            if (response.status === 425){
                setDisabledButton(null)
                setData({error: "You have to wait to vote again", time: responseJson.remaining} as APIResponse)
                Countdown(parseInt(responseJson.remaining))
            }
            else{
                console.error(response)
                alert("Something went wrong, got unknown status code: " + response.status)
            }
            setTimeout(() => setSending(false), 2000)
            return
        }
        setDisabledButton(null)
        setData({error: "You have to wait to vote again", time: responseJson.remaining} as APIResponse)
        Countdown(parseInt(responseJson.remaining))
        setTimeout(() => setSending(false), 2000)
    }
    
    useEffect(() => {
        if (data.error === "Voting has not started" || data.error === "Could not retrieve films" || data.error === "null") {
        fetchData();
        const intervalId = setInterval(() => {
            if (data.error === "Voting has not started" || data.error === "Could not retrieve films" || data.error === "null") {
                fetchData();
            }
        }, 10000);
        return () => clearInterval(intervalId)
        }
    });
    useEffect(() => {
        let timeoutId: NodeJS.Timeout;

        const addNextItem = (index: number) => {
            const keys = Object.keys(data);
            // If there is key with name of "error" then we don't want to add it to the list
            if (keys.length === 1 && keys[0] === "error") {
              return;
            }
            // If current key is "error" or "time" then skip it
            if (keys[index] === "error" || keys[index] === "time") {
              addNextItem(index + 1);
              return;
            }
            if (index < keys.length) {
                // check if key is not duplicate, if it is, skip it
                if (renderList.includes(keys[index])) {
                    addNextItem(index + 1);
                    return;
                }
              setRenderList((currentList) => [
                ...currentList,
                keys[index],
              ]);
              timeoutId = setTimeout(() => addNextItem(index + 1), 150); 
            }
          };
      
          addNextItem(0);
      
          return () => clearTimeout(timeoutId); // Cleanup to avoid memory leak
    }, [data]);
    return(
        <div className="voting-main-container">
            {
                data.error === "Voting has not started"?
                <h1 className="error-message voting-h1">{ballotData.not_started}</h1>
                : data.error === "Could not retrieve films"?
                <h1 className="error-message voting-h1">{ballotData.film_error}</h1>
                : data.error === "You have to wait to vote again"?
                <h1 className="error-message voting-h1">{time}</h1>
                : renderList.length > 0?
                <>
                    <h1 className="voting-h1">{ballotData.h1}</h1>
                    <div className="options-container">
                    {renderList.map((id) => (
                        <div key={id} className="option element-appear">
                        <button id={id} disabled={id !== null && id === disabledButton} onClick={() => handleSelect(id)}></button>
                        <div className="film">
                            <p className="id">{id}</p>
                            <p className="name">{data[id]}</p>
                        </div>
                        </div>
                    ))}
                    </div>
                    {disabledButton !== null ?
                        <footer className="element-appear">
                            <button onClick={() => sendVote(disabledButton)} disabled={sending}>
                                <p>{ballotData.vote_button}</p>
                            </button>
                        </footer>
                        : null}
                </>
                : null
            }
        </div>
    );
}

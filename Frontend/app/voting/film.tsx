'use client'
import { useState, useEffect } from "react";
import { useRouter } from 'next/navigation'
import CustomError from '../_error/error'

export default function Film() {
    const [disabledButton, setDisabledButton] = useState<string | null>(null)
    const [renderList, setRenderList] = useState<string[]>([]);
    const [sending, setSending] = useState<boolean>(false)
    const [data, setData] = useState<APIResponse>({error : "null"} as APIResponse)
    const router = useRouter()

    async function fetchData() {
        let responseData: APIResponse
        try{
            let response = await fetch('/api/voting')
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
            setData({error: "Token not found"} as APIResponse)
        }
        else if (responseData.error === "Admins can't vote") {
            setData({error: "Admins can't vote"} as APIResponse)
        }
        else if (responseData.error === "Could not retrieve films") {
            setData({error: "Could not retrieve films"} as APIResponse)
        }
        else{
            setData(responseData)
        }
    }
    function handleSelect(id: string) {
        setDisabledButton(id)
    }
    async function sendVote(id: string | null) {
        if (id === null) {
            return;
        }
        setSending(true)
        let response = await fetch('/api/voting', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ "vote": id })
        })
        if (!response.ok) {
            if (response.status === 401) {
                setData({error: "Token not found"} as APIResponse)
            }
            if (response.status === 500) {
                alert("Něco se pokazilo, zkuste to prosím znovu.")
                console.error(response)
            }
            setTimeout(() => setSending(false), 2000)
            return
        }
        setTimeout(() => setSending(false), 2000)

    }

    useEffect(() => {
        fetchData();
        const intervalId = setInterval(fetchData, 10000)
        return () => clearInterval(intervalId)
    }, [])

    // adds "voting-body" class to body element
    useEffect(() => {
        document.body.classList.add("voting-body");
        return () => document.body.classList.remove("voting-body");
    }, []);

    useEffect(() => {
        let timeoutId: NodeJS.Timeout;

        const addNextItem = (index: number) => {
            const keys = Object.keys(data);
            // If there is key with name of "error" then we don't want to add it to the list
            if (keys.length === 1 && keys[0] === "error") {
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
    }, [data, renderList]); 
    
    return (
        <div className="voting-main-container">
            {
                data.error === "Token not found"?
                <CustomError statusCode={401} />
                :
                data.error === "Voting has not started"?
                <h1 className="error-message voting-h1">Jěště jsme nezačali hlasovat!</h1>
                :
                data.error === "Could not retrieve films"?
                <h1 className="error-message voting-h1">Něco se pokazilo, zkuste to prosím znovu.</h1>
                : data.error === "Token not found" || data.error === "Failed to authenticate" || data.error === "null"?
                 <></>
                :
                data.error === "Admins can't vote"?
                <CustomError statusCode={403} />
                :
                <>
                    <h1 className="voting-h1">Koho dnes zvolíš?</h1>
                    <div className="options-container">
                    {renderList.map((id) => (
                        <div key={id} className="option element-appear">
                        <button id={id} disabled={id !== null && id === disabledButton} onClick={() => handleSelect(id)}></button>
                        <div className="film">
                            <p>{data[id]}</p>
                        </div>
                        </div>
                    ))}
                    </div>
                    {disabledButton !== null ?
                        <footer className="element-appear">
                            <button onClick={() => sendVote(disabledButton)} disabled={sending}>
                                <p>Odeslat!</p>
                            </button>
                        </footer>
                        : null}
                </>
            }
        </div>
    );
} 
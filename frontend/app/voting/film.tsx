'use client'
import { useState, useEffect } from "react";
import { useRouter } from 'next/navigation'

export default function Film() {
    const [disabledButton, setDisabledButton] = useState<string | null>(null)
    const [sending, setSending] = useState<boolean>(false)
    const [data, setData] = useState<APIResponse>({error: "Voting has not started"} as APIResponse)
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
        if (responseData.error === "Token not found" || responseData.error === "Failed to authenticate") {
            router.push('/login')
        }
        if (responseData.error === "Could not retrieve films") {
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
                router.push('/login')
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

    return (
        <div className="main-container">
            {
                data.error === "Voting has not started"?
                <h1 className="error-message">Jěště jsme nezačali hlasovat!</h1>
                :
                data.error === "Could not retrieve films"?
                <h1 className="error-message">Něco se pokazilo, zkuste to prosím znovu.</h1>
                : data.error === "Token not found" || data.error === "Failed to authenticate"?
                 <></>
                :
                <>
                    <h1>Koho dnes zvolíš?</h1>
                    <div className="options-container">
                        {Object.keys(data).map((id: string) => (
                            <div key={id} className="option">
                                <button id={id} disabled={id != null && id == disabledButton} onClick={() => handleSelect(id)}></button>
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
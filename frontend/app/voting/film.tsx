'use client'
import { useState } from "react";
import { useRouter } from 'next/navigation'

export default function Film({ data }: { data: APIResponse}) {
    const [disabledButton, setDisabledButton] = useState<string | null>(null)
    const [sending, setSending] = useState<boolean>(false)
    const router = useRouter()

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

    return (
        <>
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
    );
} 
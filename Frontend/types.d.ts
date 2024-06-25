interface APIResponse {
    error: string,
    [key: string]: string,
    message: string,
    time: string
}
interface Films{
    [key: number]: string
}

interface ScoreboardAPI{
    voteEnd: boolean | string,
    voteDuration: number,
    films: ScoreboardsFilms,
    error: string,
    votes: number[]
}
declare module 'js-cookie';
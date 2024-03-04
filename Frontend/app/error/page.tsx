'use client';

import CustomError from "../_error/error";
import { useSearchParams } from 'next/navigation'

export default function Error(){
    try{
        const searchParams = useSearchParams();
        const errorCode = Number(searchParams.get('code'));
        return (
            <CustomError statusCode={errorCode}/>
        )
    }
    catch (e){
        console.error(e);
    }
}

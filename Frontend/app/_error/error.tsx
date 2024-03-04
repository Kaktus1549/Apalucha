import React from 'react';
import Image from 'next/image';
import '../style/error.css';

export default function CustomError(statusCode: {statusCode: number}){
    let error = statusCode.statusCode.toString()
    return(
        <div className="holder">
            <div className="error">
                <Image src={`https://http.cat/${error}`} alt="error" width={750} height={600} />
            </div>
        </div>
    );
}
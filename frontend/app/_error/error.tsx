import React from 'react';
import '../style/error.css';

export default function CustomError(statusCode: {statusCode: number}){
    let error = statusCode.statusCode.toString()
    return(
        <div className="holder">
            <div className="error">
                <img src={`https://http.cat/${error}`} alt="error" />
            </div>
        </div>
    );
}
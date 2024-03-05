
import CustomError from "../../_error/error";
export function generateStaticParams() {
    return [400, 401, 403, 404, 500]
}

export default function Error({ params: { id }}: { params: { id: number }}) {
    try{
        const errorCode: number = id;
        return (
            <CustomError statusCode={errorCode}/>
        )
    }
    catch (e){
        console.error(e);
    }
}

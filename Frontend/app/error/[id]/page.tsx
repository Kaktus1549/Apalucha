import CustomError from "../../_error/error";

export function generateStaticParams() {
    return [
        { id: "400" },
        { id: "401" },
        { id: "403" },
        { id: "404" },
        { id: "500" },
    ];
}

export default async function Error({ params }: { params: Promise<{ id: string }> }) {
    const { id } = await params;
    const errorCode = parseInt(id);
    return <CustomError statusCode={errorCode} />;
}

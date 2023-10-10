import { router } from "next/client";

export default function Message({title, content, uid, type, setIsModal}: {
    title: string,
    content: string,
    uid?: string,
    type?: string,
    setIsModal: any
}) {
    return (
        <div className={`z-50 absolute h-screen w-screen backdrop-brightness-50 backdrop-blur`}>
            <div className={`w-full h-full flex flex-col justify-center items-center`}>
                <div
                    className={`w-[400px] h-[230px] py-10 px-10 bg-white drop-shadow-2xl rounded-lg flex flex-col justify-between`}>
                    <div className={`flex flex-col gap-4`}>
                        <div className={`font-bold text-lg`}>{title}</div>
                        <div className={`whitespace-normal`}>{content}</div>
                    </div>
                    <div className={`justify-end flex`}>
                        <button
                            className={`bg-color-primary-500 w-[50%]  text-white py-1 rounded-lg`}
                            onClick={() => {
                                router.push("/patient/postures");
                                setIsModal(false);
                            }}>확인
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
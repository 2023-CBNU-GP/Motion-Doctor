import Navigation from "../components/navigation";
import {useState} from "react";

export default function Test () {
    const data = [
        {
            tag : '등배운동',
            img : '',
        },
        {
            tag : '호흡',
            img: ''
        }
    ];

    const [tag, setTag] = useState(data[0].tag);

    return (
        <div className="h-screen overflow-hidden">
            <Navigation></Navigation>

            <div className="flex h-full">
                <div className="flex flex-col overflow-hidden w-[20%] drop-shadow-sm overflow-y-scroll divide-y divide-stone-200 divide-solid">
                    {
                        data.map(item => {
                            return <div key={item.tag} onClick={() => {setTag(item.tag);}}
                                        className={`${tag === item.tag && "bg-color-primary-100 font-bold"} py-5 px-3 text-center cursor-pointer `}>
                                {item.tag}
                            </div>
                        })
                    }

                </div>
                <div className="h-full w-[40%] ">
                    <div>{tag}</div>
                </div>
                <div className="h-full w-[40%]">
                    <div>{tag}</div>
                </div>
            </div>

        </div>
    );
}
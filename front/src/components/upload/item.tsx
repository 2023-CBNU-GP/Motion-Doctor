import React, { useRef, useState } from "react";
import { UploadItem } from "@md/interfaces/upload.interface";

export default function Item({itemData, handleChange, handleRemove}: {
    itemData: UploadItem,
    handleChange: any,
    handleRemove: any
}) {
    const [isModified, setIsModified] = useState(false);
    const [item, setItem] = useState<UploadItem>(itemData!);
    const inputRef = useRef<HTMLInputElement | null>(null);

    const handleInputChange = (e: any) => {
        if (e.target.name === "filePath") {
            const files = e.target.files[0];
            const path = e.target.value;
            setItem({
                    ['name']: item.name,
                    ['tag']: item.tag,
                    ["file"]: files,
                    [e.target.name]: path
                }
            );
            handleChange(item.id, item.name, path, files);
        } else setItem({...item, [e.target.name!]: e.target.value!});
    };

    return (
        <div className="bg-gray-50 flex gap-4 items-center pb-1">
            <div className={`cursor-pointer`} onClick={() => handleRemove(item?.id)}>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1}
                     stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
            </div>
            <input name={"name"}
                   value={item?.name}
                   className={`w-[40%] bg-transparent`}
                   disabled={!isModified}
                   type={"text"}
                   onChange={handleInputChange}/>
            {
                isModified ? <input
                        className={`w-full text-slate-500 file:bg-color-primary-500 file:text-white file:border-0 file:rounded-xl file:font-semibold file:px-2.5 hover:file:bg-color-primary-400`}
                        ref={inputRef} name={"filePath"} type={"file"}
                        onChange={handleInputChange}/> :
                    <div className={`w-full`}>{item?.filePath as string}</div>
            }
            {isModified ? <button className={`min-w-fit`} onClick={() => setIsModified(false)}>수정완료</button> :
                <button className={`min-w-fit`} onClick={() => setIsModified(true)}>수정하기</button>}

            <button className={`min-w-fit`} onClick={() => handleRemove(item?.id)}>삭제</button>
        </div>
    );
}
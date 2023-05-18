import React, { useEffect, useRef, useState } from "react";
import { UploadItem } from "@md/interfaces/upload.interface";

export default function Item (itemData : UploadItem, handleRemove: any) {
    const [isModified, setIsModified] = useState(false);
    const [item, setItem] = useState(itemData);
    const inputRef = useRef<HTMLInputElement | null>(null);

    const handleInputChange = (e : React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.name === "filePath") setItem({ ...item, [e.target.name]: inputRef.current?.value });
        else setItem({ ...item, [e.target.name!] : e.target.value! });
    };

    return(
        <div className="flex">
            <input  name={"name"}
                    value={item.name}
                    disabled={!isModified}
                    type={"text"}
                    onChange={handleInputChange}/>
            {
                isModified ? <input ref={inputRef} name={"filePath"} type={"file"} onChange={handleInputChange}/> : <div>{item.filePath as string}</div>
            }
            { isModified ? <button onClick={() => setIsModified(false)}>수정완료</button> : <button onClick={() => setIsModified(true)}>수정하기</button> }

            <button onClick={() => handleRemove(item.id)}>삭제</button>
        </div>
    );
}
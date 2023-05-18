import Layout from "@md/components/layout";
import Head from "next/head";
import Navigation from "@md/components/navigation";
import { useEffect, useRef, useState } from "react";
import { UploadItem } from "@md/interfaces/upload.interface";
import Item from "@md/components/upload/item";

export default function Upload () {
    const [item, setItem] = useState({} as UploadItem);
    const [items, setItems] = useState<UploadItem[]>([]);
    const inputRef = useRef<HTMLInputElement | null>(null);
    const nextId = useRef(0);

    const handleSubmit = () => {
        const data : UploadItem | any = {
            id: nextId.current,
            name: item.name as string,
            filePath: inputRef.current?.value as string,
        };
        setItems(items.concat(data));
        nextId.current += 1;
        setItem({name: "", filePath: ""});
        inputRef.current!.value = "";
    };

    const handleRemove = (id : number) => {
        setItems(items.filter(idx => idx!.id !== id));
    }

    const handleInputChange = (e: any) => {
        if (e.target.name === "filePath") setItem({ ...item, [e.target.name]: inputRef.current?.value });
        else setItem({ ...item, [e.target.name]: e.target.value });
    };


    return(
        <div>
            <Head>
                <title>모션 닥터 | 자세 등록</title>
                <meta name="description" content="Generated by create next app" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <Navigation></Navigation>
            <Layout>
                <div>자세 등록</div>
                <div>의사번호</div>

                <div>
                    <input  name={"name"}
                            value={item.name}
                            type={"text"}
                            onChange={handleInputChange}/>
                    <input  name={"filePath"}
                            type={"file"}
                            ref={inputRef}
                            onChange={handleInputChange}/>
                    <button onClick={handleSubmit}>등록하기</button>
                </div>

                <div>
                    {
                        items.map((idx) => {return <Item key={idx.id} {...idx} {...handleRemove}/>})
                    }
                </div>

                <button>제출하기</button>
            </Layout>
        </div>
    );
};
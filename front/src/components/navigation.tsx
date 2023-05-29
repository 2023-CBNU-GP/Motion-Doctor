import Link from "next/link";
import { useEffect, useState } from "react";
import { getCookie } from "@md/utils/cookies";
import axios from "@md/utils/axiosInstance";
import { DoctorSign, PatientSign } from "@md/interfaces/user.interface";

export default function Navigation() {
    const [isLogged, setIsLogged] = useState(getCookie('jwt'));
    const [logInfo, setLogInfo] = useState<DoctorSign | PatientSign>();

    useEffect(() => {
        if (isLogged) {
            axios.get('/api/user').then((res) => {
                setLogInfo(res.data);
            });
        }
    }, [isLogged]);

    const handleLogout = () => {
        axios.post('/api/logout').then();
    };

    return (
        <div
            className="px-[120px] py-8 w-full h-10 bg-white drop-shadow sticky top-0 text-center items-center flex flex justify-between">
            <div>
                <Link href="/" className="text-lg font-bold flex gap-2">
                    <div className="text-color-primary-500">Motion</div>
                    <div>Doctor</div>
                </Link>

            </div>

            <div>
                {
                    logInfo ? <div className="flex gap-3">
                        <div>{logInfo.name}</div>
                        <Link href="/" onClick={handleLogout}>로그아웃</Link></div> : <Link href="/">로그인</Link>
                }
            </div>
        </div>
    )
}

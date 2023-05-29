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
            <div className="flex items-center gap-16">
                <Link href="/" className="text-lg font-bold flex gap-2">
                    <div className="text-color-primary-500">Motion</div>
                    <div>Doctor</div>
                </Link>
                {
                    logInfo?.type === "doctor" &&
                    <div className="flex gap-6 text-sm">
                        <Link className="hover:text-color-primary-500" href="/doctor/manage">내가 등록한 재활 코스</Link>
                        <Link className="hover:text-color-primary-500" href="/test">재활코스 구경하기</Link>
                    </div>
                }
                {
                    logInfo?.type === "patient" &&
                    <div className="flex gap-6 text-sm">
                        <Link className="hover:text-color-primary-500" href="/patient/postures">내가 등록한 재활 코스</Link>
                        <Link className="hover:text-color-primary-500" href="/test">재활코스 구경하기</Link>
                    </div>

                }
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

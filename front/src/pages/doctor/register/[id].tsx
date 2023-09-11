import { useEffect, useState } from "react";
import axiosClient from "@md/utils/axiosInstance";
import { CourseDetail } from "@md/interfaces/course.interface";
import Link from "next/link";

export default function () {
    const [tabIdx, setTabIdx] = useState(0);
    const [courseDetail, setCourseDetail] = useState<CourseDetail>();

    useEffect(() => {
        const href = decodeURI(window.location.pathname).split('/');

        axiosClient.post('/api/video_list', {type: href.pop()}).then((res) => {
            setCourseDetail(res.data.data);
        })
    }, []);

    return (
        <div className="h-screen">
            <div className="flex h-full">
                <div className="h-full w-[25%] flex flex-col">
                    <div
                        className="relative flex h-full flex-col overflow-hidden drop-shadow-sm overflow-y-scroll divide-y divide-stone-200 divide-solid">
                        <div className="py-10 px-6 gap-0.5 flex flex-col">
                            <div><label className="font-bold text-lg">{courseDetail?.doctor_name}</label> 의사님의</div>
                            <div><label
                                className="text-color-info-500 font-semibold">{courseDetail?.courseName}</label> 재활코스
                            </div>
                        </div>

                        {
                            courseDetail?.trainList.map((trainItem, index) => {
                                return <div onClick={() => setTabIdx(index)} key={index}
                                            className={`${tabIdx === index && 'bg-color-primary-100'} py-5 px-3 text-center cursor-pointer `}>
                                    {trainItem}
                                </div>
                            })
                        }
                        <div
                            className="fixed inset-x-0 bottom-0 py-5 text-center cursor-pointer flex justify-center gap-5">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                                 stroke="currentColor" className="w-6 h-6">
                                <path strokeLinecap="round" strokeLinejoin="round"
                                      d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"/>
                            </svg>
                            <Link href={"/doctor/manage"}>나가기</Link>
                        </div>
                    </div>
                </div>
                <div className="w-full bg-gray-50 h-full">
                    <video controls style={{width: '100%', height: '100%', background: 'black'}}
                           src={process.env.NEXT_PUBLIC_API_KEY + '/media/' + courseDetail?.filePathList[tabIdx] as string}>
                    </video>
                </div>
            </div>

        </div>
    );
}
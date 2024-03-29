import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import axiosClient from "@md/utils/axiosInstance";
import { ManagePatientDetail } from "@md/interfaces/manage.interface";
import Link from "next/link";
import Head from "next/head";

export default function () {
    const [tabIdx, setTabIdx] = useState(0);
    const [feedback, setFeedback] = useState<boolean | null>();
    const [isSubmit, setIsSubmit] = useState<boolean>(false);
    const [isModify, setIsModify] = useState<boolean>(false);

    const [manageDetailData, setManageDetailData] = useState<ManagePatientDetail>();
    const router = useRouter();

    useEffect(() => {
        if (!router.isReady) return;
        axiosClient.post(`/api/manage/${router.query.id}`, {type: router.query.type}).then((res) => {
            setManageDetailData(res.data.data);
            // if(res.data.data.is)
        });
    }, [router.isReady, isSubmit, isModify]);

    useEffect(() => {
        setFeedback(null);
    }, [tabIdx])

    useEffect(() => {
    }, [isSubmit]);

    const handleSubmit = () => {
        const data = {
            'video': manageDetailData?.videoList[tabIdx],
            'text': feedback == true ? '내원 필요' : '내원 불필요'
        };
        axiosClient.post('/api/comment', data).then(res => {
            alert('피드백 등록 완료 하였습니다');
            setIsSubmit(true);
            setIsModify(false);
        });
    }

    return (
        <div className="h-screen">
            <Head>
                <title>모션 닥터 | 의사 환자 피드백페이지</title>
                <meta name="description" content="Generated by create next app"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="icon" href="/favicon.ico"/>
            </Head>

            <div className="flex h-full">
                <div className="h-full w-[25%] flex flex-col">
                    <div
                        className="relative flex h-full flex-col overflow-hidden drop-shadow-sm overflow-y-scroll divide-y divide-stone-200 divide-solid">
                        <div className="py-10 px-6 gap-0.5 flex flex-col">
                            <div><label className="font-bold text-lg">{manageDetailData?.patientName}</label>님</div>
                            <div><label
                                className="text-color-info-500 font-semibold">{manageDetailData?.trainTitle}</label> 테스트
                                결과
                            </div>
                        </div>
                        {
                            manageDetailData?.trainName.map((trainItem, index) => {
                                return <div onClick={() => setTabIdx(index)} key={index}
                                            className={`${tabIdx === index && 'bg-color-primary-100'} py-5 px-3 text-center cursor-pointer `}>
                                    {trainItem}
                                </div>
                            })
                        }
                        <Link href={`/doctor/manage`}
                              className="fixed inset-x-0 bottom-0 py-5 text-center cursor-pointer flex justify-center gap-5">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                                 stroke="currentColor" className="w-6 h-6">
                                <path strokeLinecap="round" strokeLinejoin="round"
                                      d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75"/>
                            </svg>
                            <div>나가기</div>
                        </Link>
                    </div>
                </div>
                <div className="w-full bg-gray-50 h-full">
                    <video controls style={{width: '100%', height: '91.5%', background: 'black'}}
                           src={manageDetailData && process.env.NEXT_PUBLIC_API_KEY + '/media/' + manageDetailData?.videoList[tabIdx] as string}>
                    </video>
                    <div className="flex items-center h-[8.5%] justify-between px-5">
                        <div className="flex gap-1">
                            <div className="pr-1 font-semibold">내원이 필요한 환자입니까?</div>
                            {
                                manageDetailData?.commentList[tabIdx] != null && !isModify ? <>
                                        <div>{manageDetailData?.commentList[tabIdx]}</div>
                                        <button
                                            onClick={() => setIsModify(true)}
                                            className={`ml-4 text-white rounded-sm px-2 text-sm bg-color-success-500`}>수정
                                        </button>
                                    </> :
                                    <>
                                        <div className="flex justify-center gap-1">Yes<input type="radio"
                                                                                             name="diagnosis"
                                                                                             onClick={() => setFeedback(true)}
                                                                                             checked={feedback == null ? false : feedback}/>
                                        </div>
                                        <div className="flex items-center gap-1">No<input type="radio" name="diagnosis"
                                                                                          onClick={() => setFeedback(false)}
                                                                                          checked={feedback == null ? false : !feedback}/>
                                        </div>
                                        <button
                                            onClick={handleSubmit}
                                            className={`ml-4 text-white rounded-sm px-2 text-sm bg-color-primary-500`}>제출
                                        </button>
                                    </>
                            }
                        </div>

                        <div className="flex gap-2">
                            <div className="font-semibold pr-1">AI 점수 :</div>
                            <label
                                className={`${(manageDetailData?.scoreList[tabIdx] as number > 50) ? "text-color-success-500" : "text-color-danger-500"} font-bold`}>{manageDetailData?.scoreList[tabIdx]}</label>
                            <label>/</label>
                            <label className="font-bold">100</label>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
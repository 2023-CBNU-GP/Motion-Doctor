import fetch from "node-fetch";
import { ManagePatientDetail, ManagePatients } from "@md/interfaces/manage.interface";
import { useEffect, useState } from "react";

export async function getStaticPaths() {
    const resManages = await fetch("http://localhost:3000" + "/api/get-manages");
    const manageData = await resManages.json();

    const paths = manageData.map((data: ManagePatients) => ({params: {id: data._id.toString()}}));

    return {paths, fallback: false};
}

export async function getStaticProps({params}: { params: string }) {
    // /api/get-manage/{params.id} 로 해줘야 함~
    const resManagesDetail = await fetch("http://localhost:3000" + "/api/get-manage");
    const manageDetailData = await resManagesDetail.json();

    return {props: {manageDetailData}};

}

export default function ({manageDetailData}: { manageDetailData: ManagePatientDetail }) {
    const [tabIdx, setTabIdx] = useState(0);
    const [feedback, setFeedback] = useState(true);

    useEffect(() => {
        setFeedback(true);
    }, [tabIdx])

    return (
        <div className="h-screen">
            <div className="flex h-full">
                <div className="h-full w-[25%] flex flex-col">
                    <div
                        className="relative flex h-full flex-col overflow-hidden drop-shadow-sm overflow-y-scroll divide-y divide-stone-200 divide-solid">
                        <div className="py-10 px-6 gap-0.5 flex flex-col">
                            <div><label className="font-bold text-lg">{manageDetailData.patientName}</label>님</div>
                            <div><label
                                className="text-color-info-500 font-semibold">{manageDetailData.trainTitle}</label> 테스트
                                결과
                            </div>
                        </div>

                        {
                            manageDetailData.trainList.map((trainItem, index) => {
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
                            <div>나가기</div>
                        </div>
                    </div>
                </div>
                <div className="w-full bg-gray-50 h-full">
                    <video controls style={{width: '100%', height: '91.5%', background: 'black'}}
                           src={manageDetailData.videoList[tabIdx] as string}>
                    </video>
                    <div className="flex items-center h-[8.5%] justify-between px-5">
                        <div className="flex gap-1">
                            <div className="pr-1 font-semibold">내원이 필요한 환자입니까?</div>
                            <div className="flex justify-center gap-1">Yes<input type="radio" name="diagnosis"
                                                                                 onClick={() => setFeedback(true)}
                                                                                 checked={feedback}/></div>
                            <div className="flex items-center gap-1">No<input type="radio" name="diagnosis"
                                                                              onClick={() => setFeedback(false)}
                                                                              checked={!feedback}/></div>
                            <button className="ml-4 text-white bg-color-primary-500 rounded-sm px-2 text-sm">제출</button>
                        </div>

                        <div className="flex gap-2">
                            <div className="font-semibold pr-1">AI 점수 :</div>
                            <label
                                className={`${(manageDetailData.scoreList[tabIdx] as number > 50) ? "text-color-success-500" : "text-color-danger-500"} font-bold`}>{manageDetailData.scoreList[tabIdx]}</label>
                            <label>/</label>
                            <label className="font-bold">100</label>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    );
}
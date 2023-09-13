import React from "react";
import { ManagePatients, RegisterTrain } from "@md/interfaces/manage.interface";
import Link from "next/link";
import VideoList from "@md/components/videoList";

export default function ManageItem({manageData, registerTrainData, handleRemove}: {
    manageData: ManagePatients[] | null,
    registerTrainData: RegisterTrain[] | null,
    handleRemove: any
}) {
    return (
        <div>
            <div className="flex flex-col mx-12 border-x border-t border-gray-50">
                <div className="flex items-center py-3.5 font-bold border-b-2 border-gray-50">
                    <div className="w-[10%] flex justify-center">번호</div>
                    <div
                        className="w-[50%] flex justify-center items-center">{registerTrainData ? "재활 코스 명" : "환자 이름"}</div>
                    <div className="w-[40%] flex justify-center">{registerTrainData ? "재활 코스내 운동 개수" : "재활 코스 명"}</div>
                    {manageData && <div className="w-[10%] flex justify-center">피드백 여부</div>}
                </div>
                {
                    manageData ? manageData!.map((data: ManagePatients, idx) => {
                        return (
                            <Link key={idx} href={{
                                pathname: `/doctor/manage/${data.uid}`,
                                query: {
                                    "type": `${data.trainCourse}-${data.idx}`
                                }
                            }}
                                  className="flex justify-between hover:bg-color-primary-100 border-b-2 border-gray-50 py-3.5">
                                <div className="w-[10%] flex justify-center">{idx + 1}</div>
                                <div className="w-[40%] flex justify-center">{data.patientName}</div>
                                <div className="w-[40%] flex justify-center">{data.trainCourse}</div>
                                <div className="w-[10%] flex justify-center">
                                    <input type="checkbox" defaultChecked={data.isCounseled}/>
                                </div>
                            </Link>
                        );
                    }) : registerTrainData?.map((data: RegisterTrain, idx) => {
                        return (
                            <div key={idx}>
                                <Link href={'/doctor/register/' + data.trainTitle + "-" + data.typeIdx}
                                      className="flex justify-between hover:bg-color-primary-100 border-b-2 border-gray-50 py-3.5">
                                    <div className="w-[10%] flex justify-center">{idx + 1}</div>
                                    <div className="w-[50%] flex justify-center">{data.trainTitle}</div>
                                    <div className="w-[40%] flex justify-center">{data.trainListLen}</div>
                                </Link>
                                <VideoList registerTrain={data} videos={data.video_info}
                                           handleRemove={handleRemove}/>
                            </div>
                        );
                    })
                }
            </div>
        </div>
    )
}
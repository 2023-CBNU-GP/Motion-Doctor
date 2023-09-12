import Image from "next/image";
import { DoctorInfo } from "@md/interfaces/user.interface";
import { ManagePatients, RegisterTrain } from "@md/interfaces/manage.interface";

export default function Profile({doctorData, manageData, registerTrain}: {
    doctorData: DoctorInfo,
    manageData: ManagePatients[] | null,
    registerTrain: RegisterTrain[] | null
}) {
    return (
        <div className="bg-gray-50 flex items-center py-7 pl-60">
            <Image src="/images/doctor-image.png" alt="doctor-image" width="80"
                   height="80"/>
            <div className="pl-8">
                <div className="font-bold">
                    <a href={'/doctor'}
                       className="text-xl hover:text-color-primary-500 hover:border-b-2 border-color-primary-500">{doctorData?.name}님</a> 반갑습니다!
                </div>
                <div className="flex gap-3">
                    <div>병원명: <label className="text-color-info-600 font-bold">{doctorData?.hospitalname}</label>
                    </div>
                    {
                        manageData && <div>담당 환자 수: <label
                            className="text-color-info-600 font-bold">{manageData?.length}</label>명
                        </div>
                    }
                    {
                        registerTrain && <div>등록 재활 운동 코스 수: <label
                            className="text-color-info-600 font-bold">{registerTrain?.length}</label>개
                        </div>
                    }
                </div>
            </div>
        </div>
    );
}
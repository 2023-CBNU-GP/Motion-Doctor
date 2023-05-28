import { NextApiRequest, NextApiResponse } from "next";
import { ManagePatients } from "@md/interfaces/manage.interface";

// 특정 의사가 본인의 재활 코스를 수강(?)한 환자 목록
export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<ManagePatients[]>
) {
    res.status(200).json([
        {_id: "1", patientName: "홍길동", trainCourse: "어깨 재활 치료", isCounseled: false},
        {_id: "2", patientName: "김수한무", trainCourse: "어깨 재활 치료", isCounseled: true},
        {_id: "3", patientName: "동방삭", trainCourse: "어깨 재활 치료", isCounseled: false},
    ]);
}
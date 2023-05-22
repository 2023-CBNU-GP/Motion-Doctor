import { NextApiRequest, NextApiResponse } from "next";
import { ManagePatients } from "@md/interfaces/manage.interface";

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
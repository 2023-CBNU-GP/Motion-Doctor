import { NextApiRequest, NextApiResponse } from "next";
import { DoctorInfo } from "@md/interfaces/user.interface";

// 특정 의사가 담당하는 환자의 수
export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<DoctorInfo>
) {
    res.status(200).json(
        {_id: "1", name: "홍길동", patientNum: 3}
    );
}
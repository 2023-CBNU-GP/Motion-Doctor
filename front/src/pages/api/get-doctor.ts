import { NextApiRequest, NextApiResponse } from "next";
import { DoctorInfo } from "@md/interfaces/user.interface";

// 의사 정보 가져오기 (유저 정보)
export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<DoctorInfo>
) {
    res.status(200).json(
        {_id: "1", name: "홍길동", hospitalname: "삼성 병원"}
    );
}
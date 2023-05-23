import { NextApiRequest, NextApiResponse } from "next";
import { DoctorInfo } from "@md/interfaces/user.interface";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<DoctorInfo>
) {
    res.status(200).json(
        {_id: "1", name: "홍길동", hospitalname: "삼성 병원"}
    );
}
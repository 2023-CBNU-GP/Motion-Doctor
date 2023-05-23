import { NextApiRequest, NextApiResponse } from "next";
import { DoctorSign } from "@md/interfaces/user.interface";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<DoctorSign[]>
) {
    res.status(200).json([
        {
            uid: "1",
            name: "홍길동",
            id: "asdf",
            email: "adsifjas@djafoid",
            doctornum: 1234,
            hospitalname: "삼성 병원",
            state: false
        },
        {
            uid: "2",
            name: "홍길동",
            id: "gsdj",
            email: "adsifjas@djafoid",
            doctornum: 4556,
            hospitalname: "삼성 병원",
            state: true
        },
    ]);
}
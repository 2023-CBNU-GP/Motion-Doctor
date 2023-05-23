import { NextApiRequest, NextApiResponse } from "next";
import { RegisterTrain } from "@md/interfaces/manage.interface";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<RegisterTrain[]>
) {
    res.status(200).json([
        {_id: "1", doctorName: "홍길동", trainTitle: "어깨 재활 운동", trainListLen: 3},
        {_id: "2", doctorName: "홍길동", trainTitle: "등 재활 운동", trainListLen: 3},
        {_id: "3", doctorName: "홍길동", trainTitle: "허리 재활 운동", trainListLen: 3},
    ]);
}
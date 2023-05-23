import { NextApiRequest, NextApiResponse } from "next";
import { PostureInfo } from "@md/interfaces/posture.interface";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<PostureInfo[]>
) {
    res.status(200).json([
        {
            _id: "1",
            trainTitle: "어깨 재활 운동1",
            trainNum: 3,
            doctorName: "홍길동",
            hospitalName: "삼성 병원",
            counselResult: "내원 불필요"
        },
        {
            _id: "2",
            trainTitle: "어깨 재활 운동2",
            trainNum: 4,
            doctorName: "김수한무",
            hospitalName: "삼성 병원",
            counselResult: "내원 필요"
        },
        {
            _id: "3",
            trainTitle: "어깨 재활 운동3",
            trainNum: 5,
            doctorName: "홍길동",
            hospitalName: "삼성 병원",
            counselResult: "내원 불필요"
        },
    ]);
}
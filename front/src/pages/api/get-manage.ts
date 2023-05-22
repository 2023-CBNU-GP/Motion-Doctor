import { NextApiRequest, NextApiResponse } from "next";
import { ManagePatientDetail } from "@md/interfaces/manage.interface";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<ManagePatientDetail>
) {
    res.status(200).json(
        {
            _id: '1',
            patientName: "홍길동",
            trainTitle: "어깨 재활 운동",
            trainList: ["호흡운동", "등배운동"],
            videoList: ["/videos/KakaoTalk_Video_2023-03-31-10-57-34.mp4", "/videos/KakaoTalk_Video_2023-03-31-10-57-34.mp4"],
            scoreList: [95, 45]
        }
    );
}
import { NextApiRequest, NextApiResponse } from "next";
import { ManagePatientDetail } from "@md/interfaces/manage.interface";

// 특정 의사가 특정 환자의 재활 테스트 영상 보기 위한 정보.
// 의사 피드백 등록하는 post 요청도 필요함
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
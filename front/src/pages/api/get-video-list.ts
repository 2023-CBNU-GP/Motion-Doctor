import { NextApiRequest, NextApiResponse } from "next";
import { CourseInfo } from "@md/interfaces/course.interface";

// 환자가 의사가 등록한 재활 코스 전체 보기
export default function handler(
    req: NextApiRequest,
    res: NextApiResponse<CourseInfo[]>
) {
    res.status(200).json([
        {doctor_name: "홍길동", doctor_hospitalName: "삼성병원", type: "어깨 재활 운동 코스", typeIdx: "SEDXCHYO", video_num: 3},
        {doctor_name: "홍길동", doctor_hospitalName: "삼성병원", type: "다리 재활 운동 코스", typeIdx: "KOFJNVID", video_num: 2},
        {doctor_name: "홍길동", doctor_hospitalName: "삼성병원", type: "허리 재활 운동 코스", typeIdx: "SEFETGCD", video_num: 5},
    ]);
}
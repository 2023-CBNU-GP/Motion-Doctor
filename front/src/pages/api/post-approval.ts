import { NextApiRequest, NextApiResponse } from "next";

// 관리자, 의사 권한 조절 post 요청
export default function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    if (req.method === "POST") {
        const body = JSON.parse(req.body);
        res.status(200).json({message: "success", data: {body}});
    }
}
import { NextApiRequest, NextApiResponse } from "next";

export default function handler(
    req: NextApiRequest,
    res: NextApiResponse
) {
    if (req.method === "POST") {
        const body = JSON.parse(req.body);
        res.status(200).json({message: "success", data: {body}});
    }
}
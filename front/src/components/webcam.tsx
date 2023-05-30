import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";
import axios from "@md/utils/axiosInstance";
import FormData from "form-data";

const URL = process.env.NEXT_PUBLIC_SOCKET + '/ws/socket_server';

export default function WebCam({typeData, name}: { typeData: string, name: string }) {
    const webcamRef = useRef<any>(null);
    const mediaRecorderRef = useRef<any>(null);
    const interval = useRef<any>();
    const socket = useRef<any>();
    const socket2 = useRef<any>();

    const [idx, setIdx] = useState(1);
    const [capturing, setCapturing] = useState(false);
    const [recordedChunks, setRecordedChunks] = useState([]);
    const [sendType, setSendType] = useState(false);

    // 옛날 영상 없애기
    const handleDataAvailable = useCallback(
        ({data}: any) => {
            if (data.size > 0) {
                setRecordedChunks((prev) => prev.concat(data));
            }
        },
        [setRecordedChunks]
    );

    // 영상 촬영 시작 && object-detection 을 위한 10초 마다 이미지 전송
    const handleStartCaptureClick = useCallback(() => {
        setCapturing(true);
        mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
            mimeType: "video/webm",
        });

        mediaRecorderRef.current.addEventListener(
            "dataavailable",
            handleDataAvailable
        );
        mediaRecorderRef.current.start();
        socket.current = new WebSocket(URL);
        socket.current.onopen = () => {
            console.log("연결 성공");
        }
        interval.current = setInterval(() => {
            const pictureSrc = webcamRef.current.getScreenshot();
            console.log(pictureSrc);
            socket.current.send(pictureSrc);
            socket.current.onmessage = (data: string) => {
                console.log(data);
            }
        }, 10000);

    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    // 영상 촬영 종료 && interval 제거
    const handleStopCaptureClick = useCallback(() => {
        mediaRecorderRef.current.stop();
        clearInterval(interval.current);
        handleNewSocket().then();
        setCapturing(false);
    }, [mediaRecorderRef, setCapturing]);

    const handleNewSocket = async () => {
        await socket.current.close(1000);
        socket.current.onclose = (e: any) => {
            if (e.code === 1000) {
                console.log(e);
            }
        }
        axios.get(process.env.NEXT_PUBLIC_API_KEY + "/api/user").then((response) => {
            socket2.current = new WebSocket(process.env.NEXT_PUBLIC_SOCKET + "/ws/" + response.data.uid);
            socket2.current.onopen = () => {
                console.log("연결");
                setSendType(true);
            }
        });
    }

    const handleSend = async () => {
        console.log("work");
        socket2.current.send(JSON.stringify({type: typeData}));
        setSendType(false);
    }

    useEffect(() => {
        if (sendType) {
            handleSend().then(() => {
                socket2.current.onmessage = (event: any) => {
                    const json_data = JSON.parse(event.data);
                    console.log("socket2: " + json_data.message);
                }
            });
        }
    }, [sendType]);


    // 촬영 종료된 영상이 있으면 서버에 전송
    useEffect(() => {
        if (recordedChunks.length) {
            const blob = new Blob(recordedChunks, {
                type: "video/webm",
            });
            const formData = new FormData();
            formData.append('name', name);
            formData.append('type', typeData);
            formData.append('file_path', blob);
            axios.post("/api/evaluation", formData).then();
            setRecordedChunks([]);
            setIdx(idx + 1);
        }
    }, [recordedChunks]);

    return (
        <div className="w-full h-full flex flex-col">
            <div className="h-10 bg-stone-800 flex gap-4 justify-center items-center">
                {capturing ? (
                    <div onClick={handleStopCaptureClick} className="cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-8 h-8">
                            <path fillRule="evenodd"
                                  d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z"
                                  clipRule="evenodd"/>
                        </svg>
                    </div>
                ) : (
                    <div onClick={handleStartCaptureClick} className="cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-8 h-8">
                            <path fillRule="evenodd"
                                  d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm14.024-.983a1.125 1.125 0 010 1.966l-5.603 3.113A1.125 1.125 0 019 15.113V8.887c0-.857.921-1.4 1.671-.983l5.603 3.113z"
                                  clipRule="evenodd"/>
                        </svg>
                    </div>
                )}
            </div>
            <Webcam
                style={{
                    height: "100%",
                    width: "100%",
                    objectFit: "cover",
                }}
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
            />
        </div>
    );
};
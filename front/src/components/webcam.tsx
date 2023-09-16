import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";
import axios from "@md/utils/axiosInstance";

const URL = process.env.NEXT_PUBLIC_SOCKET + '/ws/socket_server';
const VIDEO_URL = process.env.NEXT_PUBLIC_SOCKET + '/ws/webcam';

export default function WebCam({typeData, name}: { typeData: string, name: string }) {
    const webcamRef = useRef<any>(null);
    const mediaRecorderRef = useRef<any>(null);
    const interval = useRef<any>();

    const socketObDect = useRef<any>();
    const socketScore = useRef<any>();
    const socketVideo = useRef<any>();

    const [base64Data, setBase64Data] = useState<any>(null);
    const [sendVideo, setSendVideo] = useState(true);
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
        mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {mimeType: 'video/webm;'});

        mediaRecorderRef.current.addEventListener(
            "dataavailable",
            handleDataAvailable
        );
        mediaRecorderRef.current.start();

        socketObDect.current = new WebSocket(URL);
        socketObDect.current.onopen = () => {
            console.log("연결 성공");
        }
        interval.current = setInterval(() => {
            const pictureSrc = webcamRef.current.getScreenshot();
            socketObDect.current.send(pictureSrc);
            socketObDect.current.onmessage = (data: string) => {
                console.log(data);
            }
        }, 10000);

    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    // 영상 촬영 종료 && interval 제거
    const handleStopCaptureClick = useCallback(() => {
        mediaRecorderRef.current.stop();
        clearInterval(interval.current);
        handleVideoSocket().then(() => {
        });
        setCapturing(false);
    }, [mediaRecorderRef, setCapturing]);

    const handleVideoSocket = async () => {
        await socketObDect.current.close(1000);
        socketObDect.current.onclose = (e: any) => {
            if (e.code === 1000) {
                console.log(e);
            }
        }

        socketVideo.current = new WebSocket(VIDEO_URL);
        socketVideo.current.onopen = () => {
            console.log("연결");
            setSendVideo(true);
        }
    }

    const handleSendVideo = async () => {
        await axios.get(process.env.NEXT_PUBLIC_API_KEY + "/api/user").then((response) => {
            socketVideo.current?.send(JSON.stringify({
                patient_id: response.data.id as string,
                exercise_name: name,
                exercise_type: typeData,
                video_data: base64Data,
            }));
        });
        setSendVideo(false);
        // console.log(data);
    }

    useEffect(() => {
        if (sendVideo) {
            handleSendVideo().then(() => {
                handleNewSocket().then();
            });
        }
    }, [sendVideo]);

    const handleNewSocket = async () => {
        if (socketVideo.current !== undefined) {
            await socketVideo.current?.close(1000);

            socketVideo.current.onclose = (e: any) => {
                if (e.code === 1000) {
                    console.log(e);
                }
            }

            axios.get(process.env.NEXT_PUBLIC_API_KEY + "/api/user").then((response) => {
                socketScore.current = new WebSocket(process.env.NEXT_PUBLIC_SOCKET + "/ws/" + response.data.uid);
                socketScore.current.onopen = () => {
                    console.log("연결");
                    setSendType(true);
                }
            });
        }
    }

    const handleSend = async () => {
        socketScore.current?.send(JSON.stringify({type: typeData, name: name}));
        setSendType(false);
    }

    useEffect(() => {
        if (sendType) {
            handleSend().then(() => {
                socketScore.current.onmessage = (event: any) => {
                    const json_data = JSON.parse(event.data);
                    console.log("socket2: " + json_data.message);
                }
            });
        }
    }, [sendType]);


    // 촬영 종료된 영상이 있으면 서버에 전송
    useEffect(() => {
        if (recordedChunks.length && mediaRecorderRef.current.state === "inactive") {
            console.log(mediaRecorderRef.current.state);

            const blob = new Blob(recordedChunks, {
                type: "video/webm",
            });

            const reader = new FileReader();

            reader.onload = () => {
                const data = reader.result;
                setBase64Data(data);
                setRecordedChunks([]);
                setIdx(idx + 1);
            };

            reader.readAsDataURL(blob);
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
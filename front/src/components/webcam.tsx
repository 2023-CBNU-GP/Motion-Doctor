import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";
import axios from "@md/utils/axiosInstance";

const URL = process.env.NEXT_PUBLIC_SOCKET + '/ws/socket_server';
const VIDEO_URL = process.env.NEXT_PUBLIC_SOCKET + '/ws/webcam';

export default function WebCam({typeData, name, setTime, setVideoResult, setIsCaptured}: {
    typeData: string,
    name: string,
    setTime: any,
    setVideoResult: any,
    setIsCaptured: any,
}) {
    const webcamRef = useRef<any>(null);
    const mediaRecorderRef = useRef<any>();
    const interval = useRef<any>();

    const socketObject = useRef<any>();
    const socketVideo = useRef<any>();

    const [base64Data, setBase64Data] = useState<any>(null);
    const [sendVideo, setSendVideo] = useState(false);
    const [idx, setIdx] = useState(1);
    const [capturing, setCapturing] = useState(false);
    const [recordedChunks, setRecordedChunks] = useState([]);

    // 옛날 영상 없애기
    const handleDataAvailable = useCallback(
        ({data}: any) => {
            if (data.size > 0) {
                setRecordedChunks((prev) => prev.concat(data));
            }
        },
        [setRecordedChunks]
    );

    function sleep(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    const startTimer = () => {
        let times = 1;
        setTime(1);
        return new Promise((resolve, reject) => {
            const interval1 = setInterval(() => {
                if (times <= 10) {
                    times++;
                    setTime(times);
                    resolve(times);
                } else {
                    clearInterval(interval1);
                    reject(new Error('500'));
                }
            }, 1000);
        });
    }


    // 영상 촬영 시작 && object-detection 을 위한 10초 마다 이미지 전송
    const handleStartCaptureClick = useCallback(async () => {
        startTimer().then();
        await sleep(10000);

        setCapturing(true);
        setIsCaptured(true);

        mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {mimeType: 'video/webm;'});

        mediaRecorderRef.current.addEventListener(
            "dataavailable",
            handleDataAvailable
        );

        mediaRecorderRef.current.start();

        socketObject.current = new WebSocket(URL);
        socketObject.current.onopen = () => {
            console.log("연결 성공");
        }

        interval.current = setInterval(() => {
            const pictureSrc = webcamRef.current.getScreenshot();
            socketObject.current.send(pictureSrc);
            socketObject.current.onmessage = (data: string) => {
                console.log(data);
            }
        }, 10000);

    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    // 영상 촬영 종료 && interval 제거
    const handleStopCaptureClick = useCallback(() => {
        mediaRecorderRef.current.stop();
        clearInterval(interval.current);
        handleVideoSocket().then(() => {
            socketVideo.current.onmessage = (data: any) => {
                if (data.data != "Video saved successfully.") {
                    const result = JSON.parse(data.data);
                    if (result.type === "return value") {
                        setVideoResult(result);
                    }
                    console.log(data.data);
                }
            }
        });
        setCapturing(false);
    }, [mediaRecorderRef, setCapturing]);

    const handleVideoSocket = async () => {
        await socketObject.current.close(1000);
        socketObject.current.onclose = (e: any) => {
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
                alert('재활 운동을 등록하였습니다.');
            });
        }
    }, [sendVideo]);


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
                    <div onClick={() => {
                        if (webcamRef.current.stream != null) {
                            handleStartCaptureClick();
                        }
                    }} className="cursor-pointer">
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
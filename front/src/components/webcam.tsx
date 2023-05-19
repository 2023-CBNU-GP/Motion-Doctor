import Webcam from "react-webcam";
import { useCallback, useEffect, useRef, useState } from "react";

export default function WebCam() {
    const webcamRef = useRef(null);
    const mediaRecorderRef = useRef<any>(null);

    const [capturing, setCapturing] = useState(false);
    const [recordedChunks, setRecordedChunks] = useState([]);

    useEffect(() => {
        while (capturing) {
            setTimeout(() => {
                console.log("true")
            }, 30000)
        }
        // if (capturing)
        // else console.log("false");
    }, [capturing]);

    const handleDataAvailable = useCallback(
        ({data}: any) => {
            if (data.size > 0) {
                setRecordedChunks((prev) => prev.concat(data));
            }
        },
        [setRecordedChunks]
    );

    const handleStartCaptureClick = useCallback(() => {
        setCapturing(true);
        //@ts-ignore
        mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
            mimeType: "video/webm",
        });
        mediaRecorderRef.current.addEventListener(
            "dataavailable",
            handleDataAvailable
        );
        mediaRecorderRef.current.start();
    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    const handleStopCaptureClick = useCallback(() => {
        mediaRecorderRef.current.stop();
        setCapturing(false);
    }, [mediaRecorderRef, setCapturing]);

    const handleDownload = useCallback(() => {
        // if (recordedChunks.length) {
        //     const blob = new Blob(recordedChunks, {
        //         type: "video/mp4",
        //     });
        //     console.log(blob);
        // }
        if (recordedChunks.length) {
            const blob = new Blob(recordedChunks, {
                type: "video/webm",
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            document.body.appendChild(a);
            a.setAttribute('style', "display: none");
            a.href = url;
            a.download = "motion.webm";
            a.click();
            window.URL.revokeObjectURL(url);
            setRecordedChunks([]);
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
                {recordedChunks.length > 0 && (
                    <div onClick={handleDownload} className="cursor-pointer">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-8 h-8">
                            <path fillRule="evenodd"
                                  d="M19.5 21a3 3 0 003-3V9a3 3 0 00-3-3h-5.379a.75.75 0 01-.53-.22L11.47 3.66A2.25 2.25 0 009.879 3H4.5a3 3 0 00-3 3v12a3 3 0 003 3h15zm-6.75-10.5a.75.75 0 00-1.5 0v4.19l-1.72-1.72a.75.75 0 00-1.06 1.06l3 3a.75.75 0 001.06 0l3-3a.75.75 0 10-1.06-1.06l-1.72 1.72V10.5z"
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
                // screenshotFormat="image/jpeg"
            />
        </div>
    );
};
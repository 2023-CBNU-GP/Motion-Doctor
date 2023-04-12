import Webcam from "react-webcam";
import { useCallback, useRef, useState } from "react";
import * as posenet from '@tensorflow-models/posenet';
import { drawKeypoints, drawSkeleton } from "@md/hooks/drawPoints";

export default function WebCam() {
    const webcamRef = useRef(null);
    const mediaRecorderRef = useRef(null);
    const canvasRef = useRef(null);

    const detectWebcamFeed = async (posenet_model) => {
        if (
            typeof webcamRef.current !== "undefined" &&
            webcamRef.current !== null &&
            webcamRef.current.video.readyState === 4
        ) {
            // Get Video Properties
            const video = webcamRef.current.video;
            const videoWidth = webcamRef.current.video.videoWidth;
            const videoHeight = webcamRef.current.video.videoHeight;
            // Set video width
            webcamRef.current.video.width = videoWidth;
            webcamRef.current.video.height = videoHeight;
            // Make Estimation
            const pose = await posenet_model.estimateSinglePose(video);
            drawResult(pose, video, videoWidth, videoHeight, canvasRef);
        }
    };

    const runPosenet = async () => {
        const posenet_model = await posenet.load({
            inputResolution: { width: 640, height: 480 },
            scale: 0.8
        });
        //
        setInterval(() => {
            detectWebcamFeed(posenet_model);
        }, 100);
    };

    runPosenet();

    const drawResult = (pose, video, videoWidth, videoHeight, canvas) => {
        const ctx = document.getElementById('canvas');

        // const ctx = canvas.current.getContext("2d");
        if (ctx) {
            canvas.current.width = videoWidth;
            canvas.current.height = videoHeight;
            drawKeypoints(pose["keypoints"], 0.6, ctx);
            drawSkeleton(pose["keypoints"], 0.7, ctx);
        }
    };



    const [capturing, setCapturing] = useState(false);
    const [recordedChunks, setRecordedChunks] = useState([]);

    const handleDataAvailable = useCallback(
        ({ data }) => {
            if (data.size > 0) {
                setRecordedChunks((prev) => prev.concat(data));
            }
        },
        [setRecordedChunks]
    );

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
    }, [webcamRef, setCapturing, mediaRecorderRef, handleDataAvailable]);

    const handleStopCaptureClick = useCallback(() => {
        mediaRecorderRef.current.stop();
        setCapturing(false);
    }, [mediaRecorderRef, setCapturing]);

    const handleDownload = useCallback(() => {
        if (recordedChunks.length) {
            const blob = new Blob(recordedChunks, {
                type: "video/mp4",
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = url;
            a.download = "motion.mp4";
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
                          <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm6-2.438c0-.724.588-1.312 1.313-1.312h4.874c.725 0 1.313.588 1.313 1.313v4.874c0 .725-.588 1.313-1.313 1.313H9.564a1.312 1.312 0 01-1.313-1.313V9.564z" clipRule="evenodd" />
                      </svg>
                  </div>
              ) : (
                  <div onClick={handleStartCaptureClick} className="cursor-pointer">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-8 h-8">
                          <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm14.024-.983a1.125 1.125 0 010 1.966l-5.603 3.113A1.125 1.125 0 019 15.113V8.887c0-.857.921-1.4 1.671-.983l5.603 3.113z" clipRule="evenodd" />
                      </svg>
                  </div>
              )}
              {recordedChunks.length > 0 && (
                  <div onClick={handleDownload} className="cursor-pointer">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="white" className="w-8 h-8">
                          <path fillRule="evenodd" d="M19.5 21a3 3 0 003-3V9a3 3 0 00-3-3h-5.379a.75.75 0 01-.53-.22L11.47 3.66A2.25 2.25 0 009.879 3H4.5a3 3 0 00-3 3v12a3 3 0 003 3h15zm-6.75-10.5a.75.75 0 00-1.5 0v4.19l-1.72-1.72a.75.75 0 00-1.06 1.06l3 3a.75.75 0 001.06 0l3-3a.75.75 0 10-1.06-1.06l-1.72 1.72V10.5z" clipRule="evenodd" />
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
          />
          <canvas
              id={"canvas"}
              ref={canvasRef}
              style={{
                  position: "absolute",
                  marginTop: "2.5rem",
                  textAlign: "center",
                  zindex: 9,
                  width: "100%",
                  height: "100%"
              }}
          />
      </div>
  );
};
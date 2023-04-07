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
        const ctx = canvas.current.getContext("2d");
        canvas.current.width = videoWidth;
        canvas.current.height = videoHeight;
        drawKeypoints(pose["keypoints"], 0.6, ctx);
        drawSkeleton(pose["keypoints"], 0.7, ctx);
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

        // posenet.load().then((model));

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
          <div className="h-10 bg-color-primary-500">
              {capturing ? (
                  <button onClick={handleStopCaptureClick}>Stop Capture</button>
              ) : (
                  <button onClick={handleStartCaptureClick}>Start Capture</button>
              )}
              {recordedChunks.length > 0 && (
                  <button onClick={handleDownload}>Download</button>
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
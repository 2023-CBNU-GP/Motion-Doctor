import Navigation from "@md/components/navigation";
import Head from "next/head";
import WebCam from "@md/components/webcam";
import Message from "@md/components/modal/message";
import Timer from "@md/components/modal/timer";
import { CourseDetail } from "@md/interfaces/course.interface";
import { UserInfo } from "@md/interfaces/user.interface";
import { useRouter } from "next/dist/client/router";
import { useEffect, useRef, useState } from "react";
import axiosClient from "@md/utils/axiosInstance";

export default function TestItem() {
    const [type, setType] = useState<string>();
    const [courseDetail, setCourseDetail] = useState<CourseDetail>();
    const [isModal, setIsModal] = useState<boolean>(false);
    const [isFinished, setIsFinished] = useState<boolean>(false);

    const vidRef = useRef<any>(null);
    const [isPause, setIsPause] = useState(false);
    const [tabIdx, setTabIdx] = useState(0);
    const [time, setTime] = useState<number>(0);
    const [user, setUser] = useState<UserInfo>();

    const router = useRouter();

    // 첫 렌더링 때 특정 코스에 대한 전체 데이터 불러오는 api
    useEffect(() => {
        if (!router.isReady) return;
        else {
            alert("**새로고침이 될 시, 기존 테스트 데이터들이 모두 삭제됩니다**");
            const href = decodeURI(router.query.id as string);
            axiosClient.get('/api/user').then((res) => {
                setUser(res.data);
            })
            setType(href);
        }
    }, [router.isReady]);

    useEffect(() => {
        if (type) {
            axiosClient.post('/api/video_list', {type: type}).then(res => {
                console.log(res.data.data);
                setCourseDetail(res.data.data);
            });
        }
    }, [type]);

    const handlePlayVideo = () => {
        if (!isPause) {
            vidRef.current.play();
        } else {
            vidRef.current.pause();
        }
    }

    return (
        <div className="h-screen overflow-hidden">
            <Head>
                <title>모션 닥터 | 자세 검사</title>
                <meta name="description" content="Generated by create next app"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <link rel="icon" href="/favicon.ico"/>
            </Head>

            {
                (time != 11 && 0 != time) && <Timer time={time}></Timer>
            }

            {
                isModal && <Message setIsModal={setIsModal}
                                    title={'수고하셨습니다'}
                                    content={'재활코스 동영상 저장을 완료하였습니다.'}
                />
            }

            <Navigation></Navigation>

            <div className="flex h-full">
                <div className="h-full w-[20%] flex flex-col">
                    <div
                        className="flex h-full flex-col overflow-hidden drop-shadow-sm overflow-y-scroll divide-y divide-stone-200 divide-solid">
                        <div className="py-10 px-6 gap-0.5 flex flex-col">
                            <div className="flex gap-2 text-sm">
                                <div><label
                                    className="text-color-primary-600 font-semibold">{courseDetail?.doctor_hospitalName}</label> 병원
                                </div>
                                <div><label
                                    className="text-color-primary-600 font-semibold">{courseDetail?.doctor_name}</label> 의사님의
                                </div>
                            </div>
                            <div className="text-lg"><label
                                className="font-bold">{courseDetail?.courseName}</label> 재활 목록
                            </div>
                        </div>
                        {
                            courseDetail && courseDetail?.trainList.map((item, idx) => {
                                return <div key={idx} onClick={() => {
                                    setTabIdx(idx);
                                }}
                                            className={`${idx === tabIdx && "bg-color-primary-100 font-bold"} py-5 px-3 text-center cursor-pointer `}>
                                    {courseDetail.trainList[idx]}
                                </div>
                            })
                        }
                    </div>

                    <div className="fixed w-[20%] inset-x-0 bottom-0 py-5 px-3 text-center cursor-pointer"
                         onClick={() => setIsModal(true)}>자세등록하기
                    </div>
                </div>
                <div className="h-full w-[40%] relative">
                    <div className='w-full h-full z-0'>
                        <WebCam typeData={type! as string} name={courseDetail?.trainList[tabIdx] as string}
                                setTime={setTime}></WebCam>
                    </div>
                </div>
                <div className="h-full w-[40%]">
                    {courseDetail &&
                        <video controls
                               src={process.env.NEXT_PUBLIC_API_KEY + '/media/' + courseDetail.filePathList[tabIdx]}
                               style={{width: "100%", height: "93%", background: 'black', cursor: 'pointer'}}
                               onClick={() => {
                                   setIsPause(!isPause);
                                   handlePlayVideo();
                               }} ref={vidRef}
                        ></video>
                    }
                </div>
            </div>
        </div>
    );
}


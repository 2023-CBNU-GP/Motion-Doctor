export interface CourseInfo {
    doctor_name: string,
    doctor_hospitalName: string,
    video_num: number,
    type?: string,
    typeIdx?: string,
}

export interface CourseDetail {
    doctor_name: string,
    doctor_hospitalName: string,
    // 코스 전체 명
    courseName: string,
    // 코스 내 운동 목록
    trainList: Array<string>,
    // 코스 내 운동목록에 대한 동영상 파일들
    filePathList: Array<string>,
}

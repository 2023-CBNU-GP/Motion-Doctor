export interface ManagePatients {
    _id: string,
    patientName: string,
    trainCourse: string,
    // 피드백 여부
    isCounseled: boolean,
}

export interface ManagePatientDetail {
    _id: string,
    patientName: string,
    trainTitle: string,
    trainList: Array<string>,
    videoList: Array<string | File>,
    scoreList: Array<number>,
}

export interface RegisterTrain {
    _id: string,
    doctorName?: string,
    trainTitle: string,
    trainListLen: number,
}